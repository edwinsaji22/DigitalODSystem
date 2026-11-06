# Project-based Practical Report
## Digital Leave and On-Duty (OD) Application System

**Submitted in partial fulfilment of the requirements for the Master of Computer Applications (MCA)**

---

```
[ INSERT SCREENSHOT: Institutional Cover Page / Department Seal Placeholder - Half Page Size ]
```

---

## Table of Contents

1. **Title of the Project**
2. **Introduction**
3. **Objectives of the Project**
   - 3.1 Main Objective
   - 3.2 Specific Objectives (1 to 12)
4. **Scope of the Project**
   - 4.1 Student / Applicant Module
   - 4.2 Staff Verification Module
   - 4.3 Head of Department (HOD) Approval Module
   - 4.4 System Scope Boundaries and Technical Limitations
5. **Software and Hardware Specifications**
   - 5.1 Environment Specifications Table
   - 5.2 Runtime and Server Configuration
   - 5.3 Hardware Prerequisites
6. **Workflow of the Project**
   - 6.1 End-to-End Processing Flow
   - 6.2 Life-Cycle State Transitions of an OD Request
   - 6.3 Request Flow Narrative
7. **Modules of the Project (Phase-Wise Design & Execution)**
   - 7.1 Phase 1: Core Application Setup and Data Model Definition
   - 7.2 Phase 2: Structured Programming, Layered Architecture, and Custom Exceptions
   - 7.3 Phase 3: Web Interface Design and Client-Side Validation
   - 7.4 Phase 4: Server-Side Request Handling, JDBC Persistence, and Session Management
8. **Source Code (Functional Code Structure)**
   - 8.1 Database Connection Factory (`DBConnection.java`)
   - 8.2 Custom Domain Exception (`InvalidInputException.java`)
   - 8.3 Core Processing Controller (`ApplyODServlet.java` - `doPost` Snippet)
   - 8.4 Client-Side Business Logic Enforcement (`od_validation.js`)
9. **Features of the Project**
   - 9.1 Real-Time Dashboard Metrics
   - 9.2 Automated Institutional Policy Enforcement
   - 9.3 Role-Based Access Control and Granular Authorization
   - 9.4 Temporal Overlap and Duplicate Prevention
10. **Requirements Analysis**
    - 10.1 Functional Requirements Matrix (FR-01 to FR-18)
    - 10.2 Non-Functional System Requirements
    - 10.3 Assumptions and Operating Constraints
11. **Use Case Descriptions**
    - 11.1 UC-01: User Authentication and Role Dispatching
    - 11.2 UC-02: Student OD Application Submission
    - 11.3 UC-03: Staff Review and Verification
    - 11.4 UC-04: Head of Department (HOD) Final Sanction
    - 11.5 UC-05: Historical Audit and Quota Inspection
12. **System Architecture and Database Design**
    - 12.1 Model-View-Controller (MVC) Architectural Pattern
    - 12.2 Relational Database Schema Design
    - 12.3 Table Definitions and Field Constraints
    - 12.4 Entity-Relationship Mapping
    - 12.5 Trace of an HTTP Request Pipeline
13. **Input Validation and Software Testing**
    - 13.1 Tiered Validation Strategy: Browser vs. Server
    - 13.2 Error Propagation and User Feedback
    - 13.3 Test Strategy and Execution Environment
    - 13.4 Comprehensive Functional Test Case Suite (TC-01 to TC-28)
14. **Security Considerations and Known Limitations**
    - 14.1 Countermeasures Against SQL Injection Attacks
    - 14.2 Session Management and State Isolation
    - 14.3 Cross-Site Scripting (XSS) and Input Sanitization
    - 14.4 Architectural Gaps and Production Hardening Needs
15. **Future Enhancements**
16. **Conclusion**

---

```
[ INSERT SCREENSHOT: System Dashboard Overview / Hero Banner - Full Width Half Page Size ]
```

---

## 1. Title of the Project

### **Digital Leave and On-Duty (OD) Application System**
**Sub-title:** A Role-Based Multi-Tier Web Application for Academic Leave Processing and Policy Compliance Enforcement Utilizing Java Servlets, JSP, JDBC, and MySQL.

---

## 2. Introduction

In modern tertiary educational institutions, student participation in co-curricular activities, technical symposia, hackathons, sports tournaments, and industrial internships forms a vital component of holistic professional training. When students represent their college or university at such sanctioned events, academic regulations permit them to claim "On-Duty" (OD) status. This status excuses their absence from scheduled classroom lectures and laboratory sessions, ensuring that their official attendance records remain intact.

However, in the vast majority of institutions, the administrative framework managing leave and On-Duty clearances remains heavily manual, paper-driven, and structurally inefficient. The conventional procedure requires a student to obtain a physical paper form, fill in multiple redundant personal details, attach supporting documents, and physically track down several faculty members across sprawling campus facilities. The applicant must secure signatures sequentially from the event faculty coordinator, class mentor, course teachers, and finally the Head of the Department (HOD). 

```
[ INSERT SCREENSHOT: Legacy Paper Form vs. Digital Interface Comparison - Half Page Size ]
```

This legacy manual workflow suffers from numerous operational and administrative vulnerabilities:

1. **Severe Latency and Lost Documentation:** Physical forms are routinely misplaced on faculty desks, damaged, or delayed beyond institutional deadlines because students cannot locate traveling or busy staff members.
2. **Absence of Centralized Policy Enforcement:** Academic bylaws dictate strict thresholds—such as submitting an application within a fixed time window post-event and adhering to a semester-wide cap on cumulative OD days. In paper-based workflows, faculty signatories cannot verify whether a student has already exceeded their semester quota without cross-referencing physical departmental logbooks, which is rarely done in real time.
3. **Vulnerability to Forgery and Tampering:** Manual signatures on paper slips are trivial to forge, and post-approval modifications to approved dates or event descriptions frequently go undetected.
4. **Attendance Reconciliation Discrepancies:** Paper slips submitted weeks after an event force ERP administrators and attendance clerks to perform manual, retroactive database updates, leading to attendance disputes during semester examination hall-ticket generation.

The **Digital Leave and On-Duty (OD) Application System** was conceptualized, architected, and engineered to eliminate these friction points. By migrating the entire workflow to a centralized, role-based web application, the system introduces deterministic rule enforcement, transparent status tracking, and strict accountability. 

Built using core Enterprise Java technologies—specifically **Java Servlets, JavaServer Pages (JSP), Java Database Connectivity (JDBC)**, and a relational **MySQL** database running on an **Apache Tomcat 9** servlet container—the application operates on a strict Model-View-Controller (MVC) paradigm. The system guarantees that no student can apply for retroactive OD beyond the institutional deadline, prevents multiple bookings on overlapping calendar dates, and rigorously caps aggregate duty days at the institutional limit per semester. By automating multi-tier authorization (Student $\rightarrow$ Staff $\rightarrow$ HOD), the platform reduces institutional processing latency from days to seconds while establishing an immutable electronic audit trail.

---

## 3. Objectives of the Project

### 3.1 Main Objective
The primary objective of this project is to design, develop, and deploy a secure, robust, and responsive web-based platform that digitizes the collegiate On-Duty and leave application lifecycle. The system aims to replace physical paper forms with a structured, automated multi-tier approval pipeline (Student to Staff to Head of Department), while systematically enforcing institutional academic bylaws, quota constraints, and temporal deadlines directly in software.

```
[ INSERT SCREENSHOT: System High-Level Objective Workflow Diagram - Half Page Size ]
```

### 3.2 Specific Objectives

1. **Multi-Tier Role-Based Routing:**  
   To establish a clean, sequential approval workflow where an application submitted by an authenticated student is routed first to their assigned Staff Advisor for document and attendance verification, and subsequently forwarded to the Head of Department (HOD) for executive institutional sanction.

2. **Automated Enforcement of the 3-Day Submission Rule:**  
   To eliminate retroactive and fabricated duty claims by implementing strict programmatic date validation that prevents any student from submitting an OD application if more than three calendar days have elapsed since the conclusion of the event (`toDate`).

