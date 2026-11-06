<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.util.List" %>
<%@ page import="java.util.ArrayList" %>
<%@ page import="model.ODRequest" %>
<%@ page import="service.ODService" %>
<%@ page import="service.ODServiceImpl" %>

<%
    // Verify session authentication
    if (session == null || session.getAttribute("loggedInUser") == null) {
        response.sendRedirect("login.html?unauthorized=1");
        return;
    }

    String loggedInUser = (String) session.getAttribute("loggedInUser");
    String userRole = (String) session.getAttribute("userRole");
    String fullName = (String) session.getAttribute("fullName");

    if (fullName == null || fullName.isEmpty()) fullName = "Dr. Alan Smith";

    // Compute initials
    String initials = "AS";
    if (fullName != null && !fullName.trim().isEmpty()) {
        String[] parts = fullName.trim().split("\\s+");
        if (parts.length >= 2) {
            initials = ("" + parts[0].charAt(0) + parts[1].charAt(0)).toUpperCase();
        } else if (parts[0].length() >= 2) {
            initials = parts[0].substring(0, 2).toUpperCase();
        }
    }

    // Enforce role access: Only HOD can access HOD dashboard
    if (!"hod".equalsIgnoreCase(userRole)) {
        response.sendRedirect("staff".equalsIgnoreCase(userRole) ? "staff_dashboard.jsp" : "student_dashboard.jsp");
        return;
    }

    // Fetch all OD requests
    ODService odService = new ODServiceImpl();
    List<ODRequest> allRequests = odService.getAllODRequests();

    // Partition lists and calculate departmental metrics dynamically
    List<ODRequest> pendingHodApprovalList = new ArrayList<>();
    int awaitingApprovalCount = 0;
    int approvedCount = 0;
    int rejectedCount = 0;
    int totalCount = allRequests.size();

    for (ODRequest req : allRequests) {
        if ("Verified".equalsIgnoreCase(req.getStaffStatus()) && "Pending".equalsIgnoreCase(req.getHodStatus())) {
            pendingHodApprovalList.add(req);
            awaitingApprovalCount++;
        }
        if ("Approved".equalsIgnoreCase(req.getHodStatus())) {
            approvedCount++;
        } else if ("Rejected".equalsIgnoreCase(req.getHodStatus()) || "Rejected".equalsIgnoreCase(req.getStaffStatus())) {
            rejectedCount++;
        }
    }

    String msg = request.getParameter("msg");
