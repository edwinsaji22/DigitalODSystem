<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.util.List" %>
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

    if (fullName == null || fullName.isEmpty()) fullName = "Prof. Jacob Mathew";

    // Compute initials
    String initials = "JM";
    if (fullName != null && !fullName.trim().isEmpty()) {
        String[] parts = fullName.trim().split("\\s+");
        if (parts.length >= 2) {
            initials = ("" + parts[0].charAt(0) + parts[1].charAt(0)).toUpperCase();
        } else if (parts[0].length() >= 2) {
            initials = parts[0].substring(0, 2).toUpperCase();
        }
    }

    // Enforce role access: Staff and HOD can access staff dashboard
    if (!"staff".equalsIgnoreCase(userRole) && !"hod".equalsIgnoreCase(userRole)) {
        response.sendRedirect("student_dashboard.jsp");
        return;
    }

    // Fetch all student OD requests
    ODService odService = new ODServiceImpl();
    List<ODRequest> allRequests = odService.getAllODRequests();

    // Calculate metrics strictly dynamically from live database records
    int totalApplications = allRequests.size();
    int pendingVerification = 0;
    int verifiedCount = 0;
    int rejectedCount = 0;

    for (ODRequest req : allRequests) {
        if ("Verified".equalsIgnoreCase(req.getStaffStatus())) {
            verifiedCount++;
        } else if ("Rejected".equalsIgnoreCase(req.getStaffStatus())) {
            rejectedCount++;
        } else if ("Pending".equalsIgnoreCase(req.getStaffStatus())) {
            pendingVerification++;
        }
    }

    String msg = request.getParameter("msg");
