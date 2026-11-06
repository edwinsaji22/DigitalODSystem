package controller;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import service.ODService;
import service.ODServiceImpl;

/**
 * Phase 4: Server-Side Integration, Sessions & MySQL Execution
 * Handles status updates by Staff (Verify/Reject) and HOD (Approve/Decline).
 */
@WebServlet("/updateODStatusServlet")
public class UpdateODStatusServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;
    private final ODService odService = new ODServiceImpl();

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        request.setCharacterEncoding("UTF-8");

        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("loggedInUser") == null) {
            response.sendRedirect("login.html");
            return;
        }

        String userRole = (String) session.getAttribute("userRole");
        String requestIdStr = request.getParameter("requestId");
        String action = request.getParameter("action");

        if (requestIdStr != null && action != null) {
            try {
                int requestId = Integer.parseInt(requestIdStr.trim());

                if ("staff".equalsIgnoreCase(userRole) || "hod".equalsIgnoreCase(userRole)) {
                    if ("verify".equalsIgnoreCase(action)) {
                        odService.updateStaffStatus(requestId, "Verified");
                        response.sendRedirect("staff_dashboard.jsp?msg=verified");
                        return;
                    } else if ("reject_staff".equalsIgnoreCase(action)) {
                        odService.updateStaffStatus(requestId, "Rejected");
                        response.sendRedirect("staff_dashboard.jsp?msg=rejected");
                        return;
                    }
                }

                if ("hod".equalsIgnoreCase(userRole)) {
                    if ("approve".equalsIgnoreCase(action)) {
                        odService.updateHODStatus(requestId, "Approved");
                        response.sendRedirect("hod_dashboard.jsp?msg=approved");
                        return;
                    } else if ("reject_hod".equalsIgnoreCase(action)) {
                        odService.updateHODStatus(requestId, "Rejected");
                        response.sendRedirect("hod_dashboard.jsp?msg=rejected");
                        return;
                    }
                }
            } catch (NumberFormatException e) {
                System.err.println("[UpdateODStatusServlet] Invalid request ID: " + requestIdStr);
            }
        }

        // Default redirect according to role
        if ("staff".equalsIgnoreCase(userRole)) {
            response.sendRedirect("staff_dashboard.jsp");
        } else if ("hod".equalsIgnoreCase(userRole)) {
            response.sendRedirect("hod_dashboard.jsp");
        } else {
            response.sendRedirect("student_dashboard.jsp");
        }
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        doPost(request, response);
    }
}
