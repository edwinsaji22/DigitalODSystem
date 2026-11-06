package service;

import exception.InvalidInputException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.format.DateTimeParseException;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.atomic.AtomicInteger;
import model.ODRequest;

/**
 * Implementation of ODService with full business rules validation,
 * MySQL JDBC execution, and thread-safe memory fallback.
 */
public class ODServiceImpl implements ODService {

    private static final List<ODRequest> MEMORY_REQUESTS = new CopyOnWriteArrayList<>();
    private static final AtomicInteger ID_GENERATOR = new AtomicInteger(100);

    /**
     * Institutional Policy: Category-specific maximum allowable working days per request.
     */
    public static int getCategoryMaxDays(String category) {
        if (category == null || category.trim().isEmpty()) return 3;
        String cat = category.toLowerCase().trim();

        if (cat.contains("placement") || cat.contains("interview")) {
            return 2;
        }
        if (cat.contains("symposium") || cat.contains("workshop") || cat.contains("conference")
                || cat.contains("paper presentation") || cat.contains("cultural")) {
            return 3;
        }
        if (cat.contains("hackathon") || cat.contains("sports") || cat.contains("nss")
                || cat.contains("ncc") || cat.contains("yrc")) {
            return 5;
        }
        if (cat.contains("internship") || cat.contains("industrial") || cat.contains("medical")) {
            return 7;
        }
        return 5;
    }