%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Faculty Portal - Digital Leave/OD (On-Duty) Application System</title>
    <link rel="stylesheet" href="css/style.css">
    <style>
        .btn-action-verify {
            background-color: var(--success);
            color: #FFFFFF;
            border: none;
            padding: 6px 14px;
            font-size: 12px;
            font-weight: 700;
            border-radius: var(--radius-sm);
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .btn-action-verify:hover {
            background-color: var(--success-hover);
        }
        .btn-action-reject {
            background-color: var(--danger);
            color: #FFFFFF;
            border: none;
            padding: 6px 14px;
            font-size: 12px;
            font-weight: 700;
            border-radius: var(--radius-sm);
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .btn-action-reject:hover {
            background-color: var(--danger-hover);
        }
    </style>
</head>
<body>

    <!-- Top Navigation Bar -->
    <header class="top-nav">
        <div class="brand-section">
            <div class="brand-icon-box" style="background: linear-gradient(135deg, #10B981 0%, #059669 100%);">&#128394;</div>
            <div>
                <div class="brand-title">Digital Leave/OD (On-Duty) Application System</div>
                <div class="brand-subtitle">Academic Leave &amp; Student Service Desk</div>
            </div>
        </div>

        <div class="nav-right-actions">
            <a href="api/od" target="_blank" class="btn-criteria-nav" title="View RESTful JSON API Endpoint" style="background: rgba(16, 185, 129, 0.08); color: #059669; border: 1px solid rgba(16, 185, 129, 0.25);">
                <span style="font-family: monospace; font-size: 14px;">{ ; }</span> JSON API &nearr;
            </a>
            <a href="od_criteria.jsp" class="btn-criteria-nav" title="View Official OD Rules & Criteria">
                <span>&#128220;</span> OD Rules &amp; Criteria
            </a>
            <div class="user-profile-pill">
                <div class="avatar-circle" style="background: linear-gradient(135deg, #10B981 0%, #059669 100%);"><%= initials %></div>
                <div class="user-text-info">
                    <span class="user-display-name"><%= fullName %></span>
                    <span class="user-display-roll">Faculty Advisor</span>
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
                <h1 style="font-size: 22px; font-weight: 800; color: var(--text-primary); margin-bottom: 4px;">Faculty Advisor Portal</h1>
                <p style="font-size: 13px; color: var(--text-muted); margin: 0;">
                    Faculty Advisor: <strong><%= fullName %></strong> &bull; Department: <strong>Computer Applications</strong>
                </p>
            </div>
        </section>

        <!-- Feedback Alert Messages -->
        <% if ("verified".equals(msg)) { %>
            <div class="alert alert-success">
                &#10003; <strong>OD Request Endorsed:</strong> Application marked as Verified and forwarded to Head of Department (HOD) for final sanction.
            </div>
        <% } else if ("rejected".equals(msg)) { %>
            <div class="alert alert-error">
                &#9888; <strong>OD Request Declined:</strong> Application marked as declined. Student notification updated.
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
                <div class="kpi-value" style="color: var(--warning);"><%= pendingVerification %></div>
                <div class="kpi-footer">
                    <span>Requires Faculty Review</span>
                    <span class="kpi-tag kpi-tag-amber"><%= pendingVerification > 0 ? "Action Required" : "All Clear" %></span>
                </div>
            </div>

            <!-- 3. Approved / Verified -->
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Approved</span>
                    <div class="kpi-icon-wrap kpi-icon-success">&#10003;</div>
                </div>
                <div class="kpi-value" style="color: var(--success);"><%= verifiedCount %></div>
                <div class="kpi-footer">
                    <span>Forwarded to HOD</span>
                    <span class="kpi-tag kpi-tag-green">&#10003; Endorsed</span>
                </div>
            </div>
        </section>

        <!-- Verification Queue Table Section -->
        <section class="history-section-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 10px;">
                <div>
                    <h3 style="font-size: 16px; font-weight: 800; color: var(--text-primary); display: flex; align-items: center; gap: 8px;">
                        <span>&#128203;</span> On-Duty Application History (<span id="totalQueueCount"><%= allRequests.size() %></span> Total Records)
                    </h3>
                    <p style="font-size: 12px; color: var(--text-muted);">Real-time status of your submitted On-Duty applications.</p>
                </div>
            </div>

            <!-- Instant Search & Multi-Criteria Filtering Toolbar -->
            <div class="filter-toolbar">
                <div class="filter-left">
                    <div class="search-box-wrap">
                        <span class="search-box-icon">&#128269;</span>
                        <input type="text" id="staffSearchInput" class="search-box-input" placeholder="Search by Roll No, Student, Event, Category..." onkeyup="filterStaffTable()">
                    </div>

                    <select id="staffStatusFilter" class="filter-select" onchange="filterStaffTable()">
                        <option value="ALL">All Staff Statuses</option>
                        <option value="PENDING">Pending Staff Review</option>
                        <option value="VERIFIED">Verified / Endorsed</option>
                        <option value="REJECTED">Declined by Faculty</option>
                    </select>

                    <span class="filter-counter-badge" id="staffCountBadge">Showing <%= allRequests.size() %> entries</span>
                </div>

                <!-- One-Click Export to CSV -->
                <button type="button" class="btn-export-csv" onclick="exportTableToCSV('staffTable', 'Faculty_OD_Review_Queue.csv')">
                    <span>&#128229;</span> Export to CSV
                </button>
            </div>

            <!-- Table -->
            <div class="table-responsive">
                <table class="data-table" id="staffTable">
                    <thead>
                        <tr>
                            <th style="width: 60px;">App ID</th>
                            <th>Applicant Roll No</th>
                            <th>Student Account</th>
                            <th>Event Category</th>
                            <th>Event Name &amp; Description</th>
                            <th>Event Date</th>
                            <th>Staff Status</th>
                            <th>HOD Status</th>
                            <th style="text-align: center; min-width: 220px;">Review Action</th>
                        </tr>
                    </thead>
                    <tbody id="staffTableBody">
                        <% if (allRequests.isEmpty()) { %>
                            <tr id="staffNoRecords">
                                <td colspan="9" style="text-align: center; padding: 36px; color: var(--text-muted);">
                                    No student applications in queue.
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
                                    data-created="<%= req.getCreatedAt() != null ? req.getCreatedAt() : "" %>">
                                    <td><strong>#OD-<%= req.getId() %></strong></td>
                                    <td><strong style="color: var(--primary); font-size: 14px;"><%= req.getRollNo() %></strong></td>
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
                                        <div style="font-size: 11px; color: var(--success); font-weight: 700; margin-top: 2px;">
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
                                    <td style="text-align: center;">
                                        <div style="display: inline-flex; gap: 6px; justify-content: center; align-items: center; flex-wrap: wrap;">
                                            <% if ("Pending".equalsIgnoreCase(req.getStaffStatus())) { %>
                                                <form action="updateODStatusServlet" method="POST" style="display: inline;">
                                                    <input type="hidden" name="requestId" value="<%= req.getId() %>">
                                                    <input type="hidden" name="action" value="verify">
                                                    <button type="submit" class="btn-action-verify" title="Verify genuine participation and forward to HOD">&#10003; Verify</button>
                                                </form>
                                                <form action="updateODStatusServlet" method="POST" style="display: inline;" onsubmit="return confirm('Decline this student OD request?');">
                                                    <input type="hidden" name="requestId" value="<%= req.getId() %>">
                                                    <input type="hidden" name="action" value="reject_staff">
                                                    <button type="submit" class="btn-action-reject" title="Decline request">&#10005; Decline</button>
                                                </form>
                                            <% } else if ("Verified".equalsIgnoreCase(req.getStaffStatus())) { %>
                                                <span style="font-size: 11px; color: var(--success-text); font-weight: 700; background: var(--success-light); padding: 4px 8px; border-radius: 4px;">&#10003; Endorsed</span>
                                            <% } else { %>
                                                <span style="font-size: 11px; color: var(--danger-text); font-weight: 700; background: var(--danger-light); padding: 4px 8px; border-radius: 4px;">Declined</span>
                                            <% } %>
                                            <button type="button" class="btn-inspect" onclick="openStaffAuditModal(this.closest('tr'))" title="Inspect Application Statement &amp; Dates">
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
            <span>Staff Portal: <strong><%= fullName %></strong></span>
            <span>&bull;</span>
            <span>Academic Session 2026</span>
        </div>
    </footer>

    <!-- Application Details Modal for Faculty Advisor -->
    <div class="modal-overlay" id="staffAuditModal">
        <div class="modal-box">
            <div class="modal-box-header">
                <div class="modal-box-title">
                    <span>&#128065;</span> Student OD Application Details &amp; Verification Audit
                </div>
                <button type="button" class="modal-close-btn" onclick="closeModal('staffAuditModal')">&times;</button>
            </div>

            <div class="modal-box-body">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; background: #F8FAFC; padding: 14px; border-radius: var(--radius-md); border: 1px solid var(--border-color); margin-bottom: 20px;">
                    <div>
                        <div class="pass-field-label">Reference ID</div>
                        <div class="pass-field-val" id="staffModalRef">#OD-000</div>
                    </div>
                    <div>
                        <div class="pass-field-label">Applicant Roll Number</div>
                        <div class="pass-field-val" id="staffModalRoll" style="color: var(--primary);">-</div>
                    </div>
                    <div>
                        <div class="pass-field-label">Student Account</div>
                        <div class="pass-field-val" id="staffModalUser">-</div>
                    </div>
                    <div>
                        <div class="pass-field-label">OD Category</div>
                        <div class="pass-field-val" id="staffModalCat">-</div>
                    </div>
                    <div style="grid-column: span 2;">
                        <div class="pass-field-label">Event Title &amp; Host College</div>
                        <div class="pass-field-val" id="staffModalEvent" style="font-size: 14px;">-</div>
                    </div>
                    <div>
                        <div class="pass-field-label">Event Date / Range</div>
                        <div class="pass-field-val" id="staffModalDate">-</div>
                    </div>
                    <div>
                        <div class="pass-field-label">Submitted Timestamp</div>
                        <div class="pass-field-val" id="staffModalCreated">-</div>
                    </div>
                    <div style="grid-column: span 2;">
                        <div class="pass-field-label">Reason / Statement by Student</div>
                        <div style="font-size: 13px; color: var(--text-secondary); margin-top: 4px;" id="staffModalReason">-</div>
                    </div>
                </div>

                <div style="font-size: 13px; font-weight: 800; color: var(--text-primary); margin-bottom: 12px;">
                    Approval Workflow Status
                </div>

                <div class="audit-stepper">
                    <div class="stepper-item completed">
                        <div class="stepper-node">&#10003;</div>
                        <div class="stepper-content">
                            <div class="stepper-title">Application Submitted by Student</div>
                            <div class="stepper-sub">Logged in database &bull; Initial draft queued</div>
                        </div>
                    </div>
                    <div class="stepper-item active" id="staffStepNode">
                        <div class="stepper-node" id="staffStepIcon">&#9203;</div>
                        <div class="stepper-content">
                            <div class="stepper-title">Faculty Advisor Review</div>
                            <div class="stepper-sub" id="staffStepText">Under your evaluation desk</div>
                        </div>
                    </div>
                    <div class="stepper-item" id="staffHodStepNode">
                        <div class="stepper-node" id="staffHodStepIcon">&#9675;</div>
                        <div class="stepper-content">
                            <div class="stepper-title">Head of Department (HOD) Final Decision</div>
                            <div class="stepper-sub" id="staffHodStepText">Requires faculty advisor endorsement first</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="modal-box-footer">
                <button type="button" class="btn-secondary" onclick="closeModal('staffAuditModal')">Close</button>
            </div>
        </div>
    </div>

    <!-- Client-Side Scripts -->
    <script>
        function closeModal(modalId) {
            const el = document.getElementById(modalId);
            if (el) el.classList.remove('active');
        }

        function filterStaffTable() {
            const query = (document.getElementById('staffSearchInput').value || '').trim().toLowerCase();
            const statusFilter = document.getElementById('staffStatusFilter').value;

            const rows = document.querySelectorAll('#staffTableBody tr');
            let visible = 0;

            rows.forEach(row => {
                if (row.id === 'staffNoRecords') return;

                const text = row.innerText.toLowerCase();
                const staff = (row.getAttribute('data-staff') || '').toUpperCase();

                let matchesQuery = !query || text.includes(query);
                let matchesStatus = (statusFilter === 'ALL') || (staff === statusFilter);

                if (matchesQuery && matchesStatus) {
                    row.style.display = '';
                    visible++;
                } else {
                    row.style.display = 'none';
                }
            });

            document.getElementById('staffCountBadge').textContent = 'Showing ' + visible + ' entries';
        }

        function openStaffAuditModal(row) {
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

            document.getElementById('staffModalRef').textContent = '#OD-2026-' + id;
            document.getElementById('staffModalRoll').textContent = roll;
            document.getElementById('staffModalUser').textContent = user;
            document.getElementById('staffModalCat').textContent = cat;
            document.getElementById('staffModalEvent').textContent = event;
            document.getElementById('staffModalDate').textContent = date;
            document.getElementById('staffModalCreated').textContent = created;
            document.getElementById('staffModalReason').textContent = reason;

            const staffStepNode = document.getElementById('staffStepNode');
            const staffStepIcon = document.getElementById('staffStepIcon');
            const staffStepText = document.getElementById('staffStepText');
            staffStepNode.className = 'stepper-item';

            if (staff === 'verified') {
                staffStepNode.classList.add('completed');
                staffStepIcon.innerHTML = '&#10003;';
                staffStepText.textContent = 'Endorsed by Faculty Advisor (Prof. Jacob Mathew)';
            } else if (staff === 'rejected') {
                staffStepNode.classList.add('rejected');
                staffStepIcon.innerHTML = '&#10005;';
                staffStepText.textContent = 'Declined by Faculty Advisor';
            } else {
                staffStepNode.classList.add('active');
                staffStepIcon.innerHTML = '&#9203;';
                staffStepText.textContent = 'Pending your verification';
            }

            const staffHodStepNode = document.getElementById('staffHodStepNode');
            const staffHodStepIcon = document.getElementById('staffHodStepIcon');
            const staffHodStepText = document.getElementById('staffHodStepText');
            staffHodStepNode.className = 'stepper-item';

            if (hod === 'approved') {
                staffHodStepNode.classList.add('completed');
                staffHodStepIcon.innerHTML = '&#10003;';
                staffHodStepText.textContent = 'Approved by Head of Department (Dr. Alan Smith)';
            } else if (hod === 'rejected') {
                staffHodStepNode.classList.add('rejected');
                staffHodStepIcon.innerHTML = '&#10005;';
                staffHodStepText.textContent = 'Declined by Head of Department';
            } else if (staff === 'verified') {
                staffHodStepNode.classList.add('active');
                staffHodStepIcon.innerHTML = '&#9203;';
                staffHodStepText.textContent = 'Awaiting HOD Final Approval';
            } else {
                staffHodStepIcon.innerHTML = '&#9675;';
                staffHodStepText.textContent = 'Requires faculty verification first';
            }

            document.getElementById('staffAuditModal').classList.add('active');
        }

        // CSV Exporter for Faculty
        function exportTableToCSV(tableId, filename) {
            const table = document.getElementById(tableId);
            if (!table) return;

            let csv = [];
            const rows = table.querySelectorAll('tr');

            for (let i = 0; i < rows.length; i++) {
                if (rows[i].id === 'staffNoRecords' || rows[i].style.display === 'none') continue;
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