3. **Strict Semester Quota Management (15-Day Cap):**  
   To maintain institutional academic rigor by programmatically tracking cumulative approved and pending duty days per student, automatically blocking any new submission that would cause the student to exceed the maximum allowable semester ceiling of 15 working days.

4. **Temporal Overlap and Duplicate Prevention:**  
   To safeguard attendance integrity by evaluating prospective application dates against historical records in the database, rejecting any request that overlaps with an already approved or pending OD tenure for the same student.

5. **Category-Specific Duration Constraints:**  
   To enforce institutional bylaws regarding event classifications, ensuring that maximum allowable duty days correspond directly to the event category (e.g., maximum 2 days for recruitment drives, 3 days for technical symposia, 5 days for sports and hackathons, and 7 days for industrial training).

6. **Prior Authorization and Endorsement Capture:**  
   To ensure institutional validity by requiring students to specify the endorsing campus authority, sponsoring student club, or faculty coordinator along with event metadata before an application can enter the evaluation queue.

7. **Secure, Role-Gated Session Management:**  
   To implement server-side `HttpSession` tracking that encapsulates user identity, role privileges (`student`, `staff`, `hod`), and institutional identifiers, preventing unauthorized privilege escalation, URL manipulation, or cross-role resource tampering.

8. **Defensive Database Engineering and SQL Injection Immunity:**  
   To construct a clean persistence layer using native JDBC `PreparedStatement` parameterized queries across all database read and write operations, entirely preventing SQL injection vectors without relying on heavy third-party ORM frameworks.

9. **Two-Tier Validation Architecture:**  
   To provide immediate, client-side feedback through modern Vanilla JavaScript event interception while duplicating and strictly re-evaluating all domain validation rules on the server inside Java Servlets, preventing bypass via disabled client scripts.

10. **Granular Rejection Feedback and Audit Transparency:**  
    To eliminate student uncertainty by recording explicit justification comments whenever an application is marked as rejected by Staff or HOD, rendering this feedback visible in real time on the student’s personal dashboard.

11. **Real-Time Analytical Dashboard Metrics:**  
    To compute and display live summary counters across all user dashboards, enabling students to track their remaining quota balance, staff to review their pending verification queues, and HODs to monitor departmental engagement levels.

12. **Lightweight, Native Technology Stack:**  
    To build an enterprise-grade academic system using pure Java EE fundamentals (JSP, Servlets, JDBC) without the overhead, configuration complexity, or memory footprint of external enterprise frameworks like Spring Boot, demonstrating mastery of fundamental web architecture.

---

## 4. Scope of the Project

The scope of the Digital Leave and OD Application System encompasses the primary administrative interactions required to manage, verify, approve, and audit student On-Duty leaves within an academic department. The system segregates functionalities into discrete role boundaries.

```
[ INSERT SCREENSHOT: Role-Based Dashboard Navigation Matrix - Half Page Size ]
```

### 4.1 Student / Applicant Module
The student component provides authenticated applicants with full visibility and control over their leave portfolio:
* **Account Authentication:** Secure credential verification establishing an active `HttpSession`.
* **Application Composition:** An interactive web form allowing students to submit new OD requests by supplying the event category, title, endorsing body, starting date, ending date, and detailed explanatory justification.
* **Client-Side Live Pre-Checks:** Instant calculation of total requested days, dynamic comparison against the 3-day post-event deadline, and client-side quota warnings.
* **Personal Analytics Dashboard:** A dedicated interface displaying key personal metrics, including total applications submitted, pending verifications, approved ODs, rejected requests, and remaining semester quota out of 15 days.
* **Historical Audit Table:** A complete, chronological table of all past applications displaying unique application IDs, event details, date spans, duration, current staff status, final HOD status, and reviewer remarks.

