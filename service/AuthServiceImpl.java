package service;

import exception.InvalidInputException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import model.User;

/**
 * Phase 2 & 4: Structured Programming & Authentication Service.
 * Implements robust role detection, MySQL JDBC query, and memory fallback.
 */
public class AuthServiceImpl implements AuthService, UserOperations {

    // Thread-safe in-memory fallback store seeded with required academic accounts
    private static final Map<String, User> MEMORY_USERS = new ConcurrentHashMap<>();

    static {
        seedDefaultAccounts();
    }

    private static void seedDefaultAccounts() {
        // Pre-populated academic accounts specified in requirements
        User student = new User(1, "studentjohn", "pass123", "student", "21MCA015",
                "John Doe", "Computer Applications", "MCA");
        User staff = new User(2, "staffjacob", "jacob1234", "staff", "STF001",
                "Prof. Jacob Mathew", "Computer Applications", "MCA Faculty");
        User hod = new User(3, "hodsmith", "hod1234", "hod", "HOD001",
                "Dr. Alan Smith", "Computer Applications", "Head of Department");

        // Legacy compatibility accounts
        User edwin = new User(4, "edwin21", "pass123", "student", "21CS045",
                "Edwin Saji", "Computer Science", "B.Tech CSE");
        User aisha = new User(5, "aisha09", "aisha2024", "student", "21CS046",
                "Aisha Khan", "Electronics", "B.Tech ECE");

        MEMORY_USERS.put("studentjohn", student);
        MEMORY_USERS.put("21mca015", student);
        MEMORY_USERS.put("staffjacob", staff);
        MEMORY_USERS.put("hodsmith", hod);
        MEMORY_USERS.put("edwin21", edwin);
        MEMORY_USERS.put("21cs045", edwin);
        MEMORY_USERS.put("aisha09", aisha);
        MEMORY_USERS.put("21cs046", aisha);
    }

    @Override
    public boolean validateInput(String username, String password) throws InvalidInputException {
        if (username == null || username.trim().isEmpty()) {
            throw new InvalidInputException("Username cannot be empty.");
        }
        if (password == null || password.trim().isEmpty()) {
            throw new InvalidInputException("Password cannot be empty.");
        }
        if (password.trim().length() < 6) {
            throw new InvalidInputException("Password must be at least 6 characters.");
        }
        return true;
    }

    @Override
    public boolean validateRegistration(String username, String password, String rollNo)
            throws InvalidInputException {
        validateInput(username, password);
        if (rollNo == null || rollNo.trim().isEmpty()) {
            throw new InvalidInputException("Roll Number cannot be empty.");
        }
        return true;
    }

    @Override
    public User authenticate(String username, String password, String role) throws InvalidInputException {
        validateInput(username, password);

        String cleanUsername = username.trim();
        String cleanPassword = password.trim();

        // 1. Try MySQL Database Authentication via JDBC
        Connection conn = null;
        PreparedStatement stmt = null;
        ResultSet rs = null;
        try {
            conn = DBConnection.getConnection();
            String sql = "SELECT id, username, password, role, roll_no, full_name, department, course " +
                         "FROM users WHERE LOWER(username) = LOWER(?)";
            stmt = conn.prepareStatement(sql);
            stmt.setString(1, cleanUsername);
            rs = stmt.executeQuery();

            if (rs.next()) {
                String dbPass = rs.getString("password");
                String dbRole = rs.getString("role");
                if (dbRole != null) dbRole = dbRole.trim().toLowerCase();

                if (cleanPassword.equals(dbPass)) {
                    return new User(
                            rs.getInt("id"),
                            rs.getString("username"),
                            rs.getString("password"),
                            dbRole,
                            rs.getString("roll_no"),
                            rs.getString("full_name"),
                            rs.getString("department"),
                            rs.getString("course")
                    );
                } else {
                    return null; // Invalid password
                }
            }
        } catch (SQLException e) {
            System.err.println("[AuthService] MySQL query failed, falling back to memory store: " + e.getMessage());
        } finally {
            DBConnection.closeQuietly(rs, stmt, conn);
        }

        // 2. Memory Store Fallback
        User fallbackUser = MEMORY_USERS.get(cleanUsername.toLowerCase());
        if (fallbackUser != null && fallbackUser.getPassword().equals(cleanPassword)) {
            return fallbackUser;
        }

        return null;
    }

