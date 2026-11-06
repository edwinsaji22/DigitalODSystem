package service;

import exception.InvalidInputException;
import model.User;

/**
 * Phase 2: Structured Programming & Reliability
 * Service interface defining user authentication and input validation operations.
 */
public interface AuthService {

    /**
     * Validates credentials format before authentication.
     * @param username user identifier
     * @param password user secret
     * @return true if valid
     * @throws InvalidInputException if constraints are violated
     */
    boolean validateInput(String username, String password) throws InvalidInputException;

    /**
     * Validates student registration inputs.
     * @param username user identifier
     * @param password user secret
     * @param rollNo college register/roll number
     * @return true if valid
     * @throws InvalidInputException if constraints are violated
     */
    boolean validateRegistration(String username, String password, String rollNo) throws InvalidInputException;

    /**
     * Authenticates a user against MySQL database records.
     * @param username user identifier
     * @param password user secret
     * @param role selected role ("student", "staff", "hod")
     * @return User object on successful authentication, null otherwise
     * @throws InvalidInputException if inputs are invalid
     */
    User authenticate(String username, String password, String role) throws InvalidInputException;

    /**
     * Registers a new student user in the database.
     * @param user User model to persist
     * @return true if successfully registered
     * @throws InvalidInputException if duplicate user or invalid fields
     */
    boolean registerUser(User user) throws InvalidInputException;

    /**
     * Fetches user profile by username.
     * @param username username to search
     * @return User or null
     */
    User getUserByUsername(String username);
}