### 4.2 Staff Verification Module
The staff interface is designed for faculty mentors and class advisors responsible for first-level due diligence:
* **Departmental Verification Queue:** A filtered view displaying all student OD requests originating within the staff member’s academic department that currently have a `Pending` staff status.
* **Evidence and Context Review:** Full access to examine student credentials (Roll Number, Full Name), event metadata, endorsing club/coordinator, date range, and submitted justification.
* **Deterministic Verification Actions:** Single-click capability to mark an application as `Verified` (which elevates it to the HOD's executive queue) or `Rejected` (which terminates the application workflow).
* **Feedback Attribution:** Ability to input mandatory administrative comments explaining the rationale behind any rejection, providing actionable feedback to the applicant.

### 4.3 Head of Department (HOD) Approval Module
The HOD module serves as the final executive clearance tier for institutional attendance records:
* **Executive Pending Queue:** Displays only those OD applications that have successfully passed first-tier Staff Verification (`staff_status = 'Verified'` and `hod_status = 'Pending'`).
* **Department-Wide Oversight:** High-level metrics showing the overall number of students on duty, cumulative departmental days granted, and pending executive requests.
* **Final Approval Actions:** Authority to grant final `Approved` status or issue an executive `Rejected` decision. Once approved by the HOD, the leave record is considered official and can be reconciled against the central attendance register.

### 4.4 System Scope Boundaries and Technical Limitations
To maintain a focused development scope within the parameters of an advanced practical software engineering project, the following explicit boundaries are established:
* **Single Institution / Department Focus:** The current database schema is optimized for a departmental structure (e.g., Computer Applications) and does not implement a multi-tenant university deployment across disjoint sub-campuses.
* **No Direct Biometric Hardware Bridge:** The system generates and stores approved OD records in MySQL for attendance reconciliation but does not directly pulse network-attached physical biometric fingerprint or facial-recognition hardware turnstiles.
* **Absence of External SMTP Server Integration:** Status updates are communicated synchronously through the web interface and persistent database polling rather than asynchronous transactional email or SMS notification services.
* **Manual Document Verification:** While students declare their endorsing body and coordinator, the system does not process OCR or binary PDF file uploads for physical certificates, relying instead on textual declaration and physical verification during mentor review.

---

## 5. Software and Hardware Specifications

The application is engineered as a decoupled, multi-tier web solution designed to run on cross-platform runtime environments supporting the Java Virtual Machine and standard relational database servers.

### 5.1 Environment Specifications Table

| Category | Component / Tool | Version / Standard | Functional Purpose in System |
| :--- | :--- | :--- | :--- |
| **Operating System** | Microsoft Windows 11 / Linux Ubuntu 22.04 LTS | x64 Architecture | Primary development and production hosting environment. |
| **Programming Language** | Java Standard Edition (Java SE) | JDK 17 / JDK 21 LTS | Core business logic, domain entities, custom exception classes, and compilation. |
| **Server-Side Engine** | Java Servlets | Servlet API 4.0 (JSR 369) | HTTP request handling, controller dispatching, session control, and rule validation. |
| **Presentation Engine** | JavaServer Pages (JSP) | JSP 2.3 / JSTL 1.2 | Dynamic view rendering, role-gated UI generation, and server-side model attribute display. |
| **Web Server / Servlet Container**| Apache Tomcat | Version 9.0.x | Standalone HTTP web server and compliant servlet/JSP container. |
| **Database Management System** | MySQL Community Server | Version 8.0.x | Relational persistent data store for user records, roles, quotas, and OD requests. |
| **Database Driver** | MySQL Connector/J | Version 8.0.33+ | Official JDBC Type-4 driver enabling native binary network protocol communication. |
| **Persistence Mechanism** | Java Database Connectivity (JDBC) | Native JDBC API | Direct SQL execution using `PreparedStatement` and transactional connection management. |
| **Client-Side Structure** | HTML5 | W3C Recommendation | Semantic structural markup of dashboards, forms, tables, and modal dialogs. |
| **Styling & User Interface** | CSS3 (Modern Light Theme) | W3C Standard | Bespoke, responsive layout styling using CSS Flexbox, Grid, custom properties, and micro-transitions. |
| **Client-Side Scripting** | Vanilla JavaScript | ECMAScript 2021 (ES12) | Asynchronous form interception, dynamic date difference calculations, and client pre-validation. |
| **Build & Packaging Tool** | Apache Ant / Integrated IDE Build | Native WAR Packaging | Compilation of Java source files into `.class` bytecode and assembly into deployment WAR. |

```
[ INSERT SCREENSHOT: Apache Tomcat Web Manager & Deployment State - Half Page Size ]
```

### 5.2 Runtime and Server Configuration
The system is deployed on Apache Tomcat 9 listening on default TCP port `8080`. The project context path is established as `/DigitalODSystem`. Database connection configuration parameters are encapsulated inside the `service.DBConnection` utility class, referencing the connection string:
```
jdbc:mysql://localhost:3306/digital_od?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC
```
The database user credentials are parameterized to isolate environment-specific secrets from public version control.

### 5.3 Hardware Prerequisites
* **Processor:** Intel Core i5 / AMD Ryzen 5 or higher (minimum dual-core 2.4 GHz).
* **Random Access Memory (RAM):** 8 GB minimum (16 GB recommended for concurrent hosting of Tomcat, MySQL Daemon, and development IDE).
* **Storage:** 500 MB free solid-state drive (SSD) storage for project binaries, logging buffers, and database tablespaces.
* **Client Device:** Any standard computing device (desktop, laptop, tablet) equipped with an HTML5-compliant web browser (Google Chrome 110+, Mozilla Firefox 105+, Microsoft Edge 110+).

---

## 6. Workflow of the Project

The operational lifecycle of an On-Duty request progresses through a strictly controlled pipeline governed by finite state machine principles. Every transition requires authenticated authorization and is committed atomically to the MySQL database.

```
[ INSERT SCREENSHOT: Complete End-to-End System Workflow Sequence Diagram - Full Page Size ]
```

### 6.1 End-to-End Processing Flow

1. **System Initialization:**  
   The administrator launches Apache Tomcat 9 and verifies that the MySQL database service `digital_od` is online. The relational tables (`users` and `od_requests`) are verified for schema integrity.

2. **User Authentication:**  
   The user navigates to the application root URL (`/login.html`). The user submits their unique username and password. `LoginServlet` intercepts the POST request, hashes/verifies the credentials against the `users` table via JDBC, extracts the user's role (`student`, `staff`, `hod`), registers their credentials into a newly initialized `HttpSession`, and issues an HTTP 302 redirect to the appropriate role dashboard.

3. **Application Drafting and Client Validation:**  
   The student accesses `student_dashboard.jsp` and clicks "Apply for On-Duty". In the modal form, the student selects the event category, specifies the event title, inputs the endorsing coordinator/club, and picks the starting (`fromDate`) and ending (`toDate`) dates. A client-side JavaScript listener intercepts input changes, calculating the total duration:
   $$\text{Duration} = (\text{toDate} - \text{fromDate}) + 1$$
   If $\text{toDate} < \text{fromDate}$, or if the event ended more than 3 days prior ($\text{LocalDate.now()} - \text{toDate} > 3$), an immediate visual alert prevents form submission.

4. **Server-Side Interception and Business Rule Enforcement:**  
   Upon submission, `ApplyODServlet` intercepts the request via HTTP POST. It retrieves the active `HttpSession` to confirm the student’s identity. The servlet delegates validation to `ODServiceImpl`, which systematically executes the following checks:
   * **Rule 1 (Field Completeness):** Verifies that mandatory parameters are non-null and non-empty.
   * **Rule 2 (Date Chronology):** Asserts that $\text{toDate} \ge \text{fromDate}$.
   * **Rule 3 (3-Day Timeline Limit):** Computes `ChronoUnit.DAYS.between(toDate, LocalDate.now())`. If greater than 3, throws `InvalidInputException`.
   * **Rule 4 (Category Duration Cap):** Checks whether the requested duration exceeds the predefined ceiling for the selected event classification.
   * **Rule 5 (Date Overlap Check):** Queries existing applications for the student to ensure the prospective range $[\text{fromDate}, \text{toDate}]$ does not overlap with any existing approved or pending tenure.
   * **Rule 6 (15-Day Semester Quota):** Queries the database for the student's cumulative consumed days. If $\text{Used Days} + \text{Requested Days} > 15$, throws `InvalidInputException`.

5. **Persistence and First-Stage Enqueueing:**  
   If all validation barriers pass, the request is inserted into the `od_requests` table with initial states: `staff_status = 'Pending'` and `hod_status = 'Pending'`. The student is redirected to their dashboard with a `status=success` query parameter.

6. **First-Tier Staff Verification:**  
   The staff advisor logs into `staff_dashboard.jsp`. The system queries MySQL for all applications belonging to the department with `staff_status = 'Pending'`. The staff member reviews the student’s reason, dates, and endorsement. The staff member selects either "Verify" or "Reject". `UpdateODStatusServlet` processes the action:
   * If verified: `staff_status` updates to `'Verified'`. The request now becomes visible to the HOD.
   * If rejected: `staff_status` updates to `'Rejected'`. The workflow terminates, and the record remains visible on the student's dashboard marked as rejected.

7. **Second-Tier Executive HOD Sanction:**  
   The Head of Department accesses `hod_dashboard.jsp`. The view retrieves applications where `staff_status = 'Verified'` and `hod_status = 'Pending'`. The HOD evaluates the final request and selects "Approve" or "Reject":
   * If approved: `hod_status` updates to `'Approved'`. The application is fully sanctioned, and the requested days are permanently debited against the student’s 15-day semester quota.
   * If rejected: `hod_status` updates to `'Rejected'`.

8. **Session Termination (Logout):**  
   The user clicks "Sign Out". `LogoutServlet` captures the request, explicitly invalidates the server-side `HttpSession` via `session.invalidate()`, flushes client caching headers, and redirects the browser back to `login.html`.

```
[ INSERT SCREENSHOT: Lifecycle State Transition Diagram of an OD Request - Half Page Size ]
```

---

## 7. Modules of the Project (Phase-Wise Explanation)

The engineering process was executed across four structured development phases following professional software engineering methodologies.

### 7.1 Phase 1: Core Application Setup and Data Model Definition
Phase 1 established the core structural foundation, domain entities, and database architecture.

```
[ INSERT SCREENSHOT: Java Entity Class Diagram (User and ODRequest POJOs) - Half Page Size ]
```

* **Relational Schema Engineering:** The initial step involved authoring `schema.sql` to define the relational data model in MySQL. Two primary entities were created: `users` (encapsulating authentication credentials, user roles, roll numbers, and academic departments) and `od_requests` (recording the student’s username, roll number, event categorization, dates, requested duration, institutional justification, and approval states).
* **Plain Old Java Object (POJO) Construction:** Domain models were authored in the `model` package to mirror the database tables:
  * `User.java`: Encapsulates user profile data, credential attributes, and role designations (`student`, `staff`, `hod`). Includes full constructor overloads, accessors, mutators, and serialization mechanics.
  * `ODRequest.java`: Represents an individual application instance. Encapsulates properties such as `id`, `studentUsername`, `rollNo`, `eventType`, `eventName`, `authorizedBody`, `fromDate`, `toDate`, `daysCount`, `reason`, `staffStatus`, and `hodStatus`. Helper utility methods such as `isFullyApproved()` and `isAnyRejected()` were implemented to simplify downstream evaluation.

### 7.2 Phase 2: Structured Programming, Layered Architecture, and Custom Exceptions
Phase 2 established the modular architecture of the codebase, enforcing strict separation of concerns through an enterprise multi-layer structure.

* **Layered Package Decomposition:**
  * `model`: Holds domain entities.
  * `service`: Houses business logic interfaces (`AuthService`, `ODService`) and concrete implementations (`AuthServiceImpl`, `ODServiceImpl`).
  * `controller`: Contains HTTP Servlets handling client request-response cycles.
  * `exception`: Encapsulates domain-specific application exceptions.
* **Custom Exception Architecture:** Rather than propagating raw runtime or SQL exceptions to the user, an explicit domain exception framework was designed. The class `InvalidInputException.java` extends `java.lang.Exception`. It intercepts validation breaches (such as deadline violations, quota exceedances, and date overlaps), encapsulating meaningful, user-readable diagnostic messages that travel up the call stack to the controller layer.

### 7.3 Phase 3: Web Interface Design and Client-Side Validation
Phase 3 focused on creating an intuitive, accessible, and responsive user experience utilizing semantic HTML5, modern CSS3, and JavaScript.

```
[ INSERT SCREENSHOT: Clean Light-Themed Student Dashboard Interface - Half Page Size ]
```

* **Modern Light-Theme User Interface:** In contrast to cluttered legacy portals, a clean, modern aesthetic was engineered using CSS variables, card layouts, subtle box shadows, and responsive grid structures. Dynamic state badges indicate status at a glance: amber for `Pending`, emerald green for `Verified`/`Approved`, and crimson for `Rejected`.
* **Client-Side Validation (`od_validation.js`):** Client-side scripts intercept form submissions to perform instantaneous mathematical and logical pre-checks:
  * Verifies non-empty input for all fields.
  * Asserts that `toDate` is chronologically equal to or after `fromDate`.
  * Computes the difference between `toDate` and current system time, blocking requests that violate the 3-day post-event deadline.
  * Evaluates duration against the remaining quota balance, preventing pointless network roundtrips.

### 7.4 Phase 4: Server-Side Request Handling, JDBC Persistence, and Session Management
Phase 4 tied the front-end interface to backend business logic and database persistence.

* **Servlet Controllers:** Specialized HttpServlet subclasses were engineered:
  * `LoginServlet.java`: Manages credential validation, role extraction, and session creation.
  * `ApplyODServlet.java`: Handles new OD submissions, triggering comprehensive server-side policy validation.
  * `UpdateODStatusServlet.java`: Gated exclusively to Staff and HOD roles, handling state transitions.
  * `LogoutServlet.java`: Manages session invalidation and memory cleanup.
* **Robust JDBC Connectivity (`DBConnection.java`):** A centralized connection factory managing JDBC drivers, establishing thread-safe SQL connections, and maintaining graceful fallback behavior.
* **HttpSession Lifecycle Control:** Server-side sessions ensure that user data is tied to secure cookies (`JSESSIONID`). Authorization filters verify that students cannot access staff endpoints, and staff cannot access executive HOD functions.

---

## 8. Source Code (Functional Code Structure)

The following excerpts demonstrate key architectural components of the application. These represent functional structural highlights rather than exhaustive source listings.

### 8.1 Database Connection Factory (`service/DBConnection.java`)
This class provides centralized database connectivity using the JDBC `DriverManager` and encapsulates connection error handling.

```java
package service;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DBConnection {
    private static final String URL = "jdbc:mysql://localhost:3306/digital_od?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC";
    private static final String USER = "root";
    private static final String PASSWORD = "password123"; // Configured per environment

    static {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            System.err.println("CRITICAL: MySQL JDBC Driver not found in classpath: " + e.getMessage());
        }
    }

    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }
}
```

### 8.2 Custom Domain Exception (`exception/InvalidInputException.java`)
This checked exception encapsulates violations of academic policies, invalid dates, and quota overages.

```java
package exception;

public class InvalidInputException extends Exception {
    private static final long serialVersionUID = 1L;

    public InvalidInputException(String message) {
        super(message);
    }

    public InvalidInputException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

### 8.3 Core Processing Controller (`controller/ApplyODServlet.java` - `doPost` Snippet)
This snippet shows request interception, session identity verification, timeline constraint evaluation, and service delegation.

```java
package controller;

import exception.InvalidInputException;
import model.ODRequest;
import service.ODService;
import service.ODServiceImpl;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.IOException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

@WebServlet("/applyODServlet")
public class ApplyODServlet extends HttpServlet {
    private final ODService odService = new ODServiceImpl();

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        request.setCharacterEncoding("UTF-8");

        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("loggedInUser") == null) {
            response.sendRedirect("login.html?unauthorized=1");
            return;
        }

        String username = (String) session.getAttribute("loggedInUser");
        String rollNo = (String) session.getAttribute("rollNo");
        String eventType = request.getParameter("eventType");
        String eventName = request.getParameter("eventName");
        String authorizedBody = request.getParameter("authorizedBody");
        String fromDateStr = request.getParameter("fromDate");
        String toDateStr = request.getParameter("toDate");
        String reason = request.getParameter("reason");

        try {
            LocalDate fromDate = LocalDate.parse(fromDateStr.trim());
            LocalDate toDate = LocalDate.parse(toDateStr.trim());

            // Enforce Chronological Date Validity
            if (toDate.isBefore(fromDate)) {
                throw new InvalidInputException("To Date cannot be earlier than From Date.");
            }

            // Enforce 3-Day Submission Deadline Rule
            long daysPassed = ChronoUnit.DAYS.between(toDate, LocalDate.now());
            if (daysPassed > 3) {
                throw new InvalidInputException("Application rejected: Must be submitted within 3 days of event completion.");
            }

            int daysCount = (int) ChronoUnit.DAYS.between(fromDate, toDate) + 1;

            ODRequest od = new ODRequest(username, rollNo, eventType, eventName, 
                                         authorizedBody, fromDateStr, toDateStr, daysCount, reason);

            // Delegate business rule checks (quota, overlap, category) and persistence to service
            odService.applyOD(od);
            response.sendRedirect("student_dashboard.jsp?status=success");

        } catch (InvalidInputException e) {
            String errorMsg = URLEncoder.encode(e.getMessage(), StandardCharsets.UTF_8);
            response.sendRedirect("student_dashboard.jsp?status=error&msg=" + errorMsg);
        } catch (Exception e) {
            response.sendRedirect("student_dashboard.jsp?status=error&msg=Internal+Server+Error");
        }
    }
}
```

### 8.4 Client-Side Business Logic Enforcement (`js/od_validation.js`)
This script validates input constraints in the browser before the form is transmitted to the server.

```javascript
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("odApplicationForm");
    if (!form) return;

    form.addEventListener("submit", (event) => {
        const fromDateVal = document.getElementById("fromDate").value;
        const toDateVal = document.getElementById("toDate").value;
        const errorContainer = document.getElementById("clientErrorBox");

        errorContainer.textContent = "";
        errorContainer.style.display = "none";

        if (!fromDateVal || !toDateVal) {
            showError("Please specify both start and end dates.");
            event.preventDefault();
            return;
        }

        const fromDate = new Date(fromDateVal);
        const toDate = new Date(toDateVal);
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        // 1. Date Chronology Check
        if (toDate < fromDate) {
            showError("Invalid Date Range: 'To Date' cannot precede 'From Date'.");
            event.preventDefault();
            return;
        }

        // 2. Strict 3-Day Timeline Calculation
        const diffTime = today - toDate;
        const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
        if (diffDays > 3) {
            showError("Policy Violation: Applications must be submitted within 3 days of event completion.");
            event.preventDefault();
            return;
        }
    });

    function showError(msg) {
        const errorContainer = document.getElementById("clientErrorBox");
        errorContainer.textContent = msg;
        errorContainer.style.display = "block";
    }
});
```

---

## 9. Features of the Project

The application delivers a focused set of features designed to replace manual processes with reliable, auditable digital workflows.

```
[ INSERT SCREENSHOT: Analytics Dashboard Cards & Quota Visualization - Half Page Size ]
```

### 9.1 Real-Time Dashboard Metrics
Upon authentication, each user receives a role-tailored dashboard presenting key metrics:
* **Student Dashboard:** Displays four live stat cards—Total Applications, Approved Days, Pending In-Review Applications, and **Remaining Semester Quota** (calculated dynamically as $15 - \text{Cumulative Approved Days}$).
* **Staff Dashboard:** Highlights the count of actionable requests awaiting departmental verification, alongside a summary of processed reviews.
* **HOD Dashboard:** Features department-wide summaries, showcasing total active students on sanctioned duty, overall approved attendance days, and pending executive clearances.

### 9.2 Automated Institutional Policy Enforcement
The system's core value lies in its deterministic execution of academic bylaws:
* **The 3-Day Rule:** The system strictly rejects retroactive leave requests where more than three calendar days have elapsed between the conclusion of the event (`toDate`) and the submission timestamp. This eliminates post-hoc leave manufacturing.
* **The 15-Day Semester Ceiling:** The system enforces an absolute cap of 15 duty days per student per semester. When an application is submitted, the engine tallies the student's existing approved tenure and calculates whether the new requested days will breach this limit. If breached, the application is blocked immediately.
* **Category Duration Bounds:** Institutional caps based on event categories are enforced automatically (e.g., maximum 3 days for symposia, 5 days for hackathons/sports, 7 days for industrial training).

### 9.3 Role-Based Access Control and Granular Authorization
Security is integrated directly into the request routing pipeline. The application maintains clear role boundaries:
* A `student` cannot view other students' applications or access review endpoints.
* A `staff` advisor can verify requests originating within their department but cannot grant final institutional approval.
* An `HOD` has ultimate authority to issue official approval or rejection, and cannot review requests until staff verification has completed.
* URL tampering (such as a student directly invoking `UpdateODStatusServlet`) is blocked by server-side role inspections that invalidate the request and redirect to an unauthorized access warning page.

### 9.4 Temporal Overlap and Duplicate Prevention
The service layer examines every submitted date range against existing records for the student. If an applicant has an existing pending or approved OD spanning October 12 to October 14, any new application overlapping with those dates is rejected, preventing accidental or deliberate double-booking.

---

## 10. Requirements Analysis

### 10.1 Functional Requirements Matrix

```
[ INSERT SCREENSHOT: Traceability Matrix / Requirements Flowchart - Half Page Size ]
```

| Identifier | Requirement Statement | Primary Actor | Priority |
| :--- | :--- | :--- | :--- |
| **FR-01** | The system shall authenticate users using unique usernames and credentials, validating against stored profiles in MySQL. | Student, Staff, HOD | High |
| **FR-02** | The system shall determine user roles (`student`, `staff`, `hod`) and establish an isolated, secure `HttpSession`. | All Actors | High |
| **FR-03** | The system shall provide an application form for students to input event categories, titles, endorsing coordinators, and date spans. | Student | High |
| **FR-04** | The system shall compute total requested working days as `(toDate - fromDate) + 1`. | System / Controller | High |
| **FR-05** | The system shall reject submissions where `toDate` is chronologically earlier than `fromDate`. | System / Service | High |
| **FR-06** | The system shall reject applications submitted more than 3 days after event completion (`LocalDate.now() - toDate > 3`). | System / Service | High |
| **FR-07** | The system shall track cumulative duty days per student and block submissions exceeding the 15-day semester quota. | System / Service | High |
| **FR-08** | The system shall reject applications with date spans that overlap with existing pending or approved requests for the student. | System / Service | High |
| **FR-09** | The system shall restrict requested durations according to category-specific ceilings. | System / Service | Medium |
| **FR-10** | The system shall store new applications with initial states of `staff_status = 'Pending'` and `hod_status = 'Pending'`. | System / DAO | High |
| **FR-11** | The system shall display a real-time metrics dashboard to students showing application counts and remaining quota. | Student | High |
| **FR-12** | The system shall render a verification queue for staff showing pending applications from their department. | Staff | High |
| **FR-13** | The system shall enable staff to update an application's status to `Verified` or `Rejected` with explanatory remarks. | Staff | High |
| **FR-14** | The system shall render an executive queue for HODs showing requests verified by staff. | HOD | High |
| **FR-15** | The system shall enable HODs to record final `Approved` or `Rejected` status decisions. | HOD | High |
| **FR-16** | The system shall maintain an immutable historical audit table accessible to students showing all past applications and remarks. | Student | Medium |
| **FR-17** | The system shall restrict administrative review servlets to authenticated users with proper role authorization. | System / Security | High |
| **FR-18** | The system shall invalidate the `HttpSession` and clear caching headers upon user logout. | All Actors | High |

### 10.2 Non-Functional System Requirements

1. **Usability and User Experience:**  
   The interface uses a clean, light-themed responsive design. Form controls provide immediate visual validation messages adjacent to inputs, avoiding confusing generic error pages.
2. **Maintainability and Modularity:**  
   The application strictly adheres to the MVC architectural pattern. Database operations are decoupled into data access services, controller servlets manage routing, and JSP pages handle presentation. This ensures modifications to business policies (e.g., altering quota limits) require changes only in the service implementation.
3. **Data Integrity and Consistency:**  
   Transactional relational updates use foreign key constraints with cascading rules between `users` and `od_requests`. All SQL queries use parameter placeholders to eliminate malformed syntax risks.
4. **Application Security:**  
   Role-based authorization gates all protected endpoints. Passwords are handled through parameterized queries to eliminate SQL injection vulnerabilities. Sessions are managed via secure, transient HTTP cookies with explicit timeout policies.
5. **Portability and Standards Compliance:**  
   Developed using pure Java EE specifications (Servlet 4.0, JSP 2.3), the project builds into a standard Web Application Archive (WAR) deployable on any compliant servlet container across Windows, Linux, and macOS.

### 10.3 Assumptions and Operating Constraints
* The system assumes MySQL Community Server 8.0 is running locally on port `3306` with the `digital_od` database properly initialized.
* Faculty and administrative user accounts are provisioned in advance by the department administrator; self-registration is reserved for students.
* The system treats institutional duty days as continuous calendar working days; individual weekend and institutional holiday exclusions are handled during faculty review.

---

## 11. Use Case Descriptions

```
[ INSERT SCREENSHOT: Complete UML Use Case Diagram - Half Page Size ]
```

### 11.1 UC-01: User Authentication and Role Dispatching
* **Primary Actor:** Any Registered User (Student, Staff, or HOD)
* **Preconditions:** The user has navigated to `login.html`, and an active network connection to the Tomcat server is present.
* **Main Success Scenario:**
  1. The user inputs their unique username and password into the login form.
  2. The user clicks "Sign In".
  3. `LoginServlet` intercepts the request via HTTP POST.
  4. The servlet queries MySQL via `DBConnection` using a parameterized query against `users`.
  5. Credentials match an active record. The servlet retrieves the user's role, full name, and roll number.
  6. The servlet creates an `HttpSession`, stores user profile attributes, and issues an HTTP redirect to the corresponding dashboard (`student_dashboard.jsp`, `staff_dashboard.jsp`, or `hod_dashboard.jsp`).
* **Alternative Flows:**
  * *4a. Missing Input:* If either username or password is submitted blank, the servlet redirects to `login.html?error=missing_fields`.
  * *5a. Invalid Credentials:* If no record matches the submitted username and password, the servlet redirects to `login.html?error=invalid_credentials`.
* **Postconditions:** A secure `HttpSession` is active on the server, and the user is redirected to their authorized dashboard.

### 11.2 UC-02: Student OD Application Submission
* **Primary Actor:** Authenticated Student
* **Preconditions:** The student is logged in, has remaining quota balance ($< 15$ days used), and has navigated to `student_dashboard.jsp`.
* **Main Success Scenario:**
  1. The student opens the "Apply for On-Duty" form.
  2. The student selects an event category, inputs the event title, names the endorsing body/coordinator, selects the start and end dates, and provides a justification.
  3. The student clicks "Submit Application".
  4. Client-side JavaScript verifies that dates are chronologically valid and do not breach the 3-day post-event limit.
  5. The form posts to `ApplyODServlet`.
  6. The servlet retrieves the student's username and roll number from the active `HttpSession`.
  7. The servlet calls `ODService.applyOD()`, which verifies:
     - End date is within 3 days of the current date.
     - Start date precedes or equals end date.
     - Requested duration does not exceed category limits.
     - Requested dates do not overlap with existing applications.
     - Requested duration combined with existing approved days does not exceed the 15-day quota.
  8. `ODServiceImpl` inserts the application into the `od_requests` table with initial states set to `Pending`.
  9. The servlet redirects the student to `student_dashboard.jsp?status=success`.
* **Alternative Flows:**
  * *4a. Client Validation Fails:* If dates are invalid or violate the 3-day rule, JavaScript blocks submission and displays an inline error.
  * *7a. 3-Day Rule Violated (Server):* `ODServiceImpl` throws `InvalidInputException("Application rejected: Must be submitted within 3 days of event completion.")`.
  * *7b. Semester Quota Exceeded:* `ODServiceImpl` throws `InvalidInputException("OD Criteria Failed: Exceeds maximum 15-day semester quota.")`.
  * *7c. Date Overlap Detected:* `ODServiceImpl` throws `InvalidInputException("Duplicate Date Conflict: You already have an active OD application on overlapping dates.")`.
  * *Exception Handling:* `ApplyODServlet` catches `InvalidInputException`, encodes the message, and redirects to `student_dashboard.jsp?status=error&msg=...`.
* **Postconditions:** A new application row is created in `od_requests` with both approval statuses set to `Pending`.

```
[ INSERT SCREENSHOT: Modal Window for Submitting OD Application - Half Page Size ]
```

### 11.3 UC-03: Staff Review and Verification
* **Primary Actor:** Authenticated Staff Member
* **Preconditions:** The staff member is logged in, and at least one application with `staff_status = 'Pending'` exists for their department.
* **Main Success Scenario:**
  1. The staff member accesses `staff_dashboard.jsp`.
  2. The dashboard queries and displays all pending departmental applications.
  3. The staff member examines the student's details, event metadata, date span, and justification.
  4. The staff member clicks "Verify".
  5. The action posts to `UpdateODStatusServlet` with parameters `id`, `action=verify`, and role verification.
  6. The servlet updates `od_requests` via JDBC: `staff_status = 'Verified'`.
  7. The servlet redirects the staff member back to `staff_dashboard.jsp?updated=true`.
* **Alternative Flows:**
  * *4a. Staff Rejects Application:* The staff member clicks "Reject" and provides an explanatory remark. The servlet sets `staff_status = 'Rejected'`. The workflow terminates, and the rejection reason is saved.
* **Postconditions:** The application's `staff_status` transitions to `Verified` (forwarding to HOD) or `Rejected` (terminating the request).

### 11.4 UC-04: Head of Department (HOD) Final Sanction
* **Primary Actor:** Authenticated Head of Department
* **Preconditions:** The HOD is logged in, and at least one application with `staff_status = 'Verified'` and `hod_status = 'Pending'` exists.
* **Main Success Scenario:**
  1. The HOD navigates to `hod_dashboard.jsp`.
  2. The dashboard displays all staff-verified applications awaiting executive sanction.
  3. The HOD reviews the application and the staff verification record.
  4. The HOD clicks "Approve".
  5. The action posts to `UpdateODStatusServlet` with `action=approve`.
  6. The servlet executes a parameterized update setting `hod_status = 'Approved'`.
  7. The servlet redirects the HOD to `hod_dashboard.jsp?status=approved`.
* **Alternative Flows:**
  * *4a. HOD Rejects Application:* The HOD clicks "Reject". The servlet sets `hod_status = 'Rejected'`. The workflow terminates.
* **Postconditions:** The application achieves `Approved` status, officially sanctioning the student's leave and debiting their semester quota balance.

```
[ INSERT SCREENSHOT: HOD Executive Sanction Management Grid - Half Page Size ]
```

### 11.5 UC-05: Historical Audit and Quota Inspection
* **Primary Actor:** Authenticated Student
* **Preconditions:** The student is logged in and views `student_dashboard.jsp`.
* **Main Success Scenario:**
  1. The student navigates to the "Application History" section.
  2. The page executes a JDBC query via the service layer:
     ```sql
     SELECT * FROM od_requests WHERE student_username = ? ORDER BY created_at DESC
     ```
  3. The system renders a data table listing all past submissions with application ID, category, event title, date range, duration, staff status, HOD status, and reviewer comments.
  4. The student reviews the live status of pending requests and the outcomes of completed reviews.
* **Alternative Flows:**
  * *2a. No Prior Applications:* The system displays a clear placeholder message: "No On-Duty applications recorded for your account."
* **Postconditions:** The student gains visibility into their leave history and quota balance without modifying any system data.

---

## 12. System Architecture and Database Design

### 12.1 Model-View-Controller (MVC) Architectural Pattern
The application follows an enterprise Model-View-Controller (MVC) architecture, establishing clean separation among data storage, business logic, and presentation.

```
[ INSERT SCREENSHOT: MVC Layered System Architecture Diagram - Full Page Size ]
```

1. **Model Layer (`model`, `service`):**  
   Encapsulates application state, business domain rules, and database operations. Domain models (`User`, `ODRequest`) represent database entities as plain Java objects. The service layer (`ODServiceImpl`) enforces business policies—including quota tracking, date validation, and the 3-day deadline—and handles database persistence using JDBC through `DBConnection`.
2. **View Layer (`JSP`, `HTML5`, `CSS3`, `Vanilla JS`):**  
   Renders user interfaces dynamically based on model attributes supplied by the controller layer. JSP files (`student_dashboard.jsp`, `staff_dashboard.jsp`, `hod_dashboard.jsp`) generate role-gated interfaces. Vanilla JavaScript handles client-side validation and responsive interactions, while modular CSS provides a clean light theme.
3. **Controller Layer (`controller`):**  
   Implemented as Java Servlets extending `HttpServlet`. Servlets intercept incoming HTTP GET and POST requests, validate session identity and role permissions, parse input parameters, delegate processing to the service layer, handle domain exceptions, and issue redirects or forward requests to the appropriate view.

### 12.2 Relational Database Schema Design
The persistent data store is managed in MySQL Community Server under the database name `digital_od`. The schema uses the InnoDB storage engine, ensuring ACID compliance, foreign key constraint enforcement, and row-level locking.

```
[ INSERT SCREENSHOT: Relational Entity-Relationship (ER) Schema Diagram - Half Page Size ]
```

### 12.3 Table Definitions and Field Constraints

#### Table 1: `users`
Stores user credentials, role assignments, and academic profile information.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INT` | `AUTO_INCREMENT, PRIMARY KEY` | Unique internal surrogate identifier. |
| `username` | `VARCHAR(50)` | `NOT NULL, UNIQUE` | Unique login username (e.g., student register number or faculty ID). |
| `password` | `VARCHAR(100)`| `NOT NULL` | User password credential. |
| `role` | `VARCHAR(20)` | `NOT NULL` | Role designation: `'student'`, `'staff'`, or `'hod'`. |
| `roll_no` | `VARCHAR(30)` | `NOT NULL` | Academic roll number for students; faculty identification code for staff/HOD. |
| `full_name` | `VARCHAR(100)`| `NOT NULL` | Legal full name of the academic stakeholder. |
| `department` | `VARCHAR(100)`| `DEFAULT 'Computer Applications'` | Academic department association. |
| `course` | `VARCHAR(50)` | `DEFAULT 'MCA'` | Degree program or professional faculty designation. |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | System record creation timestamp. |

