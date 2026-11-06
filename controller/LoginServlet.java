package controller;

import exception.InvalidInputException;
import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import model.User;
import service.AuthService;
import service.AuthServiceImpl;

/**
 * Phase 4: Server-Side Integration & Authentication Servlet.
 * Validates credentials against MySQL/Memory and initializes role-based session.
 */
@WebServlet("/loginServlet")
public class LoginServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;
    private final AuthService authService = new AuthServiceImpl();

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        request.setCharacterEncoding("UTF-8");

        String username = request.getParameter("username");
        String password = request.getParameter("password");
        String role = request.getParameter("role");

        try {
            User authenticatedUser = authService.authenticate(username, password, role);

            if (authenticatedUser != null) {
                HttpSession session = request.getSession(true);
                String userRole = authenticatedUser.getRole() != null ? authenticatedUser.getRole().trim().toLowerCase() : "student";

                session.setAttribute("loggedInUser", authenticatedUser.getUsername());
                session.setAttribute("userRole", userRole);
                session.setAttribute("rollNo", authenticatedUser.getRollNo());
                session.setAttribute("fullName", authenticatedUser.getFullName());
                session.setAttribute("department", authenticatedUser.getDepartment());

                // Route strictly according to the authenticated user's actual role
                if ("hod".equalsIgnoreCase(userRole)) {
                    response.sendRedirect("hod_dashboard.jsp");
                } else if ("staff".equalsIgnoreCase(userRole)) {
                    response.sendRedirect("staff_dashboard.jsp");
                } else {
                    response.sendRedirect("student_dashboard.jsp");
                }
                return;
            }
        } catch (InvalidInputException e) {
            System.err.println("[LoginServlet] Validation error: " + e.getMessage());
        } catch (Exception e) {
            System.err.println("[LoginServlet] Internal error during login: " + e.getMessage());
        }

        // Invalid credentials or error
        response.sendRedirect("login.html?error=1");
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.sendRedirect("login.html");
    }
}
