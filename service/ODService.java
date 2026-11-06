package service;

import exception.InvalidInputException;
import java.util.List;
import model.ODRequest;

/**
 * Service interface defining On-Duty application processing and business rule validation.
 */
public interface ODService {

    /**
     * Submits a new OD application with business rule validations.
     * @param request ODRequest model
     * @return true if successfully saved
     * @throws InvalidInputException if OD criteria, date rules, or quota limits fail
     */
    boolean applyOD(ODRequest request) throws InvalidInputException;

    /**
     * Retrieves all OD requests submitted by a specific student.
     * @param username student username
     * @return List of OD requests
     */
    List<ODRequest> getODRequestsByStudent(String username);

    /**
     * Retrieves all OD requests in the system.
     * @return List of OD requests
     */
    List<ODRequest> getAllODRequests();

    /**
     * Calculates total used OD days for a student (from active Approved and Pending requests).
     * @param username student username
     * @return sum of days count
     */
    int getUsedODDays(String username);

    /**
     * Updates the staff verification status.
     * @param requestId ID of request
     * @param status "Verified" or "Rejected"
     * @return true if updated
     */
    boolean updateStaffStatus(int requestId, String status);

    /**
     * Updates the HOD final approval status.
     * @param requestId ID of request
     * @param status "Approved" or "Rejected"
     * @return true if updated
     */
    boolean updateHODStatus(int requestId, String status);
}