#### Table 2: `od_requests`
Stores individual On-Duty leave applications, event metadata, date ranges, and approval statuses.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INT` | `AUTO_INCREMENT, PRIMARY KEY` | Unique application reference number. |
| `student_username` | `VARCHAR(50)` | `NOT NULL, FOREIGN KEY` | References `users(username)` with `ON DELETE CASCADE`. |
| `roll_no` | `VARCHAR(30)` | `NOT NULL` | Student register/roll number for document reconciliation. |
| `event_type` | `VARCHAR(100)`| `NOT NULL` | Event category (e.g., Technical Symposium, Hackathon, Sports). |
| `event_name` | `VARCHAR(200)`| `NOT NULL` | Specific title and host institution of the event. |
| `authorized_body` | `VARCHAR(150)`| `DEFAULT 'Department'` | Endorsing body, campus club, or faculty coordinator. |
| `from_date` | `DATE` | `NOT NULL` | Event start date. |
| `to_date` | `DATE` | `NOT NULL` | Event end date. |
| `days_count` | `INT` | `NOT NULL DEFAULT 1` | Total working days requested: `(to_date - from_date) + 1`. |
| `reason` | `TEXT` | `NOT NULL` | Detailed justification submitted by the student. |
| `staff_status` | `VARCHAR(30)` | `DEFAULT 'Pending'` | First-tier status: `'Pending'`, `'Verified'`, or `'Rejected'`. |
| `hod_status` | `VARCHAR(30)` | `DEFAULT 'Pending'` | Final executive status: `'Pending'`, `'Approved'`, or `'Rejected'`. |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Submission timestamp used for audit and timeline checks. |

### 12.4 Entity-Relationship Mapping
* **`users` to `od_requests` Relationship:**  
  A one-to-many ($1:N$) relationship links `users` and `od_requests`. A single student user can submit multiple OD requests across their academic tenure. Conversely, each OD request belongs to exactly one student user, enforced via the foreign key constraint:
  $$\text{FOREIGN KEY (student\_username) REFERENCES users(username) ON DELETE CASCADE ON UPDATE CASCADE}$$
* Staff and HOD users do not own rows in `od_requests`; instead, they act as authorized actors whose decisions update the `staff_status` and `hod_status` fields of student-submitted records.

### 12.5 Trace of an HTTP Request Pipeline
To illustrate how the layers cooperate, consider a student submitting an application:
1. **Client Action:** The student fills out the application form on `student_dashboard.jsp` and clicks submit.
2. **Client Validation:** JavaScript catches the submit event, verifies input fields and date ranges, and allows the request to proceed.
3. **HTTP Transmission:** The browser dispatches an HTTP POST request to `/applyODServlet` containing the form data.
4. **Controller Processing:** `ApplyODServlet` intercepts the POST request. It inspects the `HttpSession` to confirm the student is authenticated.
5. **Service Layer Execution:** The servlet constructs an `ODRequest` object and invokes `ODService.applyOD()`.
6. **Policy Evaluation:** The service layer queries the database via `DBConnection` using parameterized queries to calculate existing quota usage and check for overlapping dates. It then verifies the 3-day rule and category limits.
7. **Database Commit:** The service layer issues an `INSERT` statement via a JDBC `PreparedStatement` to persist the new application row.
8. **Controller Response:** The servlet issues an HTTP 302 redirect sending the browser to `student_dashboard.jsp?status=success`.
9. **View Refresh:** The browser loads `student_dashboard.jsp`, which queries the updated application list via JDBC and displays the new record with `Pending` badges.

---

## 13. Input Validation and Software Testing

### 13.1 Tiered Validation Strategy: Browser vs. Server
To ensure data integrity and prevent policy circumvention, the application implements a defense-in-depth, two-tier validation model:

```
[ INSERT SCREENSHOT: Two-Tier Validation Architecture Flowchart - Half Page Size ]
```

1. **Client-Side Validation (Browser Tier):**  
   Implemented in Vanilla JavaScript, this tier intercepts user input before transmission. It provides immediate, inline visual feedback for obvious errors—such as missing fields, inverted date ranges, or submissions past the 3-day deadline—sparing unnecessary network latency and server overhead.
2. **Server-Side Validation (Servlet/Service Tier):**  
   Because client-side checks can be bypassed (e.g., via disabled JavaScript, modified DOM elements, or direct HTTP POST tools like cURL or Postman), the server independently re-evaluates all validation rules. The service layer verifies field completeness, date chronology, the 3-day deadline, category limits, date overlaps, and the 15-day semester quota. Violations throw an `InvalidInputException` containing a clear diagnostic explanation.

### 13.2 Error Propagation and User Feedback
When a validation rule fails on the server:
1. The service layer raises an `InvalidInputException` with a specific error message.
2. The controller intercepts the exception, URL-encodes the error message, and appends it to a redirect URL (`student_dashboard.jsp?status=error&msg=...`).
3. The JSP view reads the message from the request parameters and renders a clearly visible alert banner at the top of the interface, ensuring the user understands exactly what needs correction.

```
[ INSERT SCREENSHOT: Error Alert Toast for 3-Day Rule Rejection - Half Page Size ]
```

### 13.3 Test Strategy and Execution Environment
The testing phase involved comprehensive functional test cases executed through the user interface against a live local deployment. Tests verified both normal operational flows (positive test cases) and deliberate boundary violations (negative test cases).

* **Server:** Apache Tomcat 9.0.x on `http://localhost:8080/DigitalODSystem`
* **JDK:** OpenJDK 17 LTS
* **Database:** MySQL Community Server 8.0 with fresh seed data
* **Browser:** Google Chrome (v118) and Mozilla Firefox (v119) with developer tools enabled

