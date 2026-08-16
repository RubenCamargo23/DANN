from typing import List, Optional

from domain.models.route import Route
from domain.ports.route_repository_port import RouteRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class ListRoutesUseCase(BaseUseCase):
    """Use case for listing/filtering routes."""

    def __init__(self, route_repository: RouteRepositoryPort):
        self.route_repository = route_repository

    def execute(self, flight_id: Optional[str] = None) -> List[Route]:
        """Return all routes, optionally filtered by flight id."""
        return self.route_repository.list(flight_id=flight_id)
