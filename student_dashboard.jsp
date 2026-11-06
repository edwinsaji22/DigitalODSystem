<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.util.List" %>
<%@ page import="model.ODRequest" %>
<%@ page import="service.ODService" %>
<%@ page import="service.ODServiceImpl" %>

<%
    // Server-side session verification
    if (session == null || session.getAttribute("loggedInUser") == null) {
        response.sendRedirect("login.html?unauthorized=1");
        return;
    }

    String loggedInUser = (String) session.getAttribute("loggedInUser");
    String userRole = (String) session.getAttribute("userRole");
    String rollNo = (String) session.getAttribute("rollNo");
    String fullName = (String) session.getAttribute("fullName");
    String department = (String) session.getAttribute("department");

    if (fullName == null || fullName.isEmpty()) fullName = "John Doe";
    if (rollNo == null || rollNo.isEmpty()) rollNo = "21MCA015";
    if (department == null || department.isEmpty()) department = "Computer Applications (MCA)";

    // Compute Initials for Avatar
    String initials = "JD";
    if (fullName != null && !fullName.trim().isEmpty()) {
        String[] parts = fullName.trim().split("\\s+");
        if (parts.length >= 2) {
            initials = ("" + parts[0].charAt(0) + parts[1].charAt(0)).toUpperCase();
        } else if (parts[0].length() >= 2) {
            initials = parts[0].substring(0, 2).toUpperCase();
        } else {
            initials = parts[0].toUpperCase();
        }
    }

    // Enforce role-based access
    if (!"student".equalsIgnoreCase(userRole)) {
        response.sendRedirect("staff".equalsIgnoreCase(userRole) ? "staff_dashboard.jsp" : "hod_dashboard.jsp");
        return;
    }

    // Fetch live OD requests submitted by this student from MySQL / Service
    ODService odService = new ODServiceImpl();
    List<ODRequest> studentRequests = odService.getODRequestsByStudent(loggedInUser);

    // Calculate metrics strictly dynamically from live database records
    int totalApplications = studentRequests.size();
    int pendingCount = 0;
    int approvedCount = 0;
    int rejectedCount = 0;

    for (ODRequest req : studentRequests) {
        if (req.isFinalApproved()) {
            approvedCount++;
        } else if (req.isAnyRejected()) {
            rejectedCount++;
        } else {
            pendingCount++;
        }
    }

    // Dynamic Semester OD Quota (Real calculation from SUM(days_count) in MySQL)
    int quotaUsed = odService.getUsedODDays(loggedInUser);
    int quotaTotal = 15;
    int quotaRemaining = Math.max(0, quotaTotal - quotaUsed);
    int quotaPercent = (int) Math.min(100, Math.round(((double) quotaUsed / quotaTotal) * 100));

    String statusParam = request.getParameter("status");
    String msgParam = request.getParameter("msg");
