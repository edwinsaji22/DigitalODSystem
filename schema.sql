-- ============================================================
-- DIGITAL LEAVE / ON-DUTY (OD) APPLICATION SYSTEM
-- Academic Project Database Schema & Seed Data
-- ============================================================

CREATE DATABASE IF NOT EXISTS digital_od CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE digital_od;

-- ------------------------------------------------------------
-- 1. Table: users
-- Stores authentication credentials, roles, and profile information
-- ------------------------------------------------------------
DROP TABLE IF EXISTS od_requests;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL,              -- 'student', 'staff', 'hod'
    roll_no VARCHAR(30) NOT NULL,           -- Roll Number for Student, Staff ID for Staff/HOD
    full_name VARCHAR(100) NOT NULL,
    department VARCHAR(100) DEFAULT 'Computer Applications',
    course VARCHAR(50) DEFAULT 'MCA',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 2. Table: od_requests
-- Stores On-Duty applications submitted by students
-- ------------------------------------------------------------
CREATE TABLE od_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_username VARCHAR(50) NOT NULL,
    roll_no VARCHAR(30) NOT NULL,
    event_type VARCHAR(100) NOT NULL,        -- e.g., 'Technical Symposium', 'Paper Presentation'
    event_name VARCHAR(200) NOT NULL,
    event_date DATE NOT NULL,
    reason TEXT NOT NULL,
    staff_status VARCHAR(30) DEFAULT 'Pending',   -- 'Pending', 'Verified', 'Rejected'
    hod_status VARCHAR(30) DEFAULT 'Pending',     -- 'Pending', 'Approved', 'Rejected'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_student_username FOREIGN KEY (student_username) 
        REFERENCES users (username) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 3. Default Academic Accounts (Mandatory Test Accounts)
-- ------------------------------------------------------------
INSERT INTO users (username, password, role, roll_no, full_name, department, course) VALUES
('studentjohn', 'pass123', 'student', '21MCA015', 'John Doe', 'Computer Applications', 'MCA'),
('staffjacob', 'jacob1234', 'staff', 'STF001', 'Prof. Jacob Mathew', 'Computer Applications', 'Faculty Advisor'),
('hodsmith', 'hod1234', 'hod', 'HOD001', 'Dr. Alan Smith', 'Computer Applications', 'Head of Department'),
('edwin21', 'pass123', 'student', '21CS045', 'Edwin Saji', 'Computer Science', 'B.Tech CSE'),
('aisha09', 'aisha2024', 'student', '21CS046', 'Aisha Khan', 'Electronics', 'B.Tech ECE');

-- ------------------------------------------------------------
-- 4. Sample Pre-Populated OD Requests for Demonstration
-- ------------------------------------------------------------
INSERT INTO od_requests (student_username, roll_no, event_type, event_name, event_date, reason, staff_status, hod_status, created_at) VALUES
('studentjohn', '21MCA015', 'Technical Symposium', 'National TechFest 2026 - Hackathon', '2026-10-15', 'Selected as finalist in National Web & Mobile App Hackathon representing college.', 'Pending', 'Pending', '2026-10-01 09:30:00'),
('studentjohn', '21MCA015', 'Paper Presentation', 'IEEE International Student Conference', '2026-10-22', 'Presenting research paper on Decentralized Attendance and OD Automation Systems.', 'Verified', 'Pending', '2026-10-01 10:15:00');

-- Verification Query
SELECT 'Database schema and seed data created successfully.' AS status;
