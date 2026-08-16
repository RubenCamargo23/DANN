from domain.ports.user_repository_port import UserRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class CountUsersUseCase(BaseUseCase):
    """Use case for counting stored users."""

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    def execute(self) -> int:
        """Return the total number of stored users."""
        return self.user_repository.count()