    @Override
    public boolean applyOD(ODRequest request) throws InvalidInputException {
        if (request == null) {
            throw new InvalidInputException("OD Request cannot be null.");
        }
        if (request.getStudentUsername() == null || request.getStudentUsername().trim().isEmpty()) {
            throw new InvalidInputException("Student username is required.");
        }
        if (request.getRollNo() == null || request.getRollNo().trim().isEmpty()) {
            throw new InvalidInputException("Roll Number is required.");
        }
        if (request.getEventType() == null || request.getEventType().trim().isEmpty()) {
            throw new InvalidInputException("OD Category must be selected.");
        }
        if (request.getAuthorizedBody() == null || request.getAuthorizedBody().trim().isEmpty()) {
            throw new InvalidInputException("Prior Authorization Required: Authorized Club/Department & Staff Coordinator endorsement is required.");
        }
        if (request.getEventName() == null || request.getEventName().trim().isEmpty()) {
            throw new InvalidInputException("Event Details / Title is required.");
        }
        if (request.getReason() == null || request.getReason().trim().isEmpty()) {
            throw new InvalidInputException("Reason / Description is required.");
        }

        // ---------------------------------------------------------------------
        // BUSINESS RULE 2: Date Chronology Validation
        // ---------------------------------------------------------------------
        String fromDateStr = request.getFromDate();
        if (fromDateStr == null || fromDateStr.trim().isEmpty()) {
            fromDateStr = request.getEventDate();
        }
        String toDateStr = request.getToDate();
        if (toDateStr == null || toDateStr.trim().isEmpty()) {
            toDateStr = fromDateStr;
        }

        if (fromDateStr == null || fromDateStr.trim().isEmpty()) {
            throw new InvalidInputException("Event Date is required.");
        }

        LocalDate fromDate;
        LocalDate toDate;
        try {
            fromDate = LocalDate.parse(fromDateStr.trim());
            toDate = LocalDate.parse(toDateStr.trim());
        } catch (DateTimeParseException e) {
            throw new InvalidInputException("Invalid Date format (" + fromDateStr + "). Please use YYYY-MM-DD.");
        }

        if (toDate.isBefore(fromDate)) {
            throw new InvalidInputException("Date Validation Failed: 'To Date' (" + toDateStr + ") cannot be earlier than 'From Date' (" + fromDateStr + ").");
        }

        // ---------------------------------------------------------------------
        // JAYANTIAN OD CRITERIA: 3-Day Timeline Constraint Rule (STRICT)
        // OD applications must be submitted within 3 days of duty completion
        // ---------------------------------------------------------------------
        LocalDate today = LocalDate.now();
        long daysSinceDuty = ChronoUnit.DAYS.between(toDate, today);
        if (daysSinceDuty > 3) {
            throw new InvalidInputException("Submission Rejected (Timeline Constraint): OD applications must be submitted within 3 days of completing the duty. Late submissions are not permitted.");
        }

        int daysCount = (int) ChronoUnit.DAYS.between(fromDate, toDate) + 1;
        request.setFromDate(fromDate.toString());
        request.setToDate(toDate.toString());
        request.setEventDate(fromDate.toString());
        request.setDaysCount(daysCount);

        // ---------------------------------------------------------------------
        // BUSINESS RULE 3: Category Duration Limits
        // ---------------------------------------------------------------------
        String category = request.getEventType().trim();
        int maxAllowedDays = getCategoryMaxDays(category);
        if (daysCount > maxAllowedDays) {
            throw new InvalidInputException("Category Duration Limit Exceeded: Category '" + category
                    + "' allows a maximum duration of " + maxAllowedDays
                    + " working day(s) per application under college bylaws. Your requested duration is " + daysCount + " days.");
        }

        // ---------------------------------------------------------------------
        // BUSINESS RULE 2 (cont): Duplicate Date Overlap Check
        // ---------------------------------------------------------------------
        List<ODRequest> existingRequests = getODRequestsByStudent(request.getStudentUsername());
        for (ODRequest ex : existingRequests) {
            if (ex.isAnyRejected()) {
                continue; // Rejected applications do not block dates
            }
            LocalDate exStart = null;
            LocalDate exEnd = null;
            try {
                String exFrom = ex.getFromDate() != null ? ex.getFromDate() : ex.getEventDate();
                String exTo = ex.getToDate() != null ? ex.getToDate() : exFrom;
                if (exFrom != null) exStart = LocalDate.parse(exFrom.trim());
                if (exTo != null) exEnd = LocalDate.parse(exTo.trim());
            } catch (Exception ignored) {
            }

            if (exStart != null && exEnd != null) {
                // Overlap occurs if [fromDate, toDate] overlaps with [exStart, exEnd]
                boolean overlaps = !(toDate.isBefore(exStart) || fromDate.isAfter(exEnd));
                if (overlaps) {
                    throw new InvalidInputException("Duplicate Date Conflict: You already have an active OD application (#OD-"
                            + ex.getId() + " for '" + ex.getEventName() + "') booked from " + exStart + " to " + exEnd
                            + ". Multiple OD applications on overlapping dates are strictly prohibited.");
                }
            }
        }

        // ---------------------------------------------------------------------
        // BUSINESS RULE 1: 15-Day Semester Quota Limit
        // ---------------------------------------------------------------------
        int currentUsedDays = getUsedODDays(request.getStudentUsername());
        if (currentUsedDays + daysCount > 15) {
            int remaining = Math.max(0, 15 - currentUsedDays);
            throw new InvalidInputException("OD Criteria Failed: Exceeds maximum 15-day semester quota. You have currently utilized "
                    + currentUsedDays + " of 15 allowed days, and this application requires " + daysCount
                    + " day(s). Maximum allowable days remaining: " + remaining + " day(s).");
        }

        request.setStaffStatus("Pending");
        request.setHodStatus("Pending");
        if (request.getCreatedAt() == null) {
            request.setCreatedAt(new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date()));
        }

        // 1. Persist to MySQL Database via JDBC
        Connection conn = null;
        PreparedStatement stmt = null;
        ResultSet generatedKeys = null;
        boolean dbSaved = false;