    @Override
    public boolean registerUser(User user) throws InvalidInputException {
        if (user == null) {
            throw new InvalidInputException("User data cannot be null.");
        }
        validateRegistration(user.getUsername(), user.getPassword(), user.getRollNo());

        String cleanUser = user.getUsername().trim().toLowerCase();

        // 1. Persist to MySQL Database via JDBC
        Connection conn = null;
        PreparedStatement checkStmt = null;
        PreparedStatement insertStmt = null;
        ResultSet rs = null;
        boolean dbSuccess = false;

        try {
            conn = DBConnection.getConnection();
            // Check for existing username or roll number
            String checkSql = "SELECT COUNT(*) FROM users WHERE LOWER(username) = LOWER(?) OR LOWER(roll_no) = LOWER(?)";
            checkStmt = conn.prepareStatement(checkSql);
            checkStmt.setString(1, cleanUser);
            checkStmt.setString(2, user.getRollNo().trim().toLowerCase());
            rs = checkStmt.executeQuery();
            if (rs.next() && rs.getInt(1) > 0) {
                throw new InvalidInputException("Account with this Roll Number already exists! Please sign in.");
            }

            // Insert new student user
            String insertSql = "INSERT INTO users (username, password, role, roll_no, full_name, department, course) " +
                               "VALUES (?, ?, 'student', ?, ?, ?, ?)";
            insertStmt = conn.prepareStatement(insertSql);
            insertStmt.setString(1, user.getUsername().trim());
            insertStmt.setString(2, user.getPassword().trim());
            insertStmt.setString(3, user.getRollNo().trim().toUpperCase());
            insertStmt.setString(4, user.getFullName() != null ? user.getFullName().trim() : user.getUsername().trim());
            insertStmt.setString(5, user.getDepartment() != null ? user.getDepartment().trim() : "Computer Applications");
            insertStmt.setString(6, user.getCourse() != null ? user.getCourse().trim() : "MCA");

            int rows = insertStmt.executeUpdate();
            dbSuccess = (rows > 0);
        } catch (SQLException e) {
            System.err.println("[AuthService] MySQL register failed, applying memory fallback: " + e.getMessage());
            if (e.getErrorCode() == 1062 || (e.getMessage() != null && e.getMessage().toLowerCase().contains("duplicate"))) {
                throw new InvalidInputException("Account with this Roll Number already exists! Please sign in.");
            }
        } finally {
            DBConnection.closeQuietly(rs, checkStmt, insertStmt, conn);
        }

        // 2. Check & Save in Memory Store
        if (MEMORY_USERS.containsKey(cleanUser) || 
            MEMORY_USERS.values().stream().anyMatch(u -> u.getRollNo() != null && u.getRollNo().equalsIgnoreCase(user.getRollNo()))) {
            throw new InvalidInputException("Account with this Roll Number already exists! Please sign in.");
        }

        user.setRole("student");
        MEMORY_USERS.put(cleanUser, user);
        if (user.getRollNo() != null && !user.getRollNo().trim().isEmpty()) {
            MEMORY_USERS.put(user.getRollNo().trim().toLowerCase(), user);
        }
        return true;
    }

    @Override
    public User getUserByUsername(String username) {
        if (username == null) return null;
        String cleanUser = username.trim().toLowerCase();

        // 1. Try MySQL
        Connection conn = null;
        PreparedStatement stmt = null;
        ResultSet rs = null;
        try {
            conn = DBConnection.getConnection();
            String sql = "SELECT id, username, password, role, roll_no, full_name, department, course " +
                         "FROM users WHERE LOWER(username) = LOWER(?)";
            stmt = conn.prepareStatement(sql);
            stmt.setString(1, cleanUser);
            rs = stmt.executeQuery();

            if (rs.next()) {
                return new User(
                        rs.getInt("id"),
                        rs.getString("username"),
                        rs.getString("password"),
                        rs.getString("role").toLowerCase(),
                        rs.getString("roll_no"),
                        rs.getString("full_name"),
                        rs.getString("department"),
                        rs.getString("course")
                );
            }
        } catch (SQLException e) {
            System.err.println("[AuthService] MySQL getUserByUsername failed: " + e.getMessage());
        } finally {
            DBConnection.closeQuietly(rs, stmt, conn);
        }

        // 2. Memory Store Fallback
        return MEMORY_USERS.get(cleanUser);
    }

    @Override
    public boolean authenticate(User user, String inputUsername, String inputPassword) {
        if (user == null || inputUsername == null || inputPassword == null) {
            return false;
        }
        return user.getUsername().equalsIgnoreCase(inputUsername.trim())
                && user.getPassword().equals(inputPassword.trim());
    }
}
