from domain.ports.route_repository_port import RouteRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class ResetRoutesUseCase(BaseUseCase):
    """Use case for deleting all stored routes."""

    def __init__(self, route_repository: RouteRepositoryPort):
        self.route_repository = route_repository

    def execute(self) -> None:
        """Delete all routes."""
        self.route_repository.reset()