%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Portal - Digital Leave/OD (On-Duty) Application System</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>

    <!-- Top Navigation Bar -->
    <header class="top-nav">
        <div class="brand-section">
            <div class="brand-icon-box">&#127891;</div>
            <div>
                <div class="brand-title">Digital Leave/OD (On-Duty) Application System</div>
                <div class="brand-subtitle">Academic Leave &amp; Student Service Desk</div>
            </div>
        </div>

        <!-- Right Nav User Actions -->
        <div class="nav-right-actions">
            <button type="button" class="btn-criteria-nav" onclick="openJsonApiModal()" title="View Live RESTful JSON API Endpoint" style="background: rgba(99, 102, 241, 0.08); color: #4F46E5; border: 1px solid rgba(99, 102, 241, 0.25); cursor: pointer; display: inline-flex; align-items: center; gap: 6px; font-weight: 700;">
                <span style="font-family: monospace; font-size: 14px;">{ ; }</span> JSON API
            </button>
            <a href="od_criteria.jsp" class="btn-criteria-nav" title="View Official OD Rules & Criteria">
                <span>&#128220;</span> OD Rules &amp; Criteria
            </a>
            <div class="user-profile-pill">
                <div class="avatar-circle"><%= initials %></div>
                <div class="user-text-info">
                    <span class="user-display-name"><%= fullName %></span>
                    <span class="user-display-roll">Student &bull; <%= rollNo %></span>
                </div>
            </div>
            <a href="logoutServlet" class="btn-logout-clean" title="Sign out of portal">
                <span>&#10150;</span> Logout
            </a>
        </div>
    </header>

    <main class="main-wrapper" style="max-width: 1000px; margin: 0 auto; padding: 24px 20px; width: 100%;">

        <!-- Clean Welcome Banner -->
        <section class="welcome-banner-card" style="margin-bottom: 20px; padding: 20px 24px;">
            <div class="welcome-left">
                <h1 style="font-size: 22px; font-weight: 800; color: var(--text-primary); margin-bottom: 4px;">Welcome, <%= fullName %>! &#128075;</h1>
                <p style="font-size: 13px; color: var(--text-muted); margin: 0;">
                    Roll Number: <strong><%= rollNo %></strong> &bull; Department: <strong><%= department %></strong>
                </p>
            </div>
        </section>

        <!-- Feedback Alert Messages -->
        <% if ("success".equals(statusParam)) { %>
            <div class="alert alert-success">
                &#10003; <strong>OD Application Submitted:</strong> Your request has been queued for Faculty Advisor verification.
            </div>
        <% } else if ("error".equals(statusParam)) { %>
            <div class="alert alert-error">
                &#9888; <strong>Submission Error:</strong> <%= msgParam != null ? msgParam : "Could not submit application. Please check input fields." %>
            </div>
        <% } %>

        <!-- Dynamic Summary KPI Cards Grid (Exactly 3 Simple Dynamic Cards) -->
        <section class="kpi-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px;">
            <!-- 1. Total Applications -->
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Total Applications</span>
                    <div class="kpi-icon-wrap kpi-icon-indigo">&#128196;</div>
                </div>
                <div class="kpi-value"><%= totalApplications %></div>
                <div class="kpi-footer">
                    <span>Submitted Requests</span>
                    <span class="kpi-tag kpi-tag-green">Active</span>
                </div>
            </div>

            <!-- 2. Pending Verification -->
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Pending</span>
                    <div class="kpi-icon-wrap kpi-icon-warning">&#9203;</div>
                </div>
                <div class="kpi-value" style="color: var(--warning);"><%= pendingCount %></div>
                <div class="kpi-footer">
                    <span>Under Review</span>
                    <span class="kpi-tag kpi-tag-amber"><%= pendingCount > 0 ? "Under Review" : "Clear" %></span>
                </div>
            </div>

            <!-- 3. Approved ODs -->
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Approved</span>
                    <div class="kpi-icon-wrap kpi-icon-success">&#10003;</div>
                </div>
                <div class="kpi-value" style="color: var(--success);"><%= approvedCount %></div>
                <div class="kpi-footer">
                    <span>OD Sanctioned</span>
                    <span class="kpi-tag kpi-tag-green">&#10003; Valid</span>
                </div>
            </div>
        </section>

        <!-- Clean & Simplified "Apply for OD" Form (Only 5 Essential Inputs) -->
        <section class="form-card" style="margin-bottom: 24px;">
            <div class="form-card-header">
                <div class="form-header-left">
                    <div class="form-header-icon">&#9997;</div>
                    <div>
                        <div class="form-header-title">Apply for Leave / On-Duty (OD)</div>
                        <div class="form-header-subtitle">Submit academic, technical, sports or workshop participation for faculty and HOD sanction</div>
                    </div>
                </div>
            </div>

            <form action="applyODServlet" method="POST" id="odApplicationForm" onsubmit="return validateODForm()">
                <!-- Field 1: Roll Number & Student Name (Auto-filled and read-only from HttpSession) -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
                    <div>
                        <label class="field-label" for="rollNoInput">Applicant Roll Number</label>
                        <input type="text" class="form-control" id="rollNoInput" name="rollNo" value="<%= rollNo %>" readonly style="background-color: #F8FAFC; color: var(--text-secondary); cursor: not-allowed; font-weight: 700;">
                    </div>
                    <div>
                        <label class="field-label" for="studentNameInput">Student Full Name</label>
                        <input type="text" class="form-control" id="studentNameInput" value="<%= fullName %>" readonly style="background-color: #F8FAFC; color: var(--text-secondary); cursor: not-allowed; font-weight: 700;">
                    </div>
                </div>

                <!-- Field 2: OD Category (Dropdown with exact 7 Jayantian options) -->
                <div class="form-field-group" style="margin-bottom: 16px;">
                    <label class="field-label" for="eventTypeSelect">OD Category <span class="required">*</span></label>
                    <select class="form-control" id="eventTypeSelect" name="eventType" required>
                        <option value="Department Association / Academic Club Event" selected>Department Association / Academic Club Event</option>
                        <option value="Technical Symposium / Workshop / Hackathon">Technical Symposium / Workshop / Hackathon</option>
                        <option value="Conference / Paper Presentation">Conference / Paper Presentation</option>
                        <option value="Inter-Collegiate Sports / Zonal Tournament">Inter-Collegiate Sports / Zonal Tournament</option>
                        <option value="NSS / NCC / CSA / Extension Activity">NSS / NCC / CSA / Extension Activity</option>
                        <option value="Cultural / Literary Club Representation">Cultural / Literary Club Representation</option>
                        <option value="Placement Drive / Official Department Duty">Placement Drive / Official Department Duty</option>
                    </select>
                </div>

                <!-- Field 3: Authorized Body / Club & Staff Coordinator Name -->
                <div class="form-field-group" style="margin-bottom: 16px;">
                    <label class="field-label" for="authorizedBodyInput">Authorized Body / Club &amp; Staff Coordinator Name <span class="required">*</span></label>
                    <input type="text" class="form-control" id="authorizedBodyInput" name="authorizedBody" placeholder="e.g. ACM Student Chapter &bull; Dr. Alan Smith / Prof. Jacob Mathew" required>
                    <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">&#9432; Required for Prior Authorization &amp; Staff Coordinator endorsement.</div>
                </div>

                <!-- Field 4: Event Date Picker (From Date & To Date) with quick helper buttons and timeline indicator -->
                <div class="form-field-group" style="margin-bottom: 16px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <label class="field-label" style="margin-bottom: 0;">Event Dates (Duty Duration) <span class="required">*</span></label>
                        <div style="display: flex; gap: 6px; align-items: center;">
                            <span style="font-size: 11px; color: var(--text-muted); font-weight: 600;">Quick Pick:</span>
                            <button type="button" class="btn-quick-date" onclick="setQuickDate(0)">Today</button>
                            <button type="button" class="btn-quick-date" onclick="setQuickDate(1)">Yesterday</button>
                            <button type="button" class="btn-quick-date" onclick="setQuickDate(2)">2 Days Ago</button>
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                        <div>
                            <label class="field-sublabel" for="fromDateInput" style="font-size: 11px; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 4px;">From Date</label>
                            <input type="date" class="form-control" id="fromDateInput" name="fromDate" onchange="calculateDateDiff()" required>
                        </div>
                        <div>
                            <label class="field-sublabel" for="toDateInput" style="font-size: 11px; font-weight: 700; color: var(--text-muted); display: block; margin-bottom: 4px;">To Date</label>
                            <input type="date" class="form-control" id="toDateInput" name="toDate" onchange="calculateDateDiff()" required>
                        </div>
                    </div>
                    <!-- Automatic display showing days passed since event ended -->
                    <div id="timelineNotice" style="margin-top: 8px; font-size: 12px; font-weight: 600; padding: 7px 12px; border-radius: var(--radius-sm); display: none; align-items: center; gap: 6px;">
                    </div>
                </div>

                <!-- Field 5: Reason / Event Details -->
                <div class="form-field-group">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <label class="field-label" for="reasonText" style="margin-bottom: 0;">Reason / Event Details <span class="required">*</span></label>
                        <span style="font-size: 11px; color: var(--text-light);" id="charCounter">0 / 500 characters</span>
                    </div>
                    <textarea class="form-control" id="reasonText" name="reason" rows="3" maxlength="500" placeholder="State your specific role, duty details, paper topic, or sports event participation..." oninput="updateCharCount()" required></textarea>
                </div>

                <!-- Form Action Buttons -->
                <div style="display: flex; gap: 12px; align-items: center; margin-top: 18px;">
                    <button type="submit" class="btn-submit-primary">
                        Submit OD Request &rarr;
                    </button>
                    <button type="reset" class="btn-secondary" onclick="resetFormCustom()">
                        Clear
                    </button>
                </div>
            </form>
        </section>

        <!-- Live Database Applications Table Section -->
        <section class="history-section-card" id="history-table-section">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 10px;">
                <div>
                    <h3 style="font-size: 16px; font-weight: 800; color: var(--text-primary); display: flex; align-items: center; gap: 8px;">
                        <span>&#128203;</span> On-Duty Application History (<span id="totalRecordsCount"><%= studentRequests.size() %></span> Total Records)
                    </h3>
                    <p style="font-size: 12px; color: var(--text-muted);">Real-time status of your submitted On-Duty applications.</p>
                </div>
            </div>

            <!-- Instant Search & Multi-Criteria Filtering Toolbar -->
            <div class="filter-toolbar">
                <div class="filter-left">
                    <div class="search-box-wrap">
                        <span class="search-box-icon">&#128269;</span>
                        <input type="text" id="tableSearchInput" class="search-box-input" placeholder="Search by Event, Category, Date, Reason..." onkeyup="filterApplicationsTable()">
                    </div>

                    <select id="statusFilterSelect" class="filter-select" onchange="filterApplicationsTable()">
                        <option value="ALL">All Statuses</option>
                        <option value="PENDING">Pending Review</option>
                        <option value="APPROVED">Final Approved</option>
                        <option value="REJECTED">Declined</option>
                    </select>

                    <select id="categoryFilterSelect" class="filter-select" onchange="filterApplicationsTable()">
                        <option value="ALL">All Categories</option>
                        <option value="Symposium">Symposium / Workshop</option>
                        <option value="Hackathon">Hackathon / Coding</option>
                        <option value="Conference">Conference / Paper</option>
                        <option value="Sports">Sports / Zonal</option>
                        <option value="NSS">NSS / NCC / Duty</option>
                        <option value="Placement">Placement / Interview</option>
                        <option value="Internship">Internship / IV</option>
                        <option value="Cultural">Cultural Fest</option>
                        <option value="Medical">Medical / Emergency</option>
                    </select>

                    <span class="filter-counter-badge" id="visibleRowsBadge">Showing <%= studentRequests.size() %> entries</span>
                </div>

                <!-- One-Click Export to CSV and JSON -->
                <div style="display: flex; gap: 8px;">
                    <button type="button" class="btn-export-csv" onclick="exportTableToCSV('studentTable', 'Digital_OD_Student_Applications.csv')">
                        <span>&#128229;</span> Export CSV
                    </button>
                    <button type="button" class="btn-export-csv" onclick="exportTableToJSON()" style="background: #EEF2FF; color: #4338CA; border: 1px solid #C7D2FE;" title="Export current application dataset as structured JSON">
                        <span style="font-family: monospace; font-weight: bold;">{ }</span> Export JSON
                    </button>
                </div>
            </div>

            <!-- Applications Data Table -->
            <div class="table-responsive">
                <table class="data-table" id="studentTable">
                    <thead>
                        <tr>
                            <th style="width: 70px;">Ref ID</th>
                            <th>Applicant Roll No</th>
                            <th>Category</th>
                            <th>Authorized Body &amp; Coordinator</th>
                            <th>Event Details &amp; Purpose</th>
                            <th>Date &amp; Duration</th>
                            <th>Staff Review</th>
                            <th>HOD Decision</th>
                            <th>Overall Status</th>
                            <th style="text-align: center; min-width: 150px;">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="studentTableBody">
                        <% if (studentRequests.isEmpty()) { %>
                            <tr id="noRecordsRow">
                                <td colspan="10" style="text-align: center; padding: 36px; color: var(--text-muted);">
                                    No application records found. Submit an OD request using the form above.
                                </td>
                            </tr>
                        <% } else { %>
                            <% for (ODRequest req : studentRequests) { %>
                                <tr data-id="<%= req.getId() %>"
                                    data-roll="<%= req.getRollNo() %>"
                                    data-category="<%= req.getEventType() %>"
                                    data-authorized="<%= req.getAuthorizedBody() %>"
                                    data-event="<%= req.getEventName() %>"
                                    data-date="<%= req.getEventDate() %>"
                                    data-from="<%= req.getFromDate() != null ? req.getFromDate() : req.getEventDate() %>"
                                    data-to="<%= req.getToDate() != null ? req.getToDate() : req.getEventDate() %>"
                                    data-days="<%= req.getDaysCount() %>"
                                    data-reason="<%= req.getReason() %>"
                                    data-staff="<%= req.getStaffStatus() %>"
                                    data-hod="<%= req.getHodStatus() %>"
                                    data-overall="<%= req.isFinalApproved() ? "APPROVED" : (req.isAnyRejected() ? "REJECTED" : "PENDING") %>"
                                    data-created="<%= req.getCreatedAt() != null ? req.getCreatedAt() : "" %>">
                                    <td><strong>#OD-<%= req.getId() %></strong></td>
                                    <td><span style="font-weight: 700; color: var(--primary);"><%= req.getRollNo() %></span></td>
                                    <td><strong><%= req.getEventType() %></strong></td>
                                    <td>
                                        <div><strong><%= req.getAuthorizedBody() != null && !req.getAuthorizedBody().isEmpty() ? req.getAuthorizedBody() : "General Body" %></strong></div>
                                        <div style="font-size: 11px; color: var(--text-muted);">&#10003; Coordinator Endorsed</div>
                                    </td>
                                    <td>
                                        <div><strong><%= req.getEventName() %></strong></div>
                                        <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px;"><%= req.getReason() %></div>
                                    </td>
                                    <td>
                                        <div style="font-weight: 700;"><%= req.getFromDate() != null ? req.getFromDate() : req.getEventDate() %></div>
                                        <% if (req.getToDate() != null && !req.getToDate().equals(req.getFromDate())) { %>
                                            <div style="font-size: 11px; color: var(--text-muted);">to <%= req.getToDate() %></div>
                                        <% } %>
                                        <div style="font-size: 11px; color: var(--primary); font-weight: 700; margin-top: 2px;">
                                            <%= req.getDaysCount() %> <%= req.getDaysCount() == 1 ? "Day" : "Days" %>
                                        </div>
                                    </td>
                                    <td>
                                        <% if ("Verified".equalsIgnoreCase(req.getStaffStatus())) { %>
                                            <span class="badge-approved-pill">&#10003; Verified</span>
                                        <% } else if ("Rejected".equalsIgnoreCase(req.getStaffStatus())) { %>
                                            <span class="badge-declined-pill">&#10005; Rejected</span>
                                        <% } else { %>
                                            <span class="badge-pending-pill">&#9203; Pending</span>
                                        <% } %>
                                    </td>
                                    <td>
                                        <% if ("Approved".equalsIgnoreCase(req.getHodStatus())) { %>
                                            <span class="badge-approved-pill">&#10003; Approved</span>
                                        <% } else if ("Rejected".equalsIgnoreCase(req.getHodStatus())) { %>
                                            <span class="badge-declined-pill">&#10005; Rejected</span>
                                        <% } else { %>
                                            <span class="badge-pending-pill">&#9203; Pending</span>
                                        <% } %>
                                    </td>
                                    <td>
                                        <% if (req.isFinalApproved()) { %>
                                            <span class="badge-approved-pill" style="font-weight: 800;">&#9733; Final OD Granted</span>
                                        <% } else if (req.isAnyRejected()) { %>
                                            <span class="badge-declined-pill">Declined</span>
                                        <% } else if (req.isStaffVerified()) { %>
                                            <span class="badge-pending-pill">Awaiting HOD Sign-off</span>
                                        <% } else { %>
                                            <span class="badge-pending-pill">Faculty Review</span>
                                        <% } %>
                                    </td>
                                    <td style="text-align: center;">
                                        <div style="display: inline-flex; gap: 6px; justify-content: center;">
                                            <% if (req.isFinalApproved()) { %>
                                                <button type="button" class="btn-pass" onclick="openGatePassModal(this.closest('tr'))" title="View & Print Official Gate Pass">
                                                    <span>&#127915;</span> OD Pass
                                                </button>
                                            <% } %>
                                            <button type="button" class="btn-inspect" onclick="openAuditModal(this.closest('tr'))" title="Inspect Application & Audit Trail">
                                                <span>&#128065;</span> Details
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            <% } %>
                        <% } %>
                    </tbody>
                </table>
            </div>
        </section>

    </main>

    <!-- Site Footer -->
    <footer class="site-footer">
        <div>
            Digital Leave &amp; On-Duty Management System &bull; College of Engineering &amp; Technology
        </div>
        <div class="footer-links">
            <span>Logged in as <strong><%= fullName %> (<%= rollNo %>)</strong></span>
            <span>&bull;</span>
            <span>Academic Session 2026</span>
        </div>
    </footer>

    <!-- ======================================================================
         MODAL 1: OFFICIAL DIGITAL OD GATE PASS (PRINTABLE WITH QR)
         ====================================================================== -->
    <div class="modal-overlay" id="gatePassModal">
        <div class="modal-box">
            <div class="modal-box-header">
                <div class="modal-box-title">
                    <span>&#127915;</span> Official Digital OD Gate Pass / Attendance Credit
                </div>
                <button type="button" class="modal-close-btn" onclick="closeModal('gatePassModal')">&times;</button>
            </div>

            <div class="modal-box-body">
                <div class="official-pass-sheet" id="printablePassContent">
                    <div class="pass-header">
                        <div class="pass-institute-name">College of Engineering &amp; Technology</div>
                        <div class="pass-department-name">Autonomous Academic Institution &bull; Affiliated to University</div>
                        <div class="pass-badge-title">Official On-Duty (OD) Sanction Pass</div>
                    </div>

                    <div class="pass-ref-row">
                        <span>Ref ID: <strong id="passRefId">#OD-2026-000</strong></span>
                        <span>Date Issued: <strong id="passIssueDate">Today</strong></span>
                    </div>

                    <div class="pass-grid-2">
                        <div>
                            <div class="pass-field-label">Student Name</div>
                            <div class="pass-field-val" id="passStudentName"><%= fullName %></div>
                        </div>
                        <div>
                            <div class="pass-field-label">Roll / Register No</div>
                            <div class="pass-field-val" id="passRollNo"><%= rollNo %></div>
                        </div>
                        <div>
                            <div class="pass-field-label">Department &amp; Course</div>
                            <div class="pass-field-val" id="passDept"><%= department %></div>
                        </div>
                        <div>
                            <div class="pass-field-label">OD Category</div>
                            <div class="pass-field-val" id="passCategory">Hackathon</div>
                        </div>
                        <div>
                            <div class="pass-field-label">Event Date &amp; Duration</div>
                            <div class="pass-field-val" id="passEventDate">2026-10-15</div>
                        </div>
                        <div>
                            <div class="pass-field-label">Official Status</div>
                            <div class="pass-field-val" style="color: var(--success);">&#10003; Approved &amp; Granted</div>
                        </div>
                    </div>

                    <div class="pass-purpose-box">
                        <div class="pass-field-label">Event Title &amp; Host Institution</div>
                        <div class="pass-field-val" id="passEventName" style="font-size: 13px;">National Smart TechFest 2026</div>
                        <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;" id="passReason">Selected as college team representative.</div>
                    </div>

                    <div class="pass-verification-footer">
                        <div class="qr-code-box" id="qrContainer" title="Scan to verify OD Gate Pass">
                            <!-- Clean SVG Verification QR -->
                            <svg width="66" height="66" viewBox="0 0 33 33" shape-rendering="crispEdges">
                                <path fill="#0F172A" d="M0,0 h7v7 h-7z M1,1 v5 h5 v-5z M2,2 h3 v3 h-3z M26,0 h7v7 h-7z M27,1 v5 h5 v-5z M28,2 h3 v3 h-3z M0,26 h7v7 h-7z M1,27 v5 h5 v-5z M2,28 h3 v3 h-3z M9,1 h2v1 h-2z M13,1 h1v1 h-1z M16,1 h2v1 h-2z M20,1 h3v1 h-3z M10,3 h1v1 h-1z M14,3 h2v1 h-2z M18,3 h1v1 h-1z M22,3 h2v1 h-2z M8,5 h2v1 h-2z M12,5 h3v1 h-3z M17,5 h2v1 h-2z M21,5 h2v1 h-2z M9,8 h2v1 h-2z M13,8 h1v1 h-1z M16,8 h3v1 h-3z M21,8 h2v1 h-2z M24,8 h2v1 h-2z M8,10 h1v1 h-1z M11,10 h3v1 h-3z M16,10 h1v1 h-1z M19,10 h2v1 h-2z M23,10 h3v1 h-3z M28,10 h3v1 h-3z M9,12 h2v1 h-2z M13,12 h2v1 h-2z M17,12 h1v1 h-1z M20,12 h3v1 h-3z M25,12 h1v1 h-1z M28,12 h2v1 h-2z M8,14 h2v1 h-2z M12,14 h1v1 h-1z M15,14 h3v1 h-3z M20,14 h2v1 h-2z M24,14 h3v1 h-3z M9,16 h3v1 h-3z M14,16 h2v1 h-2z M18,16 h2v1 h-2z M22,16 h1v1 h-1z M25,16 h2v1 h-2z M29,16 h2v1 h-2z M8,18 h1v1 h-1z M11,18 h2v1 h-2z M15,18 h2v1 h-2z M19,18 h1v1 h-1z M22,18 h3v1 h-3z M27,18 h2v1 h-2z M9,20 h2v1 h-2z M13,20 h3v1 h-3z M18,20 h1v1 h-1z M21,20 h2v1 h-2z M25,20 h1v1 h-1z M28,20 h3v1 h-3z M8,22 h3v1 h-3z M13,22 h1v1 h-1z M16,22 h2v1 h-2z M20,22 h1v1 h-1z M23,22 h2v1 h-2z M27,22 h1v1 h-1z M29,22 h2v1 h-2z M9,24 h1v1 h-1z M12,24 h2v1 h-2z M16,24 h3v1 h-3z M21,24 h2v1 h-2z M25,24 h3v1 h-3z M9,27 h3v1 h-3z M14,27 h1v1 h-1z M17,27 h2v1 h-2z M21,27 h2v1 h-2z M25,27 h1v1 h-1z M28,27 h2v1 h-2z M8,29 h2v1 h-2z M12,29 h3v1 h-3z M17,29 h1v1 h-1z M20,29 h3v1 h-3z M25,29 h2v1 h-2z M29,29 h1v1 h-1z M9,31 h1v1 h-1z M12,31 h2v1 h-2z M16,31 h3v1 h-3z M21,31 h1v1 h-1z M24,31 h2v1 h-2z M28,31 h3v1 h-3z" />
                            </svg>
                        </div>

                        <div>
                            <span class="pass-stamp-approved">&#10003; HOD SANCTIONED</span>
                        </div>

                        <div class="pass-sign-wrap">
                            <div>Faculty Advisor: <strong>Verified</strong></div>
                            <div style="margin-top: 4px;">Sanctioned By: <strong>Head of Department</strong></div>
                            <div style="color: var(--text-light); font-size: 10px; margin-top: 2px;">Digitally Validated Security Seal</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="modal-box-footer">
                <button type="button" class="btn-secondary" onclick="closeModal('gatePassModal')">Close</button>
                <button type="button" class="btn-submit-primary" onclick="window.print()">
                    <span>&#128424;</span> Print OD Gate Pass
                </button>
            </div>
        </div>
    </div>

    <!-- ======================================================================
         MODAL 2: APPLICATION DETAILS & MULTI-TIER AUDIT TRAIL
         ====================================================================== -->
    <div class="modal-overlay" id="auditModal">
        <div class="modal-box">
            <div class="modal-box-header">
                <div class="modal-box-title">
                    <span>&#128065;</span> Application Inspection &amp; Audit Trail
                </div>
                <button type="button" class="modal-close-btn" onclick="closeModal('auditModal')">&times;</button>
            </div>

            <div class="modal-box-body">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; background: #F8FAFC; padding: 14px; border-radius: var(--radius-md); border: 1px solid var(--border-color); margin-bottom: 20px;">
                    <div>
                        <div class="pass-field-label">Reference ID</div>
                        <div class="pass-field-val" id="auditRefId">#OD-000</div>
                    </div>
                    <div>
                        <div class="pass-field-label">Category</div>
                        <div class="pass-field-val" id="auditCategory">-</div>
                    </div>
                    <div style="grid-column: span 2;">
                        <div class="pass-field-label">Event Title</div>
                        <div class="pass-field-val" id="auditEventTitle" style="font-size: 14px;">-</div>
                    </div>
                    <div style="grid-column: span 2;">
                        <div class="pass-field-label">Authorized Body &amp; Staff Coordinator</div>
                        <div class="pass-field-val" id="auditAuthorized" style="font-size: 13px; font-weight: 700; color: var(--primary);">-</div>
                    </div>
                    <div>
                        <div class="pass-field-label">Event Date</div>
                        <div class="pass-field-val" id="auditDate">-</div>
                    </div>
                    <div>
                        <div class="pass-field-label">Date Submitted</div>
                        <div class="pass-field-val" id="auditCreated">-</div>
                    </div>
                    <div style="grid-column: span 2;">
                        <div class="pass-field-label">Reason / Statement</div>
                        <div style="font-size: 13px; color: var(--text-secondary); margin-top: 2px;" id="auditReason">-</div>
                    </div>
                </div>

                <div style="font-size: 13px; font-weight: 800; color: var(--text-primary); margin-bottom: 12px;">
                    Multi-Tier Approval Progress Stepper
                </div>

                <div class="audit-stepper" id="auditStepper">
                    <!-- Step 1: Submission -->
                    <div class="stepper-item completed">
                        <div class="stepper-node">&#10003;</div>
                        <div class="stepper-content">
                            <div class="stepper-title">Application Submitted by Student</div>
                            <div class="stepper-sub">Logged in database &bull; Initial draft queued</div>
                        </div>
                    </div>

                    <!-- Step 2: Faculty Advisor -->
                    <div class="stepper-item" id="auditStepStaff">
                        <div class="stepper-node" id="auditNodeStaff">&#9203;</div>
                        <div class="stepper-content">
                            <div class="stepper-title">Faculty Advisor Review</div>
                            <div class="stepper-sub" id="auditSubStaff">Awaiting review by Prof. Jacob Mathew</div>
                        </div>
                    </div>

                    <!-- Step 3: HOD Decision -->
                    <div class="stepper-item" id="auditStepHod">
                        <div class="stepper-node" id="auditNodeHod">&#9675;</div>
                        <div class="stepper-content">
                            <div class="stepper-title">Head of Department (HOD) Sanction</div>
                            <div class="stepper-sub" id="auditSubHod">Awaiting departmental clearance by Dr. Alan Smith</div>
                        </div>
                    </div>

                    <!-- Step 4: Final Outcome -->
                    <div class="stepper-item" id="auditStepFinal">
                        <div class="stepper-node" id="auditNodeFinal">&#9675;</div>
                        <div class="stepper-content">
                            <div class="stepper-title">Attendance Waiver &amp; Biometric Credit</div>
                            <div class="stepper-sub" id="auditSubFinal">Pending completion of multi-tier workflow</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="modal-box-footer">
                <button type="button" class="btn-secondary" onclick="closeModal('auditModal')">Close</button>
            </div>
        </div>
    </div>

    <!-- Client-Side Interactive Logic -->
    <script>
        // Character counter
        function updateCharCount() {
            const textarea = document.getElementById('reasonText');
            const counter = document.getElementById('charCounter');
            counter.textContent = textarea.value.length + ' / 500 characters';
        }

        function resetFormCustom() {
            setTimeout(() => {
                setDefaultDates();
                updateCharCount();
            }, 50);
        }

        function setDefaultDates() {
            const today = new Date().toISOString().split('T')[0];
            const fromInput = document.getElementById('fromDateInput');
            const toInput = document.getElementById('toDateInput');
            if (fromInput && !fromInput.value) fromInput.value = today;
            if (toInput && !toInput.value) toInput.value = today;
            calculateDateDiff();
        }

        function setQuickDate(daysAgo) {
            const d = new Date();
            d.setDate(d.getDate() - daysAgo);
            const dateStr = d.toISOString().split('T')[0];
            document.getElementById('fromDateInput').value = dateStr;
            document.getElementById('toDateInput').value = dateStr;
            calculateDateDiff();
        }

        function calculateDateDiff() {
            const toDateVal = document.getElementById('toDateInput').value;
            const fromDateVal = document.getElementById('fromDateInput').value;
            const noticeBox = document.getElementById('timelineNotice');
            if (!toDateVal) {
                noticeBox.style.display = 'none';
                return;
            }

            const toDate = new Date(toDateVal + 'T00:00:00');
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            const diffTime = today.getTime() - toDate.getTime();
            const daysPassed = Math.floor(diffTime / (1000 * 60 * 60 * 24));

            noticeBox.style.display = 'flex';
            if (daysPassed < 0) {
                noticeBox.style.background = '#EEF2FF';
                noticeBox.style.color = '#4338CA';
                noticeBox.style.border = '1px solid #C7D2FE';
                noticeBox.innerHTML = '&#9432; <strong>Advance Application:</strong> Event takes place in ' + Math.abs(daysPassed) + ' day(s). Prior authorization applies.';
            } else if (daysPassed === 0) {
                noticeBox.style.background = '#ECFDF5';
                noticeBox.style.color = '#065F46';
                noticeBox.style.border = '1px solid #A7F3D0';
                noticeBox.innerHTML = '&#10003; <strong>Timeline Status:</strong> Event ends today (0 days passed). Within the allowable 3-day submission window.';
            } else if (daysPassed <= 3) {
                noticeBox.style.background = '#ECFDF5';
                noticeBox.style.color = '#065F46';
                noticeBox.style.border = '1px solid #A7F3D0';
                noticeBox.innerHTML = '&#10003; <strong>Timeline Status:</strong> ' + daysPassed + ' day' + (daysPassed === 1 ? '' : 's') + ' passed since duty ended (Within allowable 3-day limit).';
            } else {
                noticeBox.style.background = '#FEF2F2';
                noticeBox.style.color = '#B91C1C';
                noticeBox.style.border = '1px solid #FECDD3';
                noticeBox.innerHTML = '&#9888; <strong>Timeline Violation:</strong> ' + daysPassed + ' days passed since duty ended. College rule strictly requires submission within 3 days. Late submissions are blocked.';
            }
        }

        function validateODForm() {
            const authorizedBody = document.getElementById('authorizedBodyInput').value.trim();
            const fromDateVal = document.getElementById('fromDateInput').value;
            const toDateVal = document.getElementById('toDateInput').value;
            const reason = document.getElementById('reasonText').value.trim();

            if (!authorizedBody) {
                alert("Prior Authorization Required: Please enter Authorized Body / Club & Staff Coordinator Name.");
                document.getElementById('authorizedBodyInput').focus();
                return false;
            }

            if (!fromDateVal || !toDateVal) {
                alert("Please select both 'From Date' and 'To Date'.");
                return false;
            }

            if (toDateVal < fromDateVal) {
                alert("Date Validation Failed: 'To Date' (" + toDateVal + ") cannot be earlier than 'From Date' (" + fromDateVal + ").");
                return false;
            }

            const toDate = new Date(toDateVal + 'T00:00:00');
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            const diffTime = today.getTime() - toDate.getTime();
            const daysPassed = Math.floor(diffTime / (1000 * 60 * 60 * 24));

            if (daysPassed > 3) {
                alert("Submission Rejected (Timeline Constraint): OD applications must be submitted within 3 days of completing the duty. Late submissions are not permitted.");
                return false;
            }

            if (!reason) {
                alert("Please enter Reason / Event Details.");
                document.getElementById('reasonText').focus();
                return false;
            }

            return true;
        }

        // Instant Live Search & Multi-Filter Logic
        function filterApplicationsTable() {
            const query = (document.getElementById('tableSearchInput').value || '').trim().toLowerCase();
            const statusFilter = document.getElementById('statusFilterSelect').value;
            const categoryFilter = document.getElementById('categoryFilterSelect').value.toLowerCase();

            const rows = document.querySelectorAll('#studentTableBody tr');
            let visibleCount = 0;

            rows.forEach(row => {
                if (row.id === 'noRecordsRow') return;

                const text = row.innerText.toLowerCase();
                const overall = row.getAttribute('data-overall') || '';
                const category = (row.getAttribute('data-category') || '').toLowerCase();

                let matchesQuery = !query || text.includes(query);
                let matchesStatus = (statusFilter === 'ALL') || (overall === statusFilter);
                let matchesCategory = (categoryFilter === 'all') || category.includes(categoryFilter);

                if (matchesQuery && matchesStatus && matchesCategory) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });

            document.getElementById('visibleRowsBadge').textContent = 'Showing ' + visibleCount + ' entries';
        }

        // Modal Helpers
        function closeModal(modalId) {
            const el = document.getElementById(modalId);
            if (el) el.classList.remove('active');
        }

        function openGatePassModal(row) {
            if (!row) return;
            document.getElementById('passRefId').textContent = '#OD-2026-' + row.getAttribute('data-id');
            document.getElementById('passIssueDate').textContent = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
            document.getElementById('passCategory').textContent = row.getAttribute('data-category');
            document.getElementById('passEventName').textContent = row.getAttribute('data-event');
            document.getElementById('passEventDate').textContent = row.getAttribute('data-date');
            document.getElementById('passReason').textContent = row.getAttribute('data-reason');

            document.getElementById('gatePassModal').classList.add('active');
        }

        function openAuditModal(row) {
            if (!row) return;
            const id = row.getAttribute('data-id');
            const cat = row.getAttribute('data-category');
            const event = row.getAttribute('data-event');
            const date = row.getAttribute('data-date');
            const reason = row.getAttribute('data-reason');
            const created = row.getAttribute('data-created') || 'Recently logged';
            const staff = row.getAttribute('data-staff');
            const hod = row.getAttribute('data-hod');
            const overall = row.getAttribute('data-overall');

            document.getElementById('auditRefId').textContent = '#OD-2026-' + id;
            document.getElementById('auditCategory').textContent = cat;
            document.getElementById('auditEventTitle').textContent = event;
            document.getElementById('auditAuthorized').textContent = row.getAttribute('data-authorized') || 'Official College Department / Activity';
            document.getElementById('auditDate').textContent = date;
            document.getElementById('auditCreated').textContent = created;
            document.getElementById('auditReason').textContent = reason;

            // Update Staff Stepper Node
            const stepStaff = document.getElementById('auditStepStaff');
            const nodeStaff = document.getElementById('auditNodeStaff');
            const subStaff = document.getElementById('auditSubStaff');
            stepStaff.className = 'stepper-item';

            if (staff.toLowerCase() === 'verified') {
                stepStaff.classList.add('completed');
                nodeStaff.innerHTML = '&#10003;';
                subStaff.textContent = 'Verified & Endorsed by Faculty Advisor (Prof. Jacob Mathew)';
            } else if (staff.toLowerCase() === 'rejected') {
                stepStaff.classList.add('rejected');
                nodeStaff.innerHTML = '&#10005;';
                subStaff.textContent = 'Declined by Faculty Advisor';
            } else {
                stepStaff.classList.add('active');
                nodeStaff.innerHTML = '&#9203;';
                subStaff.textContent = 'Pending Faculty Advisor Verification';
            }

            // Update HOD Stepper Node
            const stepHod = document.getElementById('auditStepHod');
            const nodeHod = document.getElementById('auditNodeHod');
            const subHod = document.getElementById('auditSubHod');
            stepHod.className = 'stepper-item';

            if (hod.toLowerCase() === 'approved') {
                stepHod.classList.add('completed');
                nodeHod.innerHTML = '&#10003;';
                subHod.textContent = 'Officially Approved by Head of Department (Dr. Alan Smith)';
            } else if (hod.toLowerCase() === 'rejected') {
                stepHod.classList.add('rejected');
                nodeHod.innerHTML = '&#10005;';
                subHod.textContent = 'Declined by Head of Department';
            } else if (staff.toLowerCase() === 'verified') {
                stepHod.classList.add('active');
                nodeHod.innerHTML = '&#9203;';
                subHod.textContent = 'Awaiting Final Approval by HOD';
            } else {
                nodeHod.innerHTML = '&#9675;';
                subHod.textContent = 'Queued behind Faculty Advisor Review';
            }

            // Update Final Outcome Stepper Node
            const stepFinal = document.getElementById('auditStepFinal');
            const nodeFinal = document.getElementById('auditNodeFinal');
            const subFinal = document.getElementById('auditSubFinal');
            stepFinal.className = 'stepper-item';

            if (overall === 'APPROVED') {
                stepFinal.classList.add('completed');
                nodeFinal.innerHTML = '&#10003;';
                subFinal.textContent = 'Official OD Gate Pass Generated & Biometric Attendance Credited';
            } else if (overall === 'REJECTED') {
                stepFinal.classList.add('rejected');
                nodeFinal.innerHTML = '&#10005;';
                subFinal.textContent = 'Application Closed without Attendance Waiver';
            } else {
                nodeFinal.innerHTML = '&#9675;';
                subFinal.textContent = 'Waiver will be credited upon HOD approval';
            }

            document.getElementById('auditModal').classList.add('active');
        }

        // Real Client-Side CSV Exporter
        function exportTableToCSV(tableId, filename) {
            const table = document.getElementById(tableId);
            if (!table) return;

            let csv = [];
            const rows = table.querySelectorAll('tr');

            for (let i = 0; i < rows.length; i++) {
                if (rows[i].id === 'noRecordsRow' || rows[i].style.display === 'none') continue;
                let row = [];
                const cols = rows[i].querySelectorAll('th, td');
                
                // Do not export the last Actions column
                const limit = (i === 0) ? cols.length - 1 : cols.length - 1;
                for (let j = 0; j < limit; j++) {
                    let text = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, ' ').replace(/"/g, '""').trim();
                    row.push('"' + text + '"');
                }
                csv.push(row.join(','));
            }

            const csvFile = new Blob([csv.join('\n')], { type: 'text/csv;charset=utf-8;' });
            const downloadLink = document.createElement('a');
            downloadLink.download = filename;
            downloadLink.href = window.URL.createObjectURL(csvFile);
            downloadLink.style.display = 'none';
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
        }

        // Real Client-Side JSON Exporter
        function exportTableToJSON() {
            const table = document.getElementById('studentTable');
            if (!table) return;

            const rows = table.querySelectorAll('tbody tr');
            const data = [];

            rows.forEach(r => {
                if (r.id === 'noRecordsRow' || r.style.display === 'none') return;
                data.push({
                    id: r.dataset.id || "",
                    rollNo: r.dataset.roll || "",
                    category: r.dataset.category || "",
                    authorizedBody: r.dataset.authorized || "",
                    eventName: r.dataset.event || "",
                    fromDate: r.dataset.from || "",
                    toDate: r.dataset.to || "",
                    daysCount: parseInt(r.dataset.days || "1", 10),
                    reason: r.dataset.reason || "",
                    staffStatus: r.dataset.staff || "",
                    hodStatus: r.dataset.hod || "",
                    overallStatus: r.dataset.overall || "",
                    createdAt: r.dataset.created || ""
                });
            });

            const jsonStr = JSON.stringify({
                system: "Digital Leave / On-Duty (OD) Application System",
                exportedAt: new Date().toISOString(),
                applicant: "<%= rollNo %>",
                totalRecords: data.length,
                records: data
            }, null, 2);

            const blob = new Blob([jsonStr], { type: 'application/json;charset=utf-8;' });
            const link = document.createElement('a');
            link.download = 'Digital_OD_Student_Applications.json';
            link.href = window.URL.createObjectURL(blob);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        // Live RESTful JSON API Modal Controller
        function openJsonApiModal(endpoint = 'api/od') {
            const modal = document.getElementById('jsonApiModal');
            const box = document.getElementById('jsonPreviewBox');
            const link = document.getElementById('openApiNewTabBtn');
            const epTag = document.getElementById('apiEndpointTag');
            if (!modal || !box) return;

            modal.style.display = 'flex';
            epTag.textContent = endpoint;
            link.href = endpoint;
            box.textContent = "Loading live data from " + endpoint + "...";

            fetch(endpoint, {
                headers: { 'Accept': 'application/json' }
            })
            .then(res => res.json())
            .then(data => {
                box.textContent = JSON.stringify(data, null, 2);
            })
            .catch(err => {
                box.textContent = "Could not fetch JSON from " + endpoint + ": " + err.message + "\n\nTip: Ensure the local Tomcat server is running and accessible.";
            });
        }

        function closeJsonApiModal() {
            const modal = document.getElementById('jsonApiModal');
            if (modal) modal.style.display = 'none';
        }

        function copyJsonToClipboard() {
            const box = document.getElementById('jsonPreviewBox');
            if (!box) return;
            navigator.clipboard.writeText(box.textContent).then(() => {
                const btn = document.getElementById('copyJsonBtn');
                if (btn) {
                    const original = btn.innerHTML;
                    btn.innerHTML = "&#10003; Copied!";
                    setTimeout(() => { btn.innerHTML = original; }, 1800);
                }
            });
        }

        // Close modal on Escape key
        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeJsonApiModal();
        });

        // Initialize on page load
        window.addEventListener('DOMContentLoaded', () => {
            setDefaultDates();
            updateCharCount();
        });
    </script>

    <!-- Interactive RESTful JSON API Modal -->
    <div id="jsonApiModal" style="display: none; position: fixed; inset: 0; background: rgba(15, 23, 42, 0.65); z-index: 9999; align-items: center; justify-content: center; padding: 20px; backdrop-filter: blur(4px);">
        <div style="background: #FFFFFF; border-radius: 12px; max-width: 720px; width: 100%; box-shadow: 0 20px 40px rgba(0,0,0,0.2); overflow: hidden; display: flex; flex-direction: column; max-height: 85vh;">
            <div style="padding: 16px 20px; border-bottom: 1px solid #E2E8F0; display: flex; align-items: center; justify-content: space-between; background: #F8FAFC;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 32px; height: 32px; border-radius: 8px; background: #EEF2FF; color: #4F46E5; display: flex; align-items: center; justify-content: center; font-family: monospace; font-weight: 800;">{ }</div>
                    <div>
                        <div style="font-weight: 800; font-size: 15px; color: #1E293B;">Live RESTful JSON API Response</div>
                        <div style="font-size: 12px; color: #64748B;">Controller: <code style="color: #4F46E5;">controller.ApiODServlet</code> &bull; <span id="apiEndpointTag" style="font-weight: 700; color: #059669;">api/od</span></div>
                    </div>
                </div>
                <button type="button" onclick="closeJsonApiModal()" style="border: none; background: transparent; font-size: 20px; cursor: pointer; color: #94A3B8; padding: 4px 8px;">&times;</button>
            </div>

            <!-- Tab Switcher -->
            <div style="padding: 10px 20px; background: #F1F5F9; display: flex; gap: 8px; border-bottom: 1px solid #E2E8F0;">
                <button type="button" onclick="openJsonApiModal('api/od')" class="btn-export-csv" style="padding: 5px 12px; font-size: 12px; background: #FFFFFF; border: 1px solid #CBD5E1; color: #1E293B; cursor: pointer;">
                    &#128196; Live OD Requests (JSON)
                </button>
                <button type="button" onclick="openJsonApiModal('api/od-policy')" class="btn-export-csv" style="padding: 5px 12px; font-size: 12px; background: #FFFFFF; border: 1px solid #CBD5E1; color: #1E293B; cursor: pointer;">
                    &#128220; Institutional Policy (JSON)
                </button>
            </div>

            <div style="padding: 16px 20px; flex: 1; overflow-y: auto;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 12px; color: #64748B;">HTTP 200 OK &bull; <code style="color: #059669;">Content-Type: application/json</code></span>
                    <button type="button" id="copyJsonBtn" onclick="copyJsonToClipboard()" style="padding: 4px 10px; font-size: 12px; border-radius: 6px; border: 1px solid #CBD5E1; background: #FFFFFF; cursor: pointer; font-weight: 600;">
                        &#128203; Copy JSON
                    </button>
                </div>
                <pre id="jsonPreviewBox" style="background: #0F172A; color: #38BDF8; padding: 14px; border-radius: 8px; font-family: 'Consolas', 'Courier New', monospace; font-size: 12.5px; line-height: 1.5; margin: 0; max-height: 360px; overflow: auto; text-align: left;"></pre>
            </div>

            <div style="padding: 12px 20px; border-top: 1px solid #E2E8F0; display: flex; justify-content: flex-end; gap: 10px; background: #F8FAFC;">
                <a id="openApiNewTabBtn" href="api/od" target="_blank" style="padding: 7px 14px; font-size: 12px; font-weight: 700; border-radius: 6px; text-decoration: none; background: #4F46E5; color: #FFFFFF; display: inline-flex; align-items: center; gap: 6px;">
                    Open API in New Tab &nearr;
                </a>
                <button type="button" onclick="closeJsonApiModal()" style="padding: 7px 14px; font-size: 12px; font-weight: 700; border-radius: 6px; border: 1px solid #CBD5E1; background: #FFFFFF; color: #475569; cursor: pointer;">
                    Close
                </button>
            </div>
        </div>
    </div>
</body>
</html>
