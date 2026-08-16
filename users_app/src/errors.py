class UserNotFoundError(Exception):
    """Exception raised when a user is not found."""

    pass


class UserAlreadyExistsError(Exception):
    """Exception raised when a user with the same username or email already exists."""

    pass


class InvalidCredentialsError(Exception):
    """Exception raised when username/password do not match a user."""

    pass


class InvalidTokenError(Exception):
    """Exception raised when a token is missing, invalid or expired."""

    pass
