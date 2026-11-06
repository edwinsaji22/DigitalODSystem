package service;

import exception.InvalidInputException;
import model.User;

/**
 * Phase 2: Structured Programming & Reliability
 * UserServiceImpl extending AuthServiceImpl for full backward compatibility.
 */
public class UserServiceImpl extends AuthServiceImpl implements UserOperations {

    @Override
    public boolean validateInput(String username, String password) throws InvalidInputException {
        return super.validateInput(username, password);
    }

    @Override
    public boolean authenticate(User user, String inputUsername, String inputPassword) {
        return super.authenticate(user, inputUsername, inputPassword);
    }

    /**
     * Standalone main method to run and test UserServiceImpl directly.
     */
    public static void main(String[] args) {
        System.out.println("=======================================================");
        System.out.println("   Digital OD System - UserServiceImpl Console Runner  ");
        System.out.println("=======================================================");

        UserOperations userService = new UserServiceImpl();

        // Sample registered users
        java.util.List<User> registeredUsers = new java.util.ArrayList<>();
        registeredUsers.add(new User("edwin21", "pass123", "Edwin Saji", "21CS045", "STUDENT", "Computer Science", "B.Tech CSE"));
        registeredUsers.add(new User("aisha09", "aisha2024", "Aisha Khan", "21CS046", "STUDENT", "Electronics", "B.Tech ECE"));
        registeredUsers.add(new User("staffjacob", "jacob1234", "Jacob Mathew", "STF001", "STAFF", "Administration", "-"));
        registeredUsers.add(new User("studentjohn", "pass123", "John Doe", "21MCA015", "STUDENT", "Computer Applications", "MCA"));

        try (java.util.Scanner sc = new java.util.Scanner(System.in)) {
            System.out.println("Available test users:");
            System.out.println(" - edwin21 / pass123 (Student)");
            System.out.println(" - aisha09 / aisha2024 (Student)");
            System.out.println(" - staffjacob / jacob1234 (Staff)");
            System.out.println(" - studentjohn / pass123 (Student)\n");

            System.out.print("Enter username: ");
            String loginUsername = sc.nextLine();

            System.out.print("Enter password: ");
            String loginPassword = sc.nextLine();

            try {
                userService.validateInput(loginUsername, loginPassword);

                boolean loggedIn = false;
                User matchedUser = null;
                for (User u : registeredUsers) {
                    if (userService.authenticate(u, loginUsername, loginPassword)) {
                        loggedIn = true;
                        matchedUser = u;
                        break;
                    }
                }

                if (loggedIn && matchedUser != null) {
                    System.out.println("\n[SUCCESS] Login Successful!");
                    System.out.println("Welcome, " + matchedUser.getFullName() + " (" + matchedUser.getRole() + ")");
                } else {
                    System.out.println("\n[FAILED] Login Failed! Incorrect username or password.");
                }
            } catch (InvalidInputException e) {
                System.out.println("\n[INPUT ERROR] " + e.getMessage());
            }
        }
    }
}

