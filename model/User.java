package model;

import java.io.Serializable;

/**
 * Phase 1: Core Application Setup & Design
 * User Model representing system actors: Student, Staff, and HOD.
 */
public class User implements Serializable {
    private static final long serialVersionUID = 1L;

    // Core Attributes
    private int id;
    private String username;
    private String password;
    private String role;           // "student", "staff", "hod" (case-insensitive)
    private String rollNo;         // Roll Number / Staff ID
    private String fullName;
    private String department;
    private String course;

    // Default Constructor
    public User() {
    }

    // Constructor with core Phase 1 fields
    public User(int id, String username, String password, String role, String rollNo) {
        this.id = id;
        this.username = username;
        this.password = password;
        this.role = role;
        this.rollNo = rollNo;
    }

    // Convenient constructor for registration/authentication
    public User(String username, String password, String role, String rollNo) {
        this(0, username, password, role, rollNo);
    }

    // Extended constructor for full profile compatibility
    public User(String username, String password, String fullName,
                String registerNumber, String role, String department, String course) {
        this.username = username;
        this.password = password;
        this.fullName = fullName;
        this.rollNo = registerNumber;
        this.role = role;
        this.department = department;
        this.course = course;
    }

    // Full constructor
    public User(int id, String username, String password, String role, String rollNo,
                String fullName, String department, String course) {
        this.id = id;
        this.username = username;
        this.password = password;
        this.role = role;
        this.rollNo = rollNo;
        this.fullName = fullName;
        this.department = department;
        this.course = course;
    }

    // ---------- Getters and Setters ----------

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }

    public String getRollNo() {
        return rollNo;
    }

    public void setRollNo(String rollNo) {
        this.rollNo = rollNo;
    }

    // Alias methods for backwards compatibility with legacy registerNumber
    public String getRegisterNumber() {
        return rollNo;
    }

    public void setRegisterNumber(String registerNumber) {
        this.rollNo = registerNumber;
    }

    public String getFullName() {
        return fullName != null ? fullName : username;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
    }

    public String getDepartment() {
        return department != null ? department : "General";
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public String getCourse() {
        return course;
    }

    public void setCourse(String course) {
        this.course = course;
    }

    // ---------- String-Handling Validation Methods (Phase 1) ----------

    public boolean isUsernameValid() {
        if (username == null) {
            return false;
        }
        String trimmed = username.trim();
        return !trimmed.isEmpty() && trimmed.length() >= 3 && trimmed.matches("^[a-zA-Z0-9_]+$");
    }

    public boolean isPasswordValid() {
        if (password == null) {
            return false;
        }
        String trimmed = password.trim();
        return trimmed.length() >= 6;
    }

    public boolean isRollNoValid() {
        if (rollNo == null) {
            return false;
        }
        return !rollNo.trim().isEmpty();
    }

    public boolean isFullNameValid() {
        if (fullName == null || fullName.trim().isEmpty()) {
            return true;
        }
        return fullName.trim().matches("^[a-zA-Z\\s.]+$");
    }

    public boolean isValidUser() {
        return isUsernameValid() && isPasswordValid();
    }

    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", username='" + username + '\'' +
                ", role='" + role + '\'' +
                ", rollNo='" + rollNo + '\'' +
                ", fullName='" + fullName + '\'' +
                ", department='" + department + '\'' +
                '}';
    }
}