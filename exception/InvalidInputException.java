package exception;

/**
 * Phase 2: Structured Programming & Reliability
 * Custom exception thrown when input validation or business rules fail.
 */
public class InvalidInputException extends Exception {
    private static final long serialVersionUID = 1L;

    public InvalidInputException(String message) {
        super(message);
    }

    public InvalidInputException(String message, Throwable cause) {
        super(message, cause);
    }
}