<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%
    String userRole = (session != null) ? (String) session.getAttribute("userRole") : null;
    String dashboardUrl = "login.html";
    if ("student".equalsIgnoreCase(userRole)) {
        dashboardUrl = "student_dashboard.jsp";
    } else if ("staff".equalsIgnoreCase(userRole)) {
        dashboardUrl = "staff_dashboard.jsp";
    } else if ("hod".equalsIgnoreCase(userRole)) {
        dashboardUrl = "hod_dashboard.jsp";
    }
%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Official On-Duty (OD) Rules &amp; Criteria</title>
    <link rel="stylesheet" href="css/style.css">
    <style>
        .criteria-container {
            max-width: 860px;
            margin: 32px auto 48px auto;
            padding: 0 20px;
            width: 100%;
        }

        .criteria-header {
            margin-bottom: 28px;
            text-align: left;
        }

        .criteria-header-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background-color: var(--primary-light);
            color: var(--primary);
            border: 1px solid var(--primary-border);
            padding: 4px 12px;
            border-radius: var(--radius-full);
            font-size: 12px;
            font-weight: 700;
            margin-bottom: 12px;
        }

        .criteria-title {
            font-size: 26px;
            font-weight: 800;
            color: var(--text-primary);
            letter-spacing: -0.5px;
            line-height: 1.3;
            margin-bottom: 8px;
        }

        .criteria-subtitle {
            font-size: 14px;
            color: var(--text-muted);
            line-height: 1.6;
        }

        .rules-list {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .rule-card {
            background-color: #FFFFFF;
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 22px 26px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
            display: flex;
            align-items: flex-start;
            gap: 20px;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }

        .rule-card:hover {
            border-color: var(--primary-border);
            box-shadow: 0 6px 18px rgba(79, 70, 229, 0.06);
        }

        .rule-number-pill {
            width: 40px;
            height: 40px;
            border-radius: var(--radius-md);
            background-color: var(--primary-light);
            color: var(--primary);
            font-size: 16px;
            font-weight: 800;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            border: 1px solid var(--primary-border);
        }

        .rule-content {
            flex: 1;
        }

        .rule-heading {
            font-size: 16px;
            font-weight: 800;
            color: var(--text-primary);
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .rule-desc {
            font-size: 13.5px;
            color: var(--text-secondary);
            line-height: 1.6;
        }

        .rule-enforcement-tag {
            font-size: 10.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 2px 7px;
            border-radius: 4px;
            background-color: #F1F5F9;
            color: var(--text-muted);
        }

        .tag-strict {
            background-color: #FEF2F2;
            color: var(--danger-text);
            border: 1px solid var(--danger-border);
        }

        .tag-mandatory {
            background-color: #ECFDF5;
            color: var(--success-text);
            border: 1px solid var(--success-border);
        }
    </style>
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

        <div class="nav-right-actions">
            <a href="<%= dashboardUrl %>" class="btn-criteria-nav" style="background-color: var(--primary); color: #FFFFFF; border-color: var(--primary);">
                <span>&larr;</span> Back to Dashboard
            </a>
        </div>
    </header>

    <main class="criteria-container">
        <!-- Header -->
        <div class="criteria-header">
            <div class="criteria-header-badge">&#128220; Institutional Regulations</div>
            <h1 class="criteria-title">Official On-Duty (OD) Requirements &amp; Criteria</h1>
            <p class="criteria-subtitle">
                All On-Duty (OD) sanction requests are governed by institutional bylaws and academic criteria. Adherence to these 4 official regulations is strictly monitored and enforced.
            </p>
        </div>

        <!-- 4 Official College Rules Cards -->
        <div class="rules-list">
            <!-- Rule 1: Prior Authorization -->
            <div class="rule-card">
                <div class="rule-number-pill">01</div>
                <div class="rule-content">
                    <div class="rule-heading">
                        Prior Authorization
                        <span class="rule-enforcement-tag tag-mandatory">Mandatory</span>
                    </div>
                    <p class="rule-desc">
                        Students must participate only via official college bodies, clubs, or authorized departments. Unofficial or independent participation without prior departmental knowledge cannot be sanctioned for attendance compensation.
                    </p>
                </div>
            </div>

            <!-- Rule 2: Form Submission & Coordinator Endorsement -->
            <div class="rule-card">
                <div class="rule-number-pill">02</div>
                <div class="rule-content">
                    <div class="rule-heading">
                        Form Submission &amp; Coordinator Endorsement
                        <span class="rule-enforcement-tag tag-mandatory">Required</span>
                    </div>
                    <p class="rule-desc">
                        Participants must submit the prescribed attendance/OD application endorsed by the respective Club/Activity Staff Coordinator. The authorized coordinator's verification confirms official duty representation.
                    </p>
                </div>
            </div>

            <!-- Rule 3: 3-Day Timeline Constraint (Automated Enforcement) -->
            <div class="rule-card">
                <div class="rule-number-pill" style="background-color: #FEF2F2; color: #DC2626; border-color: #FECDD3;">03</div>
                <div class="rule-content">
                    <div class="rule-heading">
                        3-Day Timeline Constraint (Automated Enforcement)
                        <span class="rule-enforcement-tag tag-strict">Strict Rule</span>
                    </div>
                    <p class="rule-desc">
                        Duly completed OD applications must be submitted within three (3) days of rejoining classes after the duty; late submissions are automatically rejected by the system. Advance applications prior to the event date are permitted and encouraged.
                    </p>
                </div>
            </div>

            <!-- Rule 4: Overall 75% Attendance Rule & Code of Conduct -->
            <div class="rule-card">
                <div class="rule-number-pill">04</div>
                <div class="rule-content">
                    <div class="rule-heading">
                        Overall 75% Attendance Rule &amp; Code of Conduct
                        <span class="rule-enforcement-tag tag-mandatory">Statutory</span>
                    </div>
                    <p class="rule-desc">
                        An overall minimum of 75% attendance is mandatory for semester examination eligibility. Approved OD claims adjust against calculated attendance deficits subject to Staff &amp; HOD approval and adherence to the Jayantian Code of Conduct.
                    </p>
                </div>
            </div>
        </div>

        <div style="margin-top: 32px; text-align: center;">
            <a href="<%= dashboardUrl %>" class="btn-submit-primary" style="display: inline-flex; text-decoration: none;">
                &larr; Return to Dashboard
            </a>
        </div>
    </main>

    <!-- Site Footer -->
    <footer class="site-footer">
        <div>
            Digital Leave &amp; On-Duty Management System &bull; Academic Portal
        </div>
    </footer>

</body>
</html>
