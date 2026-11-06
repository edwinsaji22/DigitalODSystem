package model;

import java.io.Serializable;

/**
 * Model representing an On-Duty (OD) application request with date range and duration.
 */
public class ODRequest implements Serializable {
    private static final long serialVersionUID = 1L;

    private int id;
    private String studentUsername;
    private String rollNo;
    private String eventType;
    private String eventName;
    private String eventDate;
    private String authorizedBody; // Authorized Body / Club & Staff Coordinator Name
    private String fromDate;
    private String toDate;
    private int daysCount = 1;
    private String reason;
    private String staffStatus; // "Pending", "Verified", "Rejected"
    private String hodStatus;   // "Pending", "Approved", "Rejected"
    private String createdAt;

    public ODRequest() {
        this.staffStatus = "Pending";
        this.hodStatus = "Pending";
        this.daysCount = 1;
    }

    // Constructor with primary event date
    public ODRequest(String studentUsername, String rollNo, String eventType,
                     String eventName, String eventDate, String reason) {
        this.studentUsername = studentUsername;
        this.rollNo = rollNo;
        this.eventType = eventType;
        this.eventName = eventName;
        this.authorizedBody = "";
        this.eventDate = eventDate;
        this.fromDate = eventDate;
        this.toDate = eventDate;
        this.daysCount = 1;
        this.reason = reason;
        this.staffStatus = "Pending";
        this.hodStatus = "Pending";
    }

    // Constructor with date range and calculated days count
    public ODRequest(String studentUsername, String rollNo, String eventType,
                     String eventName, String fromDate, String toDate, int daysCount, String reason) {
        this(studentUsername, rollNo, eventType, eventName, "", fromDate, toDate, daysCount, reason);
    }

    // Constructor with Authorized Body / Club Coordinator
    public ODRequest(String studentUsername, String rollNo, String eventType,
                     String eventName, String authorizedBody, String fromDate, String toDate, int daysCount, String reason) {
        this.studentUsername = studentUsername;
        this.rollNo = rollNo;
        this.eventType = eventType;
        this.eventName = eventName;
        this.authorizedBody = authorizedBody;
        this.fromDate = fromDate;
        this.toDate = (toDate != null && !toDate.isEmpty()) ? toDate : fromDate;
        this.eventDate = fromDate;
        this.daysCount = Math.max(1, daysCount);
        this.reason = reason;
        this.staffStatus = "Pending";
        this.hodStatus = "Pending";
    }

    // Full constructor from database record (legacy 10 params)
    public ODRequest(int id, String studentUsername, String rollNo, String eventType,
                     String eventName, String eventDate, String reason,
                     String staffStatus, String hodStatus, String createdAt) {
        this(id, studentUsername, rollNo, eventType, eventName, "", eventDate, eventDate, eventDate, 1, reason, staffStatus, hodStatus, createdAt);
    }

    // Complete constructor with date range and days count
    public ODRequest(int id, String studentUsername, String rollNo, String eventType,
                     String eventName, String eventDate, String fromDate, String toDate,
                     int daysCount, String reason, String staffStatus, String hodStatus, String createdAt) {
        this(id, studentUsername, rollNo, eventType, eventName, "", eventDate, fromDate, toDate, daysCount, reason, staffStatus, hodStatus, createdAt);
    }

    // Complete constructor with authorizedBody, date range and days count
    public ODRequest(int id, String studentUsername, String rollNo, String eventType,
                     String eventName, String authorizedBody, String eventDate, String fromDate, String toDate,
                     int daysCount, String reason, String staffStatus, String hodStatus, String createdAt) {
        this.id = id;
        this.studentUsername = studentUsername;
        this.rollNo = rollNo;
        this.eventType = eventType;
        this.eventName = eventName;
        this.authorizedBody = authorizedBody;
        this.eventDate = eventDate;
        this.fromDate = (fromDate != null && !fromDate.isEmpty()) ? fromDate : eventDate;
        this.toDate = (toDate != null && !toDate.isEmpty()) ? toDate : eventDate;
        this.daysCount = Math.max(1, daysCount);
        this.reason = reason;
        this.staffStatus = staffStatus != null ? staffStatus : "Pending";
        this.hodStatus = hodStatus != null ? hodStatus : "Pending";
        this.createdAt = createdAt;
    }

    // ---------- Getters and Setters ----------

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getStudentUsername() {
        return studentUsername;
    }

    public void setStudentUsername(String studentUsername) {
        this.studentUsername = studentUsername;
    }

    public String getRollNo() {
        return rollNo;
    }

    public void setRollNo(String rollNo) {
        this.rollNo = rollNo;
    }

    public String getEventType() {
        return eventType;
    }

    public void setEventType(String eventType) {
        this.eventType = eventType;
    }

    public String getEventName() {
        return eventName;
    }

    public void setEventName(String eventName) {
        this.eventName = eventName;
    }

    public String getAuthorizedBody() {
        return authorizedBody != null ? authorizedBody : "";
    }

    public void setAuthorizedBody(String authorizedBody) {
        this.authorizedBody = authorizedBody;
    }

    public String getEventDate() {
        return eventDate != null ? eventDate : fromDate;
    }

    public void setEventDate(String eventDate) {
        this.eventDate = eventDate;
        if (this.fromDate == null) {
            this.fromDate = eventDate;
        }
    }

    public String getFromDate() {
        return fromDate != null ? fromDate : eventDate;
    }

    public void setFromDate(String fromDate) {
        this.fromDate = fromDate;
        if (this.eventDate == null) {
            this.eventDate = fromDate;
        }
    }

    public String getToDate() {
        return toDate != null ? toDate : (fromDate != null ? fromDate : eventDate);
    }

    public void setToDate(String toDate) {
        this.toDate = toDate;
    }

    public int getDaysCount() {
        return Math.max(1, daysCount);
    }

    public void setDaysCount(int daysCount) {
        this.daysCount = Math.max(1, daysCount);
    }

    public String getReason() {
        return reason;
    }

    public void setReason(String reason) {
        this.reason = reason;
    }

    public String getStaffStatus() {
        return staffStatus;
    }

    public void setStaffStatus(String staffStatus) {
        this.staffStatus = staffStatus;
    }

    public String getHodStatus() {
        return hodStatus;
    }

    public void setHodStatus(String hodStatus) {
        this.hodStatus = hodStatus;
    }

    public String getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(String createdAt) {
        this.createdAt = createdAt;
    }

    // Helper status checking methods
    public boolean isPendingStaff() {
        return "Pending".equalsIgnoreCase(staffStatus);
    }

    public boolean isStaffVerified() {
        return "Verified".equalsIgnoreCase(staffStatus);
    }

    public boolean isStaffRejected() {
        return "Rejected".equalsIgnoreCase(staffStatus);
    }

    public boolean isPendingHOD() {
        return isStaffVerified() && "Pending".equalsIgnoreCase(hodStatus);
    }

    public boolean isHodApproved() {
        return "Approved".equalsIgnoreCase(hodStatus);
    }

    public boolean isHodRejected() {
        return "Rejected".equalsIgnoreCase(hodStatus);
    }

    public boolean isFinalApproved() {
        return isStaffVerified() && isHodApproved();
    }

    public boolean isAnyRejected() {
        return isStaffRejected() || isHodRejected();
    }

    @Override
    public String toString() {
        return "ODRequest{" +
                "id=" + id +
                ", studentUsername='" + studentUsername + '\'' +
                ", rollNo='" + rollNo + '\'' +
                ", eventType='" + eventType + '\'' +
                ", eventName='" + eventName + '\'' +
                ", fromDate='" + fromDate + '\'' +
                ", toDate='" + toDate + '\'' +
                ", daysCount=" + daysCount +
                ", staffStatus='" + staffStatus + '\'' +
                ", hodStatus='" + hodStatus + '\'' +
                '}';
    }

    /**
     * Serializes this ODRequest entity to a valid JSON string.
     * Useful for REST API endpoints, AJAX consumers, and client-side data interchange.
     */
    public String toJson() {
        return "{"
                + "\"id\":" + id + ","
                + "\"studentUsername\":\"" + escapeJson(studentUsername) + "\","
                + "\"rollNo\":\"" + escapeJson(rollNo) + "\","
                + "\"eventType\":\"" + escapeJson(eventType) + "\","
                + "\"eventName\":\"" + escapeJson(eventName) + "\","
                + "\"authorizedBody\":\"" + escapeJson(authorizedBody) + "\","
                + "\"fromDate\":\"" + escapeJson(fromDate) + "\","
                + "\"toDate\":\"" + escapeJson(toDate) + "\","
                + "\"daysCount\":" + daysCount + ","
                + "\"reason\":\"" + escapeJson(reason) + "\","
                + "\"staffStatus\":\"" + escapeJson(staffStatus) + "\","
                + "\"hodStatus\":\"" + escapeJson(hodStatus) + "\","
                + "\"finalStatus\":\"" + (isFinalApproved() ? "Approved" : (isAnyRejected() ? "Rejected" : "Pending")) + "\","
                + "\"createdAt\":\"" + escapeJson(createdAt) + "\""
                + "}";
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
