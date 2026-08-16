from clock import utcnow
from domain.models.route import Route
from domain.ports.route_repository_port import RouteRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import InvalidRouteDatesError, RouteAlreadyExistsError


class CreateRouteUseCase(BaseUseCase):
    """Use case for creating a route."""

    def __init__(self, route_repository: RouteRepositoryPort):
        self.route_repository = route_repository

    def execute(self, route: Route) -> Route:
        """Create a new route after validating dates and flight uniqueness."""
        if route.planned_start_date < utcnow():
            raise InvalidRouteDatesError("Las fechas del trayecto no son válidas")

        if route.planned_end_date <= route.planned_start_date:
            raise InvalidRouteDatesError("Las fechas del trayecto no son válidas")

        existing = self.route_repository.get_by_flight_id(route.flight_id)
        if existing:
            raise RouteAlreadyExistsError(
                f"Route with flightId {route.flight_id} already exists"
            )

        route.created_at = utcnow()
        route.updated_at = route.created_at
        return self.route_repository.create(route)