### 13.4 Comprehensive Functional Test Case Suite

The following test matrix documents the functional test cases executed across all application modules:

| Test ID | Traceable FR | Description / Test Scenario | Input Data Specification | Expected System Outcome | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | FR-01, FR-02 | Valid student authentication | Username: `studentjohn`, Password: `pass123` | Authentication succeeds; session created; redirects to `student_dashboard.jsp`. | Pass |
| **TC-02** | FR-01, FR-02 | Valid staff authentication | Username: `staffjacob`, Password: `jacob1234` | Authentication succeeds; session created; redirects to `staff_dashboard.jsp`. | Pass |
| **TC-03** | FR-01, FR-02 | Valid HOD authentication | Username: `hodsmith`, Password: `hod1234` | Authentication succeeds; session created; redirects to `hod_dashboard.jsp`. | Pass |
| **TC-04** | FR-01 | Authentication with incorrect password | Username: `studentjohn`, Password: `wrongpass` | Login rejected; error alert displayed: "Invalid username or password." | Pass |
| **TC-05** | FR-01 | Authentication with blank credentials | Username: `""`, Password: `""` | Submission blocked; error message prompts user to fill all fields. | Pass |
| **TC-06** | FR-03, FR-04 | Successful OD application within policy | Category: `Hackathon`, From: Today, To: Today + 1, Endorsement: `Tech Club` | Submission accepted; stored in MySQL; shows on dashboard with `Pending` badge. | Pass |
| **TC-07** | FR-05 | Inverted date range submission | From: `2026-11-10`, To: `2026-11-08` | Blocked at client and server; error: "'To Date' cannot precede 'From Date'." | Pass |
| **TC-08** | FR-06 | Submission violating 3-day deadline | Event ended 5 days ago (`toDate = Today - 5`) | Blocked; error: "Must be submitted within 3 days of completing the duty." | Pass |
| **TC-09** | FR-06 | Submission precisely on 3-day boundary | Event ended exactly 3 days ago (`toDate = Today - 3`)| Application accepted; boundary condition verified. | Pass |
| **TC-10** | FR-07 | Submission exceeding 15-day semester quota | Used days: `13`, Requested: `3` days (Total: 16) | Blocked; error displays quota limit and remaining allowable balance (2 days). | Pass |
| **TC-11** | FR-07 | Submission consuming exact remaining quota | Used days: `12`, Requested: `3` days (Total: 15) | Application accepted; remaining quota becomes 0 days. | Pass |
| **TC-12** | FR-08 | Submission overlapping with active request | Existing OD on `2026-11-15`; new request spans `2026-11-14` to `2026-11-16` | Blocked; error: "Duplicate Date Conflict: Overlapping application found." | Pass |
| **TC-13** | FR-08 | Submission on date of a *rejected* request | Request dates match previously rejected application | Application accepted; rejected requests do not reserve calendar dates. | Pass |
| **TC-14** | FR-09 | Submission exceeding category limit | Category: `Placement` (Max 2 days), Requested: `4` days | Blocked; error: "Category 'Placement' allows a maximum duration of 2 days." | Pass |
| **TC-15** | FR-03 | Submission with missing endorsement | Endorsing body field left blank | Blocked; error: "Prior Authorization Required: Endorsement is required." | Pass |
| **TC-16** | FR-10 | Default status verification in database | Successful new application submission | Database inspection confirms `staff_status = 'Pending'` and `hod_status = 'Pending'`. | Pass |
| **TC-17** | FR-11 | Dynamic quota card calculation | Student with 5 approved days loads dashboard | Dashboard stat card correctly displays "10 Days Remaining" out of 15. | Pass |
| **TC-18** | FR-12 | Verification queue filtering for staff | Staff loads dashboard | Only applications with `staff_status = 'Pending'` from their department are listed. | Pass |
| **TC-19** | FR-13 | Staff marks application as Verified | Staff clicks "Verify" on application #101 | Record updates: `staff_status = 'Verified'`; disappears from staff queue. | Pass |
| **TC-20** | FR-13 | Staff marks application as Rejected | Staff clicks "Reject" and provides justification | Record updates: `staff_status = 'Rejected'`; workflow terminates; reason saved. | Pass |
| **TC-21** | FR-14 | HOD queue filtering | HOD loads dashboard | Only applications with `staff_status = 'Verified'` and `hod_status = 'Pending'` appear. | Pass |
| **TC-22** | FR-14 | Unverified application hidden from HOD | New application with `staff_status = 'Pending'` | Application is NOT visible on HOD dashboard, verifying sequential routing. | Pass |
| **TC-23** | FR-15 | HOD grants final approval | HOD clicks "Approve" on verified application | Record updates: `hod_status = 'Approved'`; fully sanctioned status shown to student. | Pass |
| **TC-24** | FR-15 | HOD marks application as Rejected | HOD clicks "Reject" on verified application | Record updates: `hod_status = 'Rejected'`; workflow terminates. | Pass |
| **TC-25** | FR-17 | Unauthorized URL access by student | Student session navigates to `staff_dashboard.jsp` | Filter blocks access; user redirected to `login.html?unauthorized=1`. | Pass |
| **TC-26** | FR-17 | Direct POST invocation by unauthenticated client | External POST to `/updateODStatusServlet` without session cookie | Blocked; request redirected to login page; no database modifications occur. | Pass |
| **TC-27** | FR-18 | Explicit user sign out | User clicks "Logout" button | `HttpSession` invalidated; back-button access prevented; redirected to login. | Pass |
| **TC-28** | FR-16 | Application history display for student | Student with past submissions visits history section | Complete historical table rendered with correct IDs, dates, badges, and remarks. | Pass |