%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HOD Sanction Portal - Digital Leave/OD (On-Duty) Application System</title>
    <link rel="stylesheet" href="css/style.css">
    <style>
        .btn-action-grant {
            background-color: var(--primary);
            color: #FFFFFF;
            border: none;
            padding: 7px 16px;
            font-size: 12px;
            font-weight: 700;
            border-radius: var(--radius-sm);
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .btn-action-grant:hover {
            background-color: var(--primary-hover);
        }
        .btn-action-decline {
            background-color: var(--danger);
            color: #FFFFFF;
            border: none;
            padding: 7px 16px;
            font-size: 12px;
            font-weight: 700;
            border-radius: var(--radius-sm);
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .btn-action-decline:hover {
            background-color: var(--danger-hover);
        }
    </style>
</head>
<body>

    <!-- Top Navigation Bar -->
    <header class="top-nav">
        <div class="brand-section">
            <div class="brand-icon-box" style="background: linear-gradient(135deg, #6366F1 0%, #4338CA 100%);">&#9878;</div>
            <div>
                <div class="brand-title">Digital Leave/OD (On-Duty) Application System</div>
                <div class="brand-subtitle">Academic Leave &amp; Student Service Desk</div>
            </div>
        </div>

        <div class="nav-right-actions">
            <a href="api/od" target="_blank" class="btn-criteria-nav" title="View RESTful JSON API Endpoint" style="background: rgba(99, 102, 241, 0.08); color: #4F46E5; border: 1px solid rgba(99, 102, 241, 0.25);">
                <span style="font-family: monospace; font-size: 14px;">{ ; }</span> JSON API &nearr;
            </a>
            <a href="od_criteria.jsp" class="btn-criteria-nav" title="View Official OD Rules & Criteria">
                <span>&#128220;</span> OD Rules &amp; Criteria
            </a>
            <div class="user-profile-pill">
                <div class="avatar-circle" style="background: linear-gradient(135deg, #6366F1 0%, #4338CA 100%);"><%= initials %></div>
                <div class="user-text-info">
                    <span class="user-display-name"><%= fullName %></span>
                    <span class="user-display-roll">Head of Department</span>
                </div>
            </div>
            <a href="logoutServlet" class="btn-logout-clean" title="Sign out">
                <span>&#10150;</span> Logout
            </a>
        </div>
    </header>

    <main class="main-wrapper" style="max-width: 1000px; margin: 0 auto; padding: 24px 20px; width: 100%;">

        <!-- Clean Welcome Banner -->
        <section class="welcome-banner-card" style="margin-bottom: 20px; padding: 20px 24px;">
            <div class="welcome-left">
                <h1 style="font-size: 22px; font-weight: 800; color: var(--text-primary); margin-bottom: 4px;">Head of Department (HOD) Portal</h1>
                <p style="font-size: 13px; color: var(--text-muted); margin: 0;">
                    Department Authority: <strong><%= fullName %></strong> &bull; Department: <strong>Master of Computer Applications (MCA)</strong>
                </p>
            </div>
        </section>

        <!-- Feedback Alert Messages -->
        <% if ("approved".equals(msg)) { %>
            <div class="alert alert-success">
                &#10003; <strong>Official OD Granted:</strong> The student's On-Duty application has received final departmental approval and attendance credit waiver is recorded.
            </div>
        <% } else if ("rejected".equals(msg)) { %>
            <div class="alert alert-error">
                &#9888; <strong>OD Declined:</strong> Application marked as declined by Head of Department.
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
                <div class="kpi-value"><%= totalCount %></div>
                <div class="kpi-footer">
                    <span>Submitted Requests</span>
                    <span class="kpi-tag kpi-tag-green">Active</span>
                </div>
            </div>

            <!-- 2. Pending Verification -->
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Pending Final Sanction</span>
                    <div class="kpi-icon-wrap kpi-icon-warning">&#9889;</div>
                </div>
                <div class="kpi-value" style="color: var(--warning);"><%= awaitingApprovalCount %></div>
                <div class="kpi-footer">
                    <span>Staff-Endorsed Queue</span>
                    <span class="kpi-tag kpi-tag-amber"><%= awaitingApprovalCount > 0 ? "Requires Action" : "All Clear" %></span>
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
                    <span>Sanction Passes Issued</span>
                    <span class="kpi-tag kpi-tag-green">&#10003; Approved</span>
                </div>
            </div>
        </section>

        <!-- SECTION 1: Action Required: Staff-Verified OD Applications -->
        <section class="history-section-card" style="border-top: 4px solid var(--primary); margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 10px;">
                <div>
                    <h3 style="font-size: 16px; font-weight: 800; color: var(--text-primary); display: flex; align-items: center; gap: 8px;">
                        <span>&#9889;</span> Action Required: Staff-Verified Applications (<%= pendingHodApprovalList.size() %> Pending Final Decision)
                    </h3>
                    <p style="font-size: 12px; color: var(--text-muted);">Applications endorsed by faculty advisors requiring final departmental sanction.</p>
                </div>
                <span class="badge-pending-pill">&#9203; <%= pendingHodApprovalList.size() %> Pending Decision</span>
            </div>

            <div class="table-responsive">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th style="width: 60px;">App ID</th>
                            <th>Applicant Roll No</th>
                            <th>Student Account</th>
                            <th>Category</th>
                            <th>Event Details &amp; Purpose</th>
                            <th>Dates</th>
                            <th>Faculty Endorsement</th>
                            <th style="text-align: center; min-width: 250px;">HOD Final Decision</th>
                        </tr>
                    </thead>
                    <tbody>
                        <% if (pendingHodApprovalList.isEmpty()) { %>
                            <tr>
                                <td colspan="8" style="text-align: center; padding: 32px; color: var(--text-muted);">
                                    <div style="font-size: 24px; margin-bottom: 6px;">&#10003;</div>
                                    No applications currently awaiting HOD decision. All staff-verified requests have been reviewed.
                                </td>
                            </tr>
                        <% } else { %>
                            <% for (ODRequest req : pendingHodApprovalList) { %>
                                <tr data-id="<%= req.getId() %>"
                                    data-roll="<%= req.getRollNo() %>"
                                    data-student="<%= req.getStudentUsername() %>"
                                    data-category="<%= req.getEventType() %>"
                                    data-event="<%= req.getEventName() %>"
                                    data-date="<%= req.getEventDate() %>"
                                    data-reason="<%= req.getReason() %>"
                                    data-staff="<%= req.getStaffStatus() %>"
                                    data-hod="<%= req.getHodStatus() %>"
                                    data-created="<%= req.getCreatedAt() != null ? req.getCreatedAt() : "" %>">
                                    <td><strong>#OD-<%= req.getId() %></strong></td>
                                    <td><strong style="color: var(--primary); font-size: 14px;"><%= req.getRollNo() %></strong></td>
                                    <td><%= req.getStudentUsername() %></td>
                                    <td><strong><%= req.getEventType() %></strong></td>
                                    <td>
                                        <div><strong><%= req.getEventName() %></strong></div>
                                        <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px;"><%= req.getReason() %></div>
                                    </td>
                                    <td>
                                        <div style="font-weight: 700;"><%= req.getFromDate() != null ? req.getFromDate() : req.getEventDate() %></div>
                                        <% if (req.getToDate() != null && !req.getToDate().equals(req.getFromDate())) { %>
                                            <div style="font-size: 11px; color: var(--text-muted);">to <%= req.getToDate() %></div>
                                        <% } %>
                                        <div style="font-size: 11px; color: var(--purple); font-weight: 700; margin-top: 2px;">
                                            <%= req.getDaysCount() %> <%= req.getDaysCount() == 1 ? "Day" : "Days" %>
                                        </div>
                                    </td>
                                    <td><span class="badge-approved-pill">&#10003; Verified by Faculty</span></td>
                                    <td style="text-align: center;">
                                        <div style="display: inline-flex; gap: 6px; justify-content: center; align-items: center; flex-wrap: wrap;">
                                            <form action="updateODStatusServlet" method="POST" style="display: inline;">
                                                <input type="hidden" name="requestId" value="<%= req.getId() %>">
                                                <input type="hidden" name="action" value="approve">
                                                <button type="submit" class="btn-action-grant" title="Grant official On-Duty">&#10003; Grant OD</button>
                                            </form>
                                            <form action="updateODStatusServlet" method="POST" style="display: inline;" onsubmit="return confirm('Decline this student OD request?');">
                                                <input type="hidden" name="requestId" value="<%= req.getId() %>">
                                                <input type="hidden" name="action" value="reject_hod">
                                                <button type="submit" class="btn-action-decline" title="Decline request">&#10005; Decline</button>
                                            </form>
                                            <button type="button" class="btn-inspect" onclick="openHodAuditModal(this.closest('tr'))" title="Inspect Application Statement">
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

        <!-- SECTION 2: Complete Departmental OD Archive Table -->
        <section class="history-section-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 10px;">
                <div>
                    <h3 style="font-size: 16px; font-weight: 800; color: var(--text-primary); display: flex; align-items: center; gap: 8px;">
                        <span>&#128203;</span> On-Duty Application History (<span id="totalHodArchiveCount"><%= allRequests.size() %></span> Total Records)
                    </h3>
                    <p style="font-size: 12px; color: var(--text-muted);">Real-time status of your submitted On-Duty applications.</p>
                </div>
            </div>

            <!-- Instant Search & Multi-Criteria Filtering Toolbar -->
            <div class="filter-toolbar">
                <div class="filter-left">
                    <div class="search-box-wrap">
                        <span class="search-box-icon">&#128269;</span>
                        <input type="text" id="hodArchiveSearch" class="search-box-input" placeholder="Search archive by Roll No, Student, Event, Category..." onkeyup="filterHodArchiveTable()">
                    </div>

                    <select id="hodArchiveStatus" class="filter-select" onchange="filterHodArchiveTable()">
                        <option value="ALL">All Outcomes</option>
                        <option value="APPROVED">Final Approved</option>
                        <option value="PENDING">In Progress</option>
                        <option value="REJECTED">Declined</option>
                    </select>

                    <span class="filter-counter-badge" id="hodCountBadge">Showing <%= allRequests.size() %> entries</span>
                </div>

                <!-- One-Click Export to CSV -->
                <button type="button" class="btn-export-csv" onclick="exportTableToCSV('hodArchiveTable', 'Departmental_OD_Archive.csv')">
                    <span>&#128229;</span> Export to CSV
                </button>
            </div>

            <div class="table-responsive">
                <table class="data-table" id="hodArchiveTable">
                    <thead>
                        <tr>
                            <th style="width: 60px;">App ID</th>
                            <th>Applicant Roll No</th>
                            <th>Student</th>
                            <th>Category</th>
                            <th>Event Details</th>
                            <th>Date</th>
                            <th>Staff Status</th>
                            <th>HOD Status</th>
                            <th>Final Outcome</th>
                            <th style="text-align: center; min-width: 150px;">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="hodArchiveBody">
                        <% if (allRequests.isEmpty()) { %>
                            <tr id="hodNoRecords">
                                <td colspan="10" style="text-align: center; padding: 28px; color: var(--text-muted);">
                                    No records in departmental archive.
                                </td>
                            </tr>
                        <% } else { %>
                            <% for (ODRequest req : allRequests) { %>
                                <tr data-id="<%= req.getId() %>"
                                    data-roll="<%= req.getRollNo() %>"
                                    data-student="<%= req.getStudentUsername() %>"
                                    data-category="<%= req.getEventType() %>"
                                    data-event="<%= req.getEventName() %>"
                                    data-date="<%= req.getEventDate() %>"
                                    data-reason="<%= req.getReason() %>"
                                    data-staff="<%= req.getStaffStatus() %>"
                                    data-hod="<%= req.getHodStatus() %>"
                                    data-overall="<%= req.isFinalApproved() ? "APPROVED" : (req.isAnyRejected() ? "REJECTED" : "PENDING") %>"
                                    data-created="<%= req.getCreatedAt() != null ? req.getCreatedAt() : "" %>">
                                    <td><strong>#OD-<%= req.getId() %></strong></td>
                                    <td><strong style="color: var(--primary);"><%= req.getRollNo() %></strong></td>
                                    <td><%= req.getStudentUsername() %></td>
                                    <td><strong><%= req.getEventType() %></strong></td>
                                    <td>
                                        <div><strong><%= req.getEventName() %></strong></div>
                                        <% if (req.getAuthorizedBody() != null && !req.getAuthorizedBody().isEmpty()) { %>
                                            <div style="font-size: 11px; color: var(--primary); font-weight: 700; margin-top: 2px;">&#127891; Authorized: <%= req.getAuthorizedBody() %></div>
                                        <% } %>
                                        <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px;"><%= req.getReason() %></div>
                                    </td>
                                    <td>
                                        <div style="font-weight: 700;"><%= req.getFromDate() != null ? req.getFromDate() : req.getEventDate() %></div>
                                        <% if (req.getToDate() != null && !req.getToDate().equals(req.getFromDate())) { %>
                                            <div style="font-size: 11px; color: var(--text-muted);">to <%= req.getToDate() %></div>
                                        <% } %>
                                        <div style="font-size: 11px; color: var(--purple); font-weight: 700; margin-top: 2px;">
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
                                            <span class="badge-approved-pill" style="font-weight: 800;">&#9733; OD Granted</span>
                                        <% } else if (req.isAnyRejected()) { %>
                                            <span class="badge-declined-pill">Declined</span>
                                        <% } else { %>
                                            <span class="badge-pending-pill">In Progress</span>
                                        <% } %>
                                    </td>
                                    <td style="text-align: center;">
                                        <div style="display: inline-flex; gap: 6px; justify-content: center; align-items: center;">
                                            <% if (req.isFinalApproved()) { %>
                                                <button type="button" class="btn-pass" onclick="openHodGatePassModal(this.closest('tr'))" title="View & Print Official Gate Pass">
                                                    <span>&#127915;</span> Pass
                                                </button>
                                            <% } %>
                                            <button type="button" class="btn-inspect" onclick="openHodAuditModal(this.closest('tr'))" title="Inspect Application Statement &amp; Trail">
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
            <span>HOD Authority: <strong><%= fullName %></strong></span>
            <span>&bull;</span>
            <span>Academic Session 2026</span>
        </div>
    </footer>

    <!-- Official Gate Pass Modal for HOD -->
    <div class="modal-overlay" id="hodGatePassModal">
        <div class="modal-box">
            <div class="modal-box-header">
                <div class="modal-box-title">
                    <span>&#127915;</span> Official Digital OD Gate Pass (HOD Sanctioned)
                </div>
                <button type="button" class="modal-close-btn" onclick="closeModal('hodGatePassModal')">&times;</button>
            </div>

            <div class="modal-box-body">
                <div class="official-pass-sheet">
                    <div class="pass-header">
                        <div class="pass-institute-name">College of Engineering &amp; Technology</div>
                        <div class="pass-department-name">Autonomous Academic Institution &bull; Affiliated to University</div>
                        <div class="pass-badge-title">Official On-Duty (OD) Sanction Pass</div>
                    </div>

                    <div class="pass-ref-row">
                        <span>Ref ID: <strong id="hodPassRef">#OD-2026-000</strong></span>
                        <span>Date Issued: <strong id="hodPassDate">Today</strong></span>
                    </div>

                    <div class="pass-grid-2">
                        <div>
                            <div class="pass-field-label">Student Account</div>
                            <div class="pass-field-val" id="hodPassUser">-</div>
                        </div>
                        <div>
                            <div class="pass-field-label">Roll / Register No</div>
                            <div class="pass-field-val" id="hodPassRoll" style="color: var(--primary);">-</div>
                        </div>
                        <div>
                            <div class="pass-field-label">Department</div>
                            <div class="pass-field-val">Computer Applications (MCA)</div>
                        </div>
                        <div>
                            <div class="pass-field-label">OD Category</div>
                            <div class="pass-field-val" id="hodPassCat">-</div>
                        </div>
                        <div>
                            <div class="pass-field-label">Event Valid Date</div>
                            <div class="pass-field-val" id="hodPassEventDate">-</div>
                        </div>
                        <div>
                            <div class="pass-field-label">Sanction Status</div>
                            <div class="pass-field-val" style="color: var(--success);">&#10003; Approved &amp; Attendance Credited</div>
                        </div>
                    </div>

                    <div class="pass-purpose-box">
                        <div class="pass-field-label">Event Title &amp; Host Institution</div>
                        <div class="pass-field-val" id="hodPassEventName" style="font-size: 13px;">-</div>
                        <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;" id="hodPassReason">-</div>
                    </div>

                    <div class="pass-verification-footer">
                        <div class="qr-code-box" title="Scan to verify OD Gate Pass">
                            <svg width="66" height="66" viewBox="0 0 33 33" shape-rendering="crispEdges">
                                <path fill="#0F172A" d="M0,0 h7v7 h-7z M1,1 v5 h5 v-5z M2,2 h3 v3 h-3z M26,0 h7v7 h-7z M27,1 v5 h5 v-5z M28,2 h3 v3 h-3z M0,26 h7v7 h-7z M1,27 v5 h5 v-5z M2,28 h3 v3 h-3z M9,1 h2v1 h-2z M13,1 h1v1 h-1z M16,1 h2v1 h-2z M20,1 h3v1 h-3z M10,3 h1v1 h-1z M14,3 h2v1 h-2z M18,3 h1v1 h-1z M22,3 h2v1 h-2z M8,5 h2v1 h-2z M12,5 h3v1 h-3z M17,5 h2v1 h-2z M21,5 h2v1 h-2z M9,8 h2v1 h-2z M13,8 h1v1 h-1z M16,8 h3v1 h-3z M21,8 h2v1 h-2z M24,8 h2v1 h-2z M8,10 h1v1 h-1z M11,10 h3v1 h-3z M16,10 h1v1 h-1z M19,10 h2v1 h-2z M23,10 h3v1 h-3z M28,10 h3v1 h-3z M9,12 h2v1 h-2z M13,12 h2v1 h-2z M17,12 h1v1 h-1z M20,12 h3v1 h-3z M25,12 h1v1 h-1z M28,12 h2v1 h-2z M8,14 h2v1 h-2z M12,14 h1v1 h-1z M15,14 h3v1 h-3z M20,14 h2v1 h-2z M24,14 h3v1 h-3z M9,16 h3v1 h-3z M14,16 h2v1 h-2z M18,16 h2v1 h-2z M22,16 h1v1 h-1z M25,16 h2v1 h-2z M29,16 h2v1 h-2z M8,18 h1v1 h-1z M11,18 h2v1 h-2z M15,18 h2v1 h-2z M19,18 h1v1 h-1z M22,18 h3v1 h-3z M27,18 h2v1 h-2z M9,20 h2v1 h-2z M13,20 h3v1 h-3z M18,20 h1v1 h-1z M21,20 h2v1 h-2z M25,20 h1v1 h-1z M28,20 h3v1 h-3z M8,22 h3v1 h-3z M13,22 h1v1 h-1z M16,22 h2v1 h-2z M20,22 h1v1 h-1z M23,22 h2v1 h-2z M27,22 h1v1 h-1z M29,22 h2v1 h-2z M9,24 h1v1 h-1z M12,24 h2v1 h-2z M16,24 h3v1 h-3z M21,24 h2v1 h-2z M25,24 h3v1 h-3z M9,27 h3v1 h-3z M14,27 h1v1 h-1z M17,27 h2v1 h-2z M21,27 h2v1 h-2z M25,27 h1v1 h-1z M28,27 h2v1 h-2z M8,29 h2v1 h-2z M12,29 h3v1 h-3z M17,29 h1v1 h-1z M20,29 h3v1 h-3z M25,29 h2v1 h-2z M29,29 h1v1 h-1z M9,31 h1v1 h-1z M12,31 h2v1 h-2z M16,31 h3v1 h-3z M21,31 h1v1 h-1z M24,31 h2v1 h-2z M28,31 h3v1 h-3z" />
                            </svg>
                        </div>

                        <div>
                            <span class="pass-stamp-approved">&#10003; HOD SANCTIONED</span>
                        </div>

                        <div class="pass-sign-wrap">
                            <div>Faculty Advisor: <strong>Verified</strong></div>
                            <div style="margin-top: 4px;">Sanctioned By: <strong>Dr. Alan Smith (HOD)</strong></div>
                            <div style="color: var(--text-light); font-size: 10px; margin-top: 2px;">Official Departmental Seal</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="modal-box-footer">
                <button type="button" class="btn-secondary" onclick="closeModal('hodGatePassModal')">Close</button>
                <button type="button" class="btn-submit-primary" onclick="window.print()">
                    <span>&#128424;</span> Print OD Pass
                </button>
            </div>
        </div>
    </div>

    <!-- Application Details Modal for HOD -->
    <div class="modal-overlay" id="hodAuditModal">
        <div class="modal-box">
            <div class="modal-box-header">
                <div class="modal-box-title">
                    <span>&#128065;</span> Application Inspection &amp; Multi-Tier Trail
                </div>
                <button type="button" class="modal-close-btn" onclick="closeModal('hodAuditModal')">&times;</button>
            </div>

            <div class="modal-box-body">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; background: #F8FAFC; padding: 14px; border-radius: var(--radius-md); border: 1px solid var(--border-color); margin-bottom: 20px;">
                    <div>
                        <div class="pass-field-label">Reference ID</div>
                        <div class="pass-field-val" id="auditDetailRef">#OD-000</div>
                    </div>
                    <div>
                        <div class="pass-field-label">Applicant Roll Number</div>
                        <div class="pass-field-val" id="auditDetailRoll" style="color: var(--primary);">-</div>
                    </div>
                    <div>
                        <div class="pass-field-label">Student Username</div>
                        <div class="pass-field-val" id="auditDetailUser">-</div>
                    </div>
                    <div>
                        <div class="pass-field-label">OD Category</div>
                        <div class="pass-field-val" id="auditDetailCat">-</div>
                    </div>
                    <div style="grid-column: span 2;">
                        <div class="pass-field-label">Event Details</div>
                        <div class="pass-field-val" id="auditDetailEvent" style="font-size: 14px;">-</div>
                    </div>
                    <div>
                        <div class="pass-field-label">Event Date / Range</div>
                        <div class="pass-field-val" id="auditDetailDate">-</div>
                    </div>
                    <div>
                        <div class="pass-field-label">Logged Timestamp</div>
                        <div class="pass-field-val" id="auditDetailCreated">-</div>
                    </div>
                    <div style="grid-column: span 2;">
                        <div class="pass-field-label">Student Reason / Statement</div>
                        <div style="font-size: 13px; color: var(--text-secondary); margin-top: 4px;" id="auditDetailReason">-</div>
                    </div>
                </div>

                <div style="font-size: 13px; font-weight: 800; color: var(--text-primary); margin-bottom: 12px;">
                    Multi-Tier Academic Approval Progress
                </div>

                <div class="audit-stepper">
                    <div class="stepper-item completed">
                        <div class="stepper-node">&#10003;</div>
                        <div class="stepper-content">
                            <div class="stepper-title">Application Submitted by Student</div>
                            <div class="stepper-sub">Logged in database &bull; Initial draft queued</div>
                        </div>
                    </div>
                    <div class="stepper-item" id="auditHodStaffNode">
                        <div class="stepper-node" id="auditHodStaffIcon">&#9203;</div>
                        <div class="stepper-content">
                            <div class="stepper-title">Faculty Advisor Review</div>
                            <div class="stepper-sub" id="auditHodStaffText">Faculty evaluation</div>
                        </div>
                    </div>
                    <div class="stepper-item" id="auditHodFinalNode">
                        <div class="stepper-node" id="auditHodFinalIcon">&#9675;</div>
                        <div class="stepper-content">
                            <div class="stepper-title">Head of Department (HOD) Final Sanction</div>
                            <div class="stepper-sub" id="auditHodFinalText">Departmental authority clearance</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="modal-box-footer">
                <button type="button" class="btn-secondary" onclick="closeModal('hodAuditModal')">Close</button>
            </div>
        </div>
    </div>

    <!-- Client-Side Scripts -->
    <script>
        function closeModal(modalId) {
            const el = document.getElementById(modalId);
            if (el) el.classList.remove('active');
        }

        function filterHodArchiveTable() {
            const query = (document.getElementById('hodArchiveSearch').value || '').trim().toLowerCase();
            const statusFilter = document.getElementById('hodArchiveStatus').value;

            const rows = document.querySelectorAll('#hodArchiveBody tr');
            let visible = 0;

            rows.forEach(row => {
                if (row.id === 'hodNoRecords') return;

                const text = row.innerText.toLowerCase();
                const overall = (row.getAttribute('data-overall') || '').toUpperCase();

                let matchesQuery = !query || text.includes(query);
                let matchesStatus = (statusFilter === 'ALL') || (overall === statusFilter);

                if (matchesQuery && matchesStatus) {
                    row.style.display = '';
                    visible++;
                } else {
                    row.style.display = 'none';
                }
            });

            document.getElementById('hodCountBadge').textContent = 'Showing ' + visible + ' entries';
        }

        function openHodGatePassModal(row) {
            if (!row) return;
            document.getElementById('hodPassRef').textContent = '#OD-2026-' + row.getAttribute('data-id');
            document.getElementById('hodPassDate').textContent = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
            document.getElementById('hodPassUser').textContent = row.getAttribute('data-student');
            document.getElementById('hodPassRoll').textContent = row.getAttribute('data-roll');
            document.getElementById('hodPassCat').textContent = row.getAttribute('data-category');
            document.getElementById('hodPassEventName').textContent = row.getAttribute('data-event');
            document.getElementById('hodPassEventDate').textContent = row.getAttribute('data-date');
            document.getElementById('hodPassReason').textContent = row.getAttribute('data-reason');

            document.getElementById('hodGatePassModal').classList.add('active');
        }

        function openHodAuditModal(row) {
            if (!row) return;
            const id = row.getAttribute('data-id');
            const roll = row.getAttribute('data-roll');
            const user = row.getAttribute('data-student');
            const cat = row.getAttribute('data-category');
            const event = row.getAttribute('data-event');
            const date = row.getAttribute('data-date');
            const reason = row.getAttribute('data-reason');
            const created = row.getAttribute('data-created') || 'Recently logged';
            const staff = (row.getAttribute('data-staff') || 'Pending').toLowerCase();
            const hod = (row.getAttribute('data-hod') || 'Pending').toLowerCase();

            document.getElementById('auditDetailRef').textContent = '#OD-2026-' + id;
            document.getElementById('auditDetailRoll').textContent = roll;
            document.getElementById('auditDetailUser').textContent = user;
            document.getElementById('auditDetailCat').textContent = cat;
            document.getElementById('auditDetailEvent').textContent = event;
            document.getElementById('auditDetailDate').textContent = date;
            document.getElementById('auditDetailCreated').textContent = created;
            document.getElementById('auditDetailReason').textContent = reason;

            const staffNode = document.getElementById('auditHodStaffNode');
            const staffIcon = document.getElementById('auditHodStaffIcon');
            const staffText = document.getElementById('auditHodStaffText');
            staffNode.className = 'stepper-item';

            if (staff === 'verified') {
                staffNode.classList.add('completed');
                staffIcon.innerHTML = '&#10003;';
                staffText.textContent = 'Endorsed by Faculty Advisor (Prof. Jacob Mathew)';
            } else if (staff === 'rejected') {
                staffNode.classList.add('rejected');
                staffIcon.innerHTML = '&#10005;';
                staffText.textContent = 'Declined by Faculty Advisor';
            } else {
                staffNode.classList.add('active');
                staffIcon.innerHTML = '&#9203;';
                staffText.textContent = 'Pending Faculty Advisor Review';
            }

            const hodNode = document.getElementById('auditHodFinalNode');
            const hodIcon = document.getElementById('auditHodFinalIcon');
            const hodText = document.getElementById('auditHodFinalText');
            hodNode.className = 'stepper-item';

            if (hod === 'approved') {
                hodNode.classList.add('completed');
                hodIcon.innerHTML = '&#10003;';
                hodText.textContent = 'Official OD Sanctioned by Head of Department (Dr. Alan Smith)';
            } else if (hod === 'rejected') {
                hodNode.classList.add('rejected');
                hodIcon.innerHTML = '&#10005;';
                hodText.textContent = 'Declined by Head of Department';
            } else if (staff === 'verified') {
                hodNode.classList.add('active');
                hodIcon.innerHTML = '&#9203;';
                hodText.textContent = 'Awaiting your final sanction';
            } else {
                hodIcon.innerHTML = '&#9675;';
                hodText.textContent = 'Pending preceding faculty endorsement';
            }

            document.getElementById('hodAuditModal').classList.add('active');
        }

        // CSV Exporter for HOD
        function exportTableToCSV(tableId, filename) {
            const table = document.getElementById(tableId);
            if (!table) return;

            let csv = [];
            const rows = table.querySelectorAll('tr');

            for (let i = 0; i < rows.length; i++) {
                if (rows[i].id === 'hodNoRecords' || rows[i].style.display === 'none') continue;
                let row = [];
                const cols = rows[i].querySelectorAll('th, td');
                
                const limit = cols.length - 1; // skip Actions column
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
    </script>
</body>
</html>
