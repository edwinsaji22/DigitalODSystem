<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%
    // Universal Dashboard Router
    if (session == null || session.getAttribute("loggedInUser") == null) {
        response.sendRedirect("login.html?unauthorized=1");
        return;
    }

    String role = (String) session.getAttribute("userRole");
    if ("staff".equalsIgnoreCase(role)) {
        response.sendRedirect("staff_dashboard.jsp");
    } else if ("hod".equalsIgnoreCase(role)) {
        response.sendRedirect("hod_dashboard.jsp");
    } else {
        response.sendRedirect("student_dashboard.jsp");
    }
%>
