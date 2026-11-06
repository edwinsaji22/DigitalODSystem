import exception.InvalidInputException;
import java.util.ArrayList;
import java.util.Scanner;
import model.User;
import service.UserOperations;
import service.UserServiceImpl;

public class MainAccessControl {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            // Your existing mini-database of users
            ArrayList<User> registeredUsers = new ArrayList<>();
            registeredUsers.add(new User("edwin21", "pass123", "Edwin Saji", "21CS045", "STUDENT", "Computer Science", "B.Tech CSE"));
            registeredUsers.add(new User("aisha09", "aisha2024", "Aisha Khan", "21CS046", "STUDENT", "Electronics", "B.Tech ECE"));
            registeredUsers.add(new User("staffjacob", "jacob1234", "Jacob Mathew", "STF001", "STAFF", "Administration", "-"));

            // Connecting to the Phase 2 interface
            UserOperations userService = new UserServiceImpl();

            System.out.println("----- LOGIN -----");
            System.out.print("Enter username: ");
            String loginUsername = sc.nextLine();
            
            System.out.print("Enter password: ");
            String loginPassword = sc.nextLine();

            // Phase 2 Exception Handling Block
            try {
                // This checks for empty inputs and triggers InvalidInputException if it finds them
                userService.validateInput(loginUsername, loginPassword);

                boolean loggedIn = false;
                
                // Loops through your users and authenticates via the service interface
                for (User u : registeredUsers) {
                    if (userService.authenticate(u, loginUsername, loginPassword)) {
                        loggedIn = true;
                        break;
                    }
                }

                if (loggedIn) {
                    System.out.println("\nLogin Successful! Welcome to the Digital OD System.");
                } else {
                    System.out.println("\nLogin Failed! Incorrect username or password.");
                }

            } catch (InvalidInputException e) {
                // If they leave a field empty, it catches the error here instead of crashing
                System.out.println("\nINPUT ERROR: " + e.getMessage());
            }
        }
    }
}