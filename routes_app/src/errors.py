class RouteNotFoundError(Exception):
    """Exception raised when a route is not found."""

    pass


class RouteAlreadyExistsError(Exception):
    """Exception raised when a route with the same flightId already exists."""

    pass


class InvalidRouteDatesError(Exception):
    """Exception raised when route dates are not valid."""

    pass