        try {
            conn = DBConnection.getConnection();
            String sql = "INSERT INTO od_requests (student_username, roll_no, event_type, event_name, authorized_body, event_date, from_date, to_date, days_count, reason, staff_status, hod_status) " +
                         "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending', 'Pending')";
            stmt = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS);
            stmt.setString(1, request.getStudentUsername().trim());
            stmt.setString(2, request.getRollNo().trim());
            stmt.setString(3, request.getEventType().trim());
            stmt.setString(4, request.getEventName().trim());
            stmt.setString(5, request.getAuthorizedBody().trim());
            stmt.setString(6, request.getEventDate().trim());
            stmt.setString(7, request.getFromDate().trim());
            stmt.setString(8, request.getToDate().trim());
            stmt.setInt(9, request.getDaysCount());
            stmt.setString(10, request.getReason().trim());

            int affectedRows = stmt.executeUpdate();
            if (affectedRows > 0) {
                dbSaved = true;
                generatedKeys = stmt.getGeneratedKeys();
                if (generatedKeys.next()) {
                    request.setId(generatedKeys.getInt(1));
                }
            }
        } catch (SQLException e) {
            System.err.println("[ODService] MySQL insert failed, applying memory fallback: " + e.getMessage());
        } finally {
            DBConnection.closeQuietly(generatedKeys, stmt, conn);
        }

        if (!dbSaved && request.getId() == 0) {
            request.setId(ID_GENERATOR.incrementAndGet());
        }

        // 2. Keep in-memory synchronized for instant responsiveness
        MEMORY_REQUESTS.add(0, request);
        return true;
    }

    @Override
    public int getUsedODDays(String username) {
        if (username == null || username.trim().isEmpty()) return 0;
        String cleanUser = username.trim();

        // 1. Try MySQL Database
        Connection conn = null;
        PreparedStatement stmt = null;
        ResultSet rs = null;
        try {
            conn = DBConnection.getConnection();
            String sql = "SELECT COALESCE(SUM(days_count), 0) FROM od_requests " +
                         "WHERE LOWER(student_username) = LOWER(?) " +
                         "AND LOWER(hod_status) != 'rejected' AND LOWER(staff_status) != 'rejected'";
            stmt = conn.prepareStatement(sql);
            stmt.setString(1, cleanUser);
            rs = stmt.executeQuery();
            if (rs.next()) {
                return rs.getInt(1);
            }
        } catch (SQLException e) {
            System.err.println("[ODService] MySQL getUsedODDays query failed: " + e.getMessage());
        } finally {
            DBConnection.closeQuietly(rs, stmt, conn);
        }

        // 2. Memory Store Fallback
        int count = 0;
        for (ODRequest req : MEMORY_REQUESTS) {
            if (cleanUser.equalsIgnoreCase(req.getStudentUsername()) && !req.isAnyRejected()) {
                count += Math.max(1, req.getDaysCount());
            }
        }
        return count;
    }

    @Override
    public List<ODRequest> getODRequestsByStudent(String username) {
        if (username == null) return Collections.emptyList();
        String cleanUser = username.trim();

        // 1. Try MySQL Database via JDBC
        Connection conn = null;
        PreparedStatement stmt = null;
        ResultSet rs = null;
        List<ODRequest> list = new ArrayList<>();

        try {
            conn = DBConnection.getConnection();
            String sql = "SELECT id, student_username, roll_no, event_type, event_name, authorized_body, event_date, " +
                         "from_date, to_date, days_count, reason, staff_status, hod_status, created_at " +
                         "FROM od_requests WHERE LOWER(student_username) = LOWER(?) ORDER BY id DESC";
            stmt = conn.prepareStatement(sql);
            stmt.setString(1, cleanUser);
            rs = stmt.executeQuery();

            while (rs.next()) {
                list.add(mapResultSetToOD(rs));
            }
            return list;
        } catch (SQLException e) {
            System.err.println("[ODService] MySQL query by student failed: " + e.getMessage());
        } finally {
            DBConnection.closeQuietly(rs, stmt, conn);
        }

        // 2. Fallback to memory
        List<ODRequest> userList = new ArrayList<>();
        for (ODRequest req : MEMORY_REQUESTS) {
            if (cleanUser.equalsIgnoreCase(req.getStudentUsername())) {
                userList.add(req);
            }
        }
        return userList;
    }

    @Override
    public List<ODRequest> getAllODRequests() {
        Connection conn = null;
        Statement stmt = null;
        ResultSet rs = null;
        List<ODRequest> list = new ArrayList<>();

        try {
            conn = DBConnection.getConnection();
            String sql = "SELECT id, student_username, roll_no, event_type, event_name, authorized_body, event_date, " +
                         "from_date, to_date, days_count, reason, staff_status, hod_status, created_at " +
                         "FROM od_requests ORDER BY id DESC";
            stmt = conn.createStatement();
            rs = stmt.executeQuery(sql);

            while (rs.next()) {
                list.add(mapResultSetToOD(rs));
            }
            return list;
        } catch (SQLException e) {
            System.err.println("[ODService] MySQL query all requests failed: " + e.getMessage());
        } finally {
            DBConnection.closeQuietly(rs, stmt, conn);
        }

        return new ArrayList<>(MEMORY_REQUESTS);
    }

    @Override
    public boolean updateStaffStatus(int requestId, String status) {
        String cleanStatus = (status != null) ? status.trim() : "Pending";

        Connection conn = null;
        PreparedStatement stmt = null;
        try {
            conn = DBConnection.getConnection();
            String sql = "UPDATE od_requests SET staff_status = ? WHERE id = ?";
            stmt = conn.prepareStatement(sql);
            stmt.setString(1, cleanStatus);
            stmt.setInt(2, requestId);
            stmt.executeUpdate();
        } catch (SQLException e) {
            System.err.println("[ODService] MySQL updateStaffStatus failed: " + e.getMessage());
        } finally {
            DBConnection.closeQuietly(stmt, conn);
        }

        for (ODRequest req : MEMORY_REQUESTS) {
            if (req.getId() == requestId) {
                req.setStaffStatus(cleanStatus);
                return true;
            }
        }
        return true;
    }

    @Override
    public boolean updateHODStatus(int requestId, String status) {
        String cleanStatus = (status != null) ? status.trim() : "Pending";

        Connection conn = null;
        PreparedStatement stmt = null;
        try {
            conn = DBConnection.getConnection();
            String sql = "UPDATE od_requests SET hod_status = ? WHERE id = ?";
            stmt = conn.prepareStatement(sql);
            stmt.setString(1, cleanStatus);
            stmt.setInt(2, requestId);
            stmt.executeUpdate();
        } catch (SQLException e) {
            System.err.println("[ODService] MySQL updateHODStatus failed: " + e.getMessage());
        } finally {
            DBConnection.closeQuietly(stmt, conn);
        }

        for (ODRequest req : MEMORY_REQUESTS) {
            if (req.getId() == requestId) {
                req.setHodStatus(cleanStatus);
                return true;
            }
        }
        return true;
    }

    private ODRequest mapResultSetToOD(ResultSet rs) throws SQLException {
        String eventDate = rs.getString("event_date");
        String fromDate = rs.getString("from_date");
        String toDate = rs.getString("to_date");
        int daysCount = rs.getInt("days_count");

        if (fromDate == null || fromDate.isEmpty()) fromDate = eventDate;
        if (toDate == null || toDate.isEmpty()) toDate = fromDate;
        if (daysCount <= 0) daysCount = 1;

        String authorizedBody = "";
        try {
            authorizedBody = rs.getString("authorized_body");
        } catch (SQLException ignored) {}
        if (authorizedBody == null) authorizedBody = "";

        return new ODRequest(
                rs.getInt("id"),
                rs.getString("student_username"),
                rs.getString("roll_no"),
                rs.getString("event_type"),
                rs.getString("event_name"),
                authorizedBody,
                eventDate,
                fromDate,
                toDate,
                daysCount,
                rs.getString("reason"),
                rs.getString("staff_status"),
                rs.getString("hod_status"),
                rs.getString("created_at")
        );
    }
}