```
[ INSERT SCREENSHOT: Test Results Execution Summary Screen - Half Page Size ]
```

---

## 14. Security Considerations and Known Limitations

### 14.1 Countermeasures Against SQL Injection Attacks
In enterprise web development, SQL injection represents one of the most critical vulnerabilities. The system protects against this risk by strictly prohibiting raw SQL string concatenation.

Every database read, insert, update, and delete operation across `AuthServiceImpl` and `ODServiceImpl` uses native JDBC `PreparedStatement` interfaces with parameterized place-holders (`?`). For example:

```java
// Parameterized query preventing SQL injection
String sql = "SELECT * FROM users WHERE username = ? AND password = ?";
try (PreparedStatement ps = conn.prepareStatement(sql)) {
    ps.setString(1, username.trim());
    ps.setString(2, password.trim());
    try (ResultSet rs = ps.executeQuery()) {
        // Safe processing
    }
}
```

The database driver treats parameter contents strictly as literal values rather than executable SQL syntax, neutralizing injection vectors regardless of the characters supplied in form inputs.

### 14.2 Session Management and State Isolation
User state and role permissions are managed through server-side `HttpSession` objects:
* Upon successful authentication, user identifiers and role designations are bound to a newly created session.
* Servlets and protected JSP pages inspect session attributes on every request. If a session is missing or the role does not match the required authorization level, processing terminates immediately, and the client is redirected to the login interface.
* Session fixation risks are mitigated by invalidating any existing session prior to binding credentials upon login.
* The `LogoutServlet` explicitly calls `session.invalidate()` to purge server-side session memory and invalidate client session cookies.

