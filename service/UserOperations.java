package service;

import exception.InvalidInputException;
import model.User;

public interface UserOperations {
    boolean validateInput(String username, String password) throws InvalidInputException;
    boolean authenticate(User user, String inputUsername, String inputPassword);
}