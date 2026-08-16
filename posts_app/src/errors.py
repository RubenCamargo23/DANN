class PostNotFoundError(Exception):
    """Exception raised when a post is not found."""

    pass


class InvalidExpirationDateError(Exception):
    """Exception raised when a post's expiration date is not valid."""

    pass