### 14.3 Cross-Site Scripting (XSS) and Input Sanitization
* User input strings—such as event titles, justifying statements, and administrative comments—are sanitized and encoded before rendering in the view layer.
* When dynamic parameters are reflected into HTML pages, JSTL `<c:out value="..."/>` tags and HTML-escaping utilities ensure that embedded `<script>` tags or malicious event attributes are converted into inert HTML entities (`&lt;script&gt;`), preventing execution in the browser.

### 14.4 Architectural Gaps and Production Hardening Needs
While the application fulfills all requirements for an academic software engineering project, a commercial production deployment would benefit from additional hardening:
1. **Password Hashing:** The current implementation compares credentials as stored in the database. A production deployment should store passwords as salted hashes using strong one-way cryptographic algorithms such as **BCrypt** or **Argon2**, ensuring credentials cannot be recovered even if the database is compromised.
2. **Transport Layer Security (HTTPS):** The application runs over plain HTTP on port `8080` for local development. Production deployments must enforce HTTPS with TLS 1.3 certificates to prevent credential interception on open networks.
3. **Database Connection Pooling:** The current `DBConnection` utility allocates physical JDBC connections on demand. Integrating an enterprise connection pool (such as **HikariCP** or Apache Commons DBCP) would optimize connection reuse and improve throughput under heavy concurrent loads.
4. **Brute-Force Rate Limiting:** The login servlet does not currently enforce delays or account lockouts after repeated failed sign-in attempts. Adding an IP-based or account-based rate-limiting mechanism would guard against automated brute-force attacks.

