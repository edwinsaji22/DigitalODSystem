package controller;

import exception.InvalidInputException;
import java.io.IOException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.time.format.DateTimeParseException;
import java.time.temporal.ChronoUnit;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import model.ODRequest;
import service.ODService;
import service.ODServiceImpl;

/**
 * Phase 4 & Real College OD Logic:
 * Enforces Jayantian OD Criteria:
 * 1. Prior Authorization (Authorized Body / Club & Staff Coordinator Name required)
 * 2. 3-Day Timeline Constraint (toDate vs LocalDate.now() <= 3)
 * 3. Date Chronology (toDate >= fromDate) & Overlap validation
 * 
 * Supports both standard HTML Form POST (redirects) and JSON AJAX requests (format=json).
 */
@WebServlet("/applyODServlet")
public class ApplyODServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;
    private final ODService odService = new ODServiceImpl();

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        request.setCharacterEncoding("UTF-8");

        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("loggedInUser") == null) {
            if (isJsonRequest(request)) {
                sendJsonResponse(response, HttpServletResponse.SC_UNAUTHORIZED, "error", "Unauthorized: Active session required.");
                return;
            }
            response.sendRedirect("login.html?unauthorized=1");
            return;
        }

        String username = (String) session.getAttribute("loggedInUser");

        // Roll number from session or form
        String rollNo = (String) session.getAttribute("rollNo");
        if (rollNo == null || rollNo.trim().isEmpty()) {
            rollNo = request.getParameter("rollNo");
            if (rollNo == null || rollNo.trim().isEmpty()) {
                rollNo = username;
            }
        }

        // 1. OD Category
        String eventType = request.getParameter("eventType");
        if (eventType == null || eventType.trim().isEmpty()) {
            handleError(request, response, "OD Category must be selected.");
            return;
        }

        // 2. Prior Authorization: Authorized Body / Club & Staff Coordinator Name
        String authorizedBody = request.getParameter("authorizedBody");
        if (authorizedBody == null || authorizedBody.trim().isEmpty()) {
            handleError(request, response, "Prior Authorization Required: Authorized Club/Department & Staff Coordinator endorsement is required.");
            return;
        }

        // 3. Event Dates (From Date & To Date)
        String fromDateStr = request.getParameter("fromDate");
        String toDateStr = request.getParameter("toDate");

        if (fromDateStr == null || fromDateStr.trim().isEmpty()) {
            fromDateStr = request.getParameter("eventDate");
        }
        if (fromDateStr == null || fromDateStr.trim().isEmpty()) {
            handleError(request, response, "From Date is required.");
            return;
        }
        if (toDateStr == null || toDateStr.trim().isEmpty()) {
            toDateStr = fromDateStr;
        }

        LocalDate fromDate;
        LocalDate toDate;
        try {
            fromDate = LocalDate.parse(fromDateStr.trim());
            toDate = LocalDate.parse(toDateStr.trim());
        } catch (DateTimeParseException e) {
            handleError(request, response, "Invalid Date format (" + fromDateStr + "). Please use YYYY-MM-DD.");
            return;
        }

        // Date Order Check
        if (toDate.isBefore(fromDate)) {
            handleError(request, response, "Date Validation Failed: 'To Date' (" + toDateStr + ") cannot be earlier than 'From Date' (" + fromDateStr + ").");
            return;
        }

        // 3-Day Timeline Constraint Rule (STRICT)
        // OD applications must be submitted within 3 days of completing the duty (or in advance before the event)
        long daysPassed = ChronoUnit.DAYS.between(toDate, LocalDate.now());
        if (daysPassed > 3) {
            handleError(request, response, "Submission Rejected (Timeline Constraint): OD applications must be submitted within 3 days of completing the duty. Late submissions are not permitted.");
            return;
        }

        int daysCount = (int) ChronoUnit.DAYS.between(fromDate, toDate) + 1;

        // 4. Reason / Event Details
        String reason = request.getParameter("reason");
        if (reason == null || reason.trim().isEmpty()) {
            handleError(request, response, "Reason / Event Details cannot be empty.");
            return;
        }

        // Event title / host description
        String eventName = request.getParameter("eventName");
        if (eventName == null || eventName.trim().isEmpty()) {
            eventName = eventType.trim();
        }

        try {
            ODRequest od = new ODRequest(
                username.trim(),
                rollNo.trim(),
                eventType.trim(),
                eventName.trim(),
                authorizedBody.trim(),
                fromDate.toString(),
                toDate.toString(),
                daysCount,
                reason.trim()
            );

            odService.applyOD(od);

            if (isJsonRequest(request)) {
                sendJsonResponse(response, HttpServletResponse.SC_OK, "success",
                    "OD Application submitted successfully. Assigned for Faculty Advisor review.");
                return;
            }

            response.sendRedirect("student_dashboard.jsp?status=success");
        } catch (InvalidInputException e) {
            handleError(request, response, e.getMessage());
        } catch (Exception e) {
            handleError(request, response, "Internal error: " + e.getMessage());
        }
    }

    private boolean isJsonRequest(HttpServletRequest request) {
        String format = request.getParameter("format");
        if ("json".equalsIgnoreCase(format)) return true;
        Object formatAttr = request.getAttribute("format");
        if ("json".equals(formatAttr)) return true;
        String accept = request.getHeader("Accept");
        if (accept != null && accept.contains("application/json")) return true;
        String xrw = request.getHeader("X-Requested-With");
        return "XMLHttpRequest".equalsIgnoreCase(xrw);
    }

    private void handleError(HttpServletRequest request, HttpServletResponse response, String message) throws IOException {
        if (isJsonRequest(request)) {
            sendJsonResponse(response, HttpServletResponse.SC_BAD_REQUEST, "error", message);
            return;
        }
        String errorMsg = URLEncoder.encode(message != null ? message : "Invalid input", StandardCharsets.UTF_8);
        response.sendRedirect("student_dashboard.jsp?status=error&msg=" + errorMsg);
    }

    private void sendJsonResponse(HttpServletResponse response, int statusCode, String status, String message) throws IOException {
        response.setStatus(statusCode);
        response.setContentType("application/json;charset=UTF-8");
        response.setHeader("Access-Control-Allow-Origin", "*");
        response.getWriter().write("{\n"
            + "  \"status\": \"" + status + "\",\n"
            + "  \"message\": \"" + escapeJson(message) + "\"\n"
            + "}");
    }

    private String escapeJson(String s) {
        if (s == null) return "";
        return s.replace("\\", "\\\\")
                .replace("\"", "\\\"")
                .replace("\b", "\\b")
                .replace("\f", "\\f")
                .replace("\n", "\\n")
                .replace("\r", "\\r")
                .replace("\t", "\\t");
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.sendRedirect("student_dashboard.jsp");
    }
}
