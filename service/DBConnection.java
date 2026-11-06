package service;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * Phase 2 & 4: Database Connection Manager with Automatic Schema Migration & Account Seeding.
 */
public class DBConnection {
    // Database configuration
    private static final String DB_HOST = System.getProperty("db.host", "localhost");
    private static final String DB_PORT = System.getProperty("db.port", "3306");
    private static final String DB_NAME = System.getProperty("db.name", "digital_od");
    private static final String DB_USER = System.getProperty("db.user", "root");
    private static final String DB_PASSWORD = System.getProperty("db.password", "");

    private static final String JDBC_URL = "jdbc:mysql://" + DB_HOST + ":" + DB_PORT + "/" + DB_NAME
            + "?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC&characterEncoding=UTF-8&connectTimeout=500&socketTimeout=1000";

    private static final String SERVER_URL = "jdbc:mysql://" + DB_HOST + ":" + DB_PORT
            + "/?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC&characterEncoding=UTF-8&connectTimeout=500&socketTimeout=1000";

    private static volatile boolean dbInitialized = false;
    private static volatile String activePassword = null;
    private static volatile boolean checkedAllPasswords = false;
    private static volatile SQLException cachedFailure = null;

    static {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            try {
                Class.forName("com.mysql.jdbc.Driver");
            } catch (ClassNotFoundException ex) {
                System.err.println("[DBConnection] MySQL JDBC Driver not found: " + ex.getMessage());
            }
        }
    }

    /**
     * Obtains a live JDBC Connection to the MySQL database.
     * Automatically attempts common passwords and seeds tables if needed.
     */
    public static Connection getConnection() throws SQLException {
        if (activePassword != null) {
            try {
                Connection conn = DriverManager.getConnection(JDBC_URL, DB_USER, activePassword);
                if (conn != null && !conn.isClosed()) {
                    return conn;
                }
            } catch (SQLException ignored) {
                activePassword = null;
            }
        }

        if (checkedAllPasswords && cachedFailure != null) {
            throw cachedFailure;
        }

        String[] candidatePasswords = new String[] {
            DB_PASSWORD, "", "root", "admin", "1234", "password", "root123", "mysql"
        };

        SQLException lastException = null;
        for (String pass : candidatePasswords) {
            try {
                Connection conn = DriverManager.getConnection(JDBC_URL, DB_USER, pass);
                if (conn != null && !conn.isClosed()) {
                    activePassword = pass;
                    if (!dbInitialized) {
                        ensureSchemaAndAccounts(conn);
                        dbInitialized = true;
                    }
                    return conn;
                }
            } catch (SQLException e) {
                lastException = e;
                // If database digital_od does not exist yet, try creating it via root server connection
                if (e.getErrorCode() == 1049) { // Unknown database
                    try (Connection serverConn = DriverManager.getConnection(SERVER_URL, DB_USER, pass);
                         Statement s = serverConn.createStatement()) {
                        s.executeUpdate("CREATE DATABASE IF NOT EXISTS " + DB_NAME + " CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
                        Connection conn = DriverManager.getConnection(JDBC_URL, DB_USER, pass);
                        activePassword = pass;
                        if (!dbInitialized) {
                            ensureSchemaAndAccounts(conn);
                            dbInitialized = true;
                        }
                        return conn;
                    } catch (Exception ignored) {
                    }
                }
            }
        }

        checkedAllPasswords = true;
        cachedFailure = (lastException != null) ? lastException : new SQLException("Could not connect to MySQL database at " + JDBC_URL);
        throw cachedFailure;
    }

    /**
     * Ensures necessary database tables, schema columns, and default accounts exist.
     */
    private static synchronized void ensureSchemaAndAccounts(Connection conn) {
        try (Statement stmt = conn.createStatement()) {
            // 1. Create users table
            stmt.executeUpdate("CREATE TABLE IF NOT EXISTS users (" +
                    "id INT AUTO_INCREMENT PRIMARY KEY, " +
                    "username VARCHAR(50) NOT NULL UNIQUE, " +
                    "password VARCHAR(100) NOT NULL, " +
                    "role VARCHAR(20) NOT NULL, " +
                    "roll_no VARCHAR(30) NOT NULL, " +
                    "full_name VARCHAR(100) NOT NULL, " +
                    "department VARCHAR(100) DEFAULT 'Computer Applications', " +
                    "course VARCHAR(50) DEFAULT 'MCA', " +
                    "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP" +
                    ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4");

            // 2. Create od_requests table
            stmt.executeUpdate("CREATE TABLE IF NOT EXISTS od_requests (" +
                    "id INT AUTO_INCREMENT PRIMARY KEY, " +
                    "student_username VARCHAR(50) NOT NULL, " +
                    "roll_no VARCHAR(30) NOT NULL, " +
                    "event_type VARCHAR(100) NOT NULL, " +
                    "event_name VARCHAR(200) NOT NULL, " +
                    "event_date DATE NOT NULL, " +
                    "from_date DATE, " +
                    "to_date DATE, " +
                    "days_count INT DEFAULT 1, " +
                    "reason TEXT NOT NULL, " +
                    "staff_status VARCHAR(30) DEFAULT 'Pending', " +
                    "hod_status VARCHAR(30) DEFAULT 'Pending', " +
                    "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP" +
                    ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4");

            // 3. Add any missing columns to existing od_requests table safely
            try {
                stmt.executeUpdate("ALTER TABLE od_requests ADD COLUMN from_date DATE");
            } catch (SQLException ignored) {}
            try {
                stmt.executeUpdate("ALTER TABLE od_requests ADD COLUMN to_date DATE");
            } catch (SQLException ignored) {}
            try {
                stmt.executeUpdate("ALTER TABLE od_requests ADD COLUMN days_count INT DEFAULT 1");
            } catch (SQLException ignored) {}
            try {
                stmt.executeUpdate("ALTER TABLE od_requests ADD COLUMN authorized_body VARCHAR(200)");
            } catch (SQLException ignored) {}

            // 4. Upsert mandatory default accounts (Student, Staff, HOD)
            String upsertUserSql = "INSERT INTO users (username, password, role, roll_no, full_name, department, course) " +
                    "VALUES (?, ?, ?, ?, ?, ?, ?) " +
                    "ON DUPLICATE KEY UPDATE password = VALUES(password), role = VALUES(role), " +
                    "roll_no = VALUES(roll_no), full_name = VALUES(full_name), department = VALUES(department), course = VALUES(course)";

            try (PreparedStatement ps = conn.prepareStatement(upsertUserSql)) {
                // studentjohn / 21mca015
                ps.setString(1, "studentjohn");
                ps.setString(2, "pass123");
                ps.setString(3, "student");
                ps.setString(4, "21MCA015");
                ps.setString(5, "John Doe");
                ps.setString(6, "Computer Applications");
                ps.setString(7, "MCA");
                ps.executeUpdate();

                ps.setString(1, "21mca015");
                ps.setString(2, "pass123");
                ps.setString(3, "student");
                ps.setString(4, "21MCA015");
                ps.setString(5, "John Doe");
                ps.setString(6, "Computer Applications");
                ps.setString(7, "MCA");
                ps.executeUpdate();

                // staffjacob
                ps.setString(1, "staffjacob");
                ps.setString(2, "jacob1234");
                ps.setString(3, "staff");
                ps.setString(4, "STF001");
                ps.setString(5, "Prof. Jacob Mathew");
                ps.setString(6, "Computer Applications");
                ps.setString(7, "MCA Faculty");
                ps.executeUpdate();

                // hodsmith
                ps.setString(1, "hodsmith");
                ps.setString(2, "hod1234");
                ps.setString(3, "hod");
                ps.setString(4, "HOD001");
                ps.setString(5, "Dr. Alan Smith");
                ps.setString(6, "Computer Applications");
                ps.setString(7, "Head of Department");
                ps.executeUpdate();

                // edwin21 (legacy student account)
                ps.setString(1, "edwin21");
                ps.setString(2, "pass123");
                ps.setString(3, "student");
                ps.setString(4, "21CS045");
                ps.setString(5, "Edwin Saji");
                ps.setString(6, "Computer Science");
                ps.setString(7, "B.Tech CSE");
                ps.executeUpdate();

                // aisha09 (legacy student account)
                ps.setString(1, "aisha09");
                ps.setString(2, "aisha2024");
                ps.setString(3, "student");
                ps.setString(4, "21CS046");
                ps.setString(5, "Aisha Khan");
                ps.setString(6, "Electronics");
                ps.setString(7, "B.Tech ECE");
                ps.executeUpdate();
            }

            System.out.println("[DBConnection] Schema validated and default accounts verified in MySQL.");
        } catch (SQLException e) {
            System.err.println("[DBConnection] Error during schema and account migration: " + e.getMessage());
        }
    }

    /**
     * Checks whether the MySQL database is currently reachable.
     */
    public static boolean isDatabaseAvailable() {
        try (Connection conn = getConnection()) {
            return conn != null && !conn.isClosed();
        } catch (Exception e) {
            return false;
        }
    }

    /**
     * Utility method to quietly close database resources.
     */
    public static void closeQuietly(AutoCloseable... closeables) {
        for (AutoCloseable c : closeables) {
            if (c != null) {
                try {
                    c.close();
                } catch (Exception ignored) {
                }
            }
        }
    }
}