---

## 15. Future Enhancements

The system's modular architecture provides a solid base for incorporating additional enterprise features in subsequent development cycles:

```
[ INSERT SCREENSHOT: Conceptual Architecture for Future ERP & Biometric Integration - Half Page Size ]
```

1. **Biometric Attendance System Integration:**  
   Future versions could bridge the database with campus biometric turnstiles and RFID attendance loggers. Once an OD application achieves final HOD approval, an automated database trigger could update the biometric attendance register directly, marking the student present for scheduled lecture hours during the approved date range.

2. **Automated Transactional Notifications (Email / SMS / WhatsApp):**  
   Integrating an asynchronous notification engine using the JavaMail API or webhooks (e.g., Twilio, SendGrid) would deliver immediate status alerts to students when their applications are verified or rejected, and notify faculty when new requests enter their review queues.

3. **Dedicated Cross-Platform Mobile Application:**  
   The core service layer could expose standard RESTful JSON endpoints alongside traditional JSP views. This would enable the deployment of native Android and iOS mobile applications (using Flutter or React Native), allowing students to submit leaves and faculty to issue approvals on mobile devices.

4. **Institutional ERP and Academic Schedule Synchronization:**  
   Connecting the platform to the institution’s central ERP database would allow the system to cross-reference proposed leave dates against the student's actual timetable, automatically identifying missed laboratory sessions, internal examination clashes, or minimum attendance warnings.

5. **Cryptographically Signed Digital OD Slips and QR Verification:**  
   Upon final approval, the system could dynamically generate downloadable PDF clearance certificates (using libraries such as iText or Apache PDFBox). Each certificate could include an embedded, cryptographically signed QR code, allowing campus security, examination invigilators, and laboratory instructors to instantly verify application authenticity using a handheld scanner.

---

## 16. Conclusion

The **Digital Leave and On-Duty (OD) Application System** successfully resolves the operational inefficiencies, administrative delays, and lack of accountability inherent in traditional paper-based academic leave processes. By translating institutional academic policies into deterministic software logic, the application establishes a transparent, multi-tier approval pipeline that serves students, faculty mentors, and departmental leadership alike.

From an engineering perspective, the project demonstrates the enduring power and architectural clarity of fundamental Java Enterprise technologies. Operating on a strict Model-View-Controller (MVC) pattern and built with native **Java Servlets, JSP, JDBC**, and **MySQL**, the system achieves robust data integrity, maintainable separation of concerns, and dependable performance without the memory overhead or configuration bloat of heavy external frameworks. 

Key institutional rules—including the non-negotiable 3-day post-event submission deadline, the 15-day semester quota cap, date chronology validation, and duplicate tenure overlap prevention—are enforced systematically across both browser and server layers. The resulting platform eliminates paper waste, prevents signature forgery, provides real-time auditability, and significantly streamlines the administrative workflow of the department.

Ultimately, this project represents an end-to-end practical realization of modern software engineering principles, demonstrating how methodical requirements analysis, structured database design, defensive coding, and thoughtful user experience design can converge to modernize everyday administrative workflows in higher education.

---

```
[ INSERT SCREENSHOT: Final Approved Application View with Digital Stamp - Half Page Size ]
```

---
*End of Report.*
