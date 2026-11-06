package controller;

import exception.InvalidInputException;
import java.io.IOException;
import java.net.URLEncoder;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import model.User;
import service.AuthService;
import service.AuthServiceImpl;

/**
 * Phase 4: Server-Side Integration, Sessions & MySQL Execution
 * Registers new student accounts into the MySQL database.
 */
@WebServlet("/registerServlet")
public class RegisterServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;
    private final AuthService authService = new AuthServiceImpl();

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        request.setCharacterEncoding("UTF-8");

        String rollNo = request.getParameter("rollNo");
        String fullName = request.getParameter("fullName");
        String password = request.getParameter("password");

        if (rollNo == null || rollNo.trim().isEmpty()) {
            response.sendRedirect("login.html?reg_error=1&msg=" + URLEncoder.encode("Roll number cannot be empty.", "UTF-8"));
            return;
        }

        // Student's Roll Number MUST be their login username
        String username = rollNo.trim();

        if (fullName == null || fullName.trim().isEmpty()) {
            fullName = username;
        }

        try {
            User newUser = new User(0, username, password, "student", username.toUpperCase(), fullName.trim(), "Computer Applications", "MCA");
            authService.registerUser(newUser);

            // Redirect back to login with success indicator
            response.sendRedirect("login.html?registered=1");
        } catch (InvalidInputException e) {
            String errorMsg = e.getMessage();
            if (errorMsg != null && (errorMsg.contains("already exists") || errorMsg.contains("already registered"))) {
                response.sendRedirect("login.html?error=exists");
            } else {
                response.sendRedirect("login.html?reg_error=1&msg=" + URLEncoder.encode(errorMsg != null ? errorMsg : "Registration failed", "UTF-8"));
            }
        } catch (Exception e) {
            response.sendRedirect("login.html?error=exists");
        }
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.sendRedirect("login.html");
    }
}
