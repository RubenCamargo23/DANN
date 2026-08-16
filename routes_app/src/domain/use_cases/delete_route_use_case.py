from domain.ports.route_repository_port import RouteRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import RouteNotFoundError


class DeleteRouteUseCase(BaseUseCase):
    """Use case for deleting a route."""

    def __init__(self, route_repository: RouteRepositoryPort):
        self.route_repository = route_repository

    def execute(self, route_id: str) -> None:
        """Delete a route or raise if not found."""
        route = self.route_repository.get_by_id(route_id)
        if not route:
            raise RouteNotFoundError(f"Route with id {route_id} not found")
        self.route_repository.delete(route_id)
