from domain.models.route import Route
from domain.ports.route_repository_port import RouteRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import RouteNotFoundError


class GetRouteUseCase(BaseUseCase):
    """Use case for getting a route by id."""

    def __init__(self, route_repository: RouteRepositoryPort):
        self.route_repository = route_repository

    def execute(self, route_id: str) -> Route:
        """Return a route or raise if not found."""
        route = self.route_repository.get_by_id(route_id)
        if not route:
            raise RouteNotFoundError(f"Route with id {route_id} not found")
        return route
