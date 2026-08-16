from domain.ports.route_repository_port import RouteRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class CountRoutesUseCase(BaseUseCase):
    """Use case for counting stored routes."""

    def __init__(self, route_repository: RouteRepositoryPort):
        self.route_repository = route_repository

    def execute(self) -> int:
        """Return the total number of stored routes."""
        return self.route_repository.count()
