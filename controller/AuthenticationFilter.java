package controller;

import java.io.IOException;
import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

/**
 * Phase 4: Server-Side Integration, Sessions & MySQL Execution
 * Protects secure JSP portals and Servlets, enforces role-based access control,
 * and sets anti-caching headers so browser back button cannot show cached secure views after logout.
 */
@WebFilter(filterName = "AuthenticationFilter", urlPatterns = {
    "/student_dashboard.jsp",
    "/staff_dashboard.jsp",
    "/hod_dashboard.jsp",
    "/dashboard.jsp",
    "/applyODServlet",
    "/updateODStatusServlet",
    "/student_dashboard.html",
    "/staff_dashboard.html",
    "/hod_dashboard.html"
})
public class AuthenticationFilter implements Filter {

    @Override
    public void init(FilterConfig config) throws ServletException {
        // Initialization if needed
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;

        // CRITICAL SECURITY: Prevent browser caching so logged-out users cannot hit 'Back' to view pages
        httpResponse.setHeader("Cache-Control", "no-cache, no-store, must-revalidate"); // HTTP 1.1
        httpResponse.setHeader("Pragma", "no-cache"); // HTTP 1.0
        httpResponse.setDateHeader("Expires", 0); // Proxies

        HttpSession session = httpRequest.getSession(false);
        boolean isLoggedIn = (session != null && session.getAttribute("loggedInUser") != null);

        if (!isLoggedIn) {
            httpResponse.sendRedirect(httpRequest.getContextPath() + "/login.html?unauthorized=1");
            return;
        }

        String role = (String) session.getAttribute("userRole");
        if (role == null) {
            httpResponse.sendRedirect(httpRequest.getContextPath() + "/login.html");
            return;
        }
        role = role.toLowerCase();

        String uri = httpRequest.getRequestURI();

        // Enforce role-based portal boundaries
        if (uri.contains("student_dashboard") || uri.contains("applyODServlet")) {
            if (!"student".equals(role)) {
                // If staff or HOD accidentally navigates to student portal, route them to their proper portal
                String redirectTarget = "hod".equals(role) ? "/hod_dashboard.jsp" : "/staff_dashboard.jsp";
                httpResponse.sendRedirect(httpRequest.getContextPath() + redirectTarget);
                return;
            }
        } else if (uri.contains("staff_dashboard")) {
            if (!"staff".equals(role) && !"hod".equals(role)) {
                httpResponse.sendRedirect(httpRequest.getContextPath() + "/student_dashboard.jsp");
                return;
            }
        } else if (uri.contains("hod_dashboard")) {
            if (!"hod".equals(role)) {
                String redirectTarget = "staff".equals(role) ? "/staff_dashboard.jsp" : "/student_dashboard.jsp";
                httpResponse.sendRedirect(httpRequest.getContextPath() + redirectTarget);
                return;
            }
        }

        chain.doFilter(request, response);
    }

    @Override
    public void destroy() {
    }
}
