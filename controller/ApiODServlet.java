package controller;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.List;
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
 * Phase 4 & 5: RESTful JSON API Controller (/api/od, /api/od-policy)
 * Delivers structured JSON data interchange for client-side AJAX,
 * dashboard metrics, mobile clients, and external institutional integrations.
 */
@WebServlet(name = "ApiODServlet", urlPatterns = {"/api/od", "/api/od-requests", "/api/od-policy"})
public class ApiODServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;
    private final ODService odService = new ODServiceImpl();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("application/json;charset=UTF-8");
        response.setHeader("Access-Control-Allow-Origin", "*");
        response.setHeader("Cache-Control", "no-cache, no-store, must-revalidate");

        String uri = request.getRequestURI();

        // 1. Policy Endpoint: Serves formal JSON institutional OD criteria
        if (uri.endsWith("/od-policy")) {
            servePolicyJson(response);
            return;
        }

        // 2. Data Endpoint: Serves live OD records from MySQL
        HttpSession session = request.getSession(false);
        String loggedInUser = (session != null) ? (String) session.getAttribute("loggedInUser") : null;
        String userRole = (session != null) ? (String) session.getAttribute("userRole") : null;

        // Query filter support: ?student=rollNo
        String studentParam = request.getParameter("student");
        String targetStudent = (studentParam != null && !studentParam.trim().isEmpty())
                ? studentParam.trim()
                : loggedInUser;

        List<ODRequest> requests;
        if ("staff".equalsIgnoreCase(userRole) || "hod".equalsIgnoreCase(userRole)) {
            requests = odService.getAllODRequests();
        } else if (targetStudent != null && !targetStudent.isEmpty()) {
            requests = odService.getODRequestsByStudent(targetStudent);
        } else {
            // Public / Viva Demo fallback: return all current requests
            requests = odService.getAllODRequests();
        }

        int total = requests.size();
        int pending = 0;
        int approved = 0;
        int rejected = 0;

        for (ODRequest req : requests) {
            if (req.isFinalApproved()) {
                approved++;
            } else if (req.isAnyRejected()) {
                rejected++;
            } else {
                pending++;
            }
        }

        PrintWriter out = response.getWriter();
        StringBuilder sb = new StringBuilder();
        sb.append("{\n");
        sb.append("  \"status\": \"success\",\n");
        sb.append("  \"endpoint\": \"/api/od\",\n");
        sb.append("  \"format\": \"JSON (JavaScript Object Notation)\",\n");
        sb.append("  \"timestamp\": \"").append(java.time.LocalDateTime.now().toString()).append("\",\n");
        sb.append("  \"user\": \"").append(escapeJson(targetStudent != null ? targetStudent : "Public Demo")).append("\",\n");
        sb.append("  \"role\": \"").append(escapeJson(userRole != null ? userRole : "viewer")).append("\",\n");
        sb.append("  \"metrics\": {\n");
        sb.append("    \"totalApplications\": ").append(total).append(",\n");
        sb.append("    \"pendingCount\": ").append(pending).append(",\n");
        sb.append("    \"approvedCount\": ").append(approved).append(",\n");
        sb.append("    \"rejectedCount\": ").append(rejected).append(",\n");
        sb.append("    \"maxSemesterQuota\": 15\n");
        sb.append("  },\n");
        sb.append("  \"requests\": [\n");

        for (int i = 0; i < requests.size(); i++) {
            ODRequest r = requests.get(i);
            sb.append("    {\n");
            sb.append("      \"id\": ").append(r.getId()).append(",\n");
            sb.append("      \"rollNo\": \"").append(escapeJson(r.getRollNo())).append("\",\n");
            sb.append("      \"studentUsername\": \"").append(escapeJson(r.getStudentUsername())).append("\",\n");
            sb.append("      \"eventType\": \"").append(escapeJson(r.getEventType())).append("\",\n");
            sb.append("      \"eventName\": \"").append(escapeJson(r.getEventName())).append("\",\n");
            sb.append("      \"authorizedBody\": \"").append(escapeJson(r.getAuthorizedBody())).append("\",\n");
            sb.append("      \"fromDate\": \"").append(escapeJson(r.getFromDate())).append("\",\n");
            sb.append("      \"toDate\": \"").append(escapeJson(r.getToDate())).append("\",\n");
            sb.append("      \"daysCount\": ").append(r.getDaysCount()).append(",\n");
            sb.append("      \"reason\": \"").append(escapeJson(r.getReason())).append("\",\n");
            sb.append("      \"staffStatus\": \"").append(escapeJson(r.getStaffStatus())).append("\",\n");
            sb.append("      \"hodStatus\": \"").append(escapeJson(r.getHodStatus())).append("\",\n");
            sb.append("      \"overallStatus\": \"").append(r.isFinalApproved() ? "Approved" : (r.isAnyRejected() ? "Rejected" : "Pending")).append("\",\n");
            sb.append("      \"createdAt\": \"").append(escapeJson(r.getCreatedAt())).append("\"\n");
            sb.append("    }").append(i < requests.size() - 1 ? ",\n" : "\n");
        }

        sb.append("  ]\n");
        sb.append("}");

        out.print(sb.toString());
        out.flush();
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        // Forward POST to ApplyODServlet with format=json flag to reuse business rules
        request.setAttribute("format", "json");
        doGet(request, response);
    }

    private void servePolicyJson(HttpServletResponse response) throws IOException {
        InputStream in = getServletContext().getResourceAsStream("/WEB-INF/od_policy.json");
        if (in == null) {
            response.getWriter().write("{\"status\":\"error\",\"message\":\"Policy file not found.\"}");
            return;
        }

        try (BufferedReader reader = new BufferedReader(new InputStreamReader(in, StandardCharsets.UTF_8))) {
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                sb.append(line).append("\n");
            }
            response.getWriter().write(sb.toString());
        }
    }

    private static String escapeJson(String s) {
        if (s == null) return "";
        return s.replace("\\", "\\\\")
                .replace("\"", "\\\"")
                .replace("\b", "\\b")
                .replace("\f", "\\f")
                .replace("\n", "\\n")
                .replace("\r", "\\r")
                .replace("\t", "\\t");
    }
}
