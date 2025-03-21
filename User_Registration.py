"""
Module for user registration functionality.
"""


class UserRegistration:
    """
    A user registration system to store user data.

    The `users` dict maps an email to a dict containing the user's
    password and confirmation status.
    """

    def __init__(self):
        """Initialize with an empty dictionary."""
        self.users = {}

    def register(self, email, password, confirm_password):
        """
        Register a new user.

        Checks:
         - Email format
         - Password matches confirmation
         - Password strength
         - Email not already registered

        On success, stores user with `confirmed=False` and returns a
        success message.

        Args:
            email (str): The user's email.
            password (str): The user's password.
            confirm_password (str): Confirmation password.

        Returns:
            dict:
                - Success: {"success": True, "message": "..."}
                - Failure: {"success": False, "error": "..."}
        """
        if not self.is_valid_email(email):
            return {"success": False, "error": "Invalid email format"}
        if password != confirm_password:
            return {"success": False, "error": "Passwords do not match"}
        if not self.is_strong_password(password):
            return {"success": False, "error": "Password is not strong enough"}
        if email in self.users:
            return {"success": False, "error": "Email already registered"}

        self.users[email] = {"password": password, "confirmed": False}
        return {
            "success": True,
            "message": "Registration successful, confirmation email sent"
        }

    def is_valid_email(self, email):
        """
        Check if the provided email is valid.

        A valid email has an '@' symbol and a '.' in the domain part.

        Args:
            email (str): The email address.

        Returns:
            bool: True if valid, else False.
        """
        return "@" in email and "." in email.split("@")[-1]

    def is_strong_password(self, password):
        """
        Check if the password meets strength requirements.

        A strong password is at least 8 characters long and has at
        least one letter and one digit.

        Args:
            password (str): The password to check.

        Returns:
            bool: True if strong, else False.
        """
        return (
            len(password) >= 8
            and any(c.isdigit() for c in password)
            and any(c.isalpha() for c in password)
        )
