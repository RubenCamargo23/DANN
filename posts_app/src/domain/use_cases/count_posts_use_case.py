from domain.ports.post_repository_port import PostRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class CountPostsUseCase(BaseUseCase):
    """Use case for counting stored posts."""

    def __init__(self, post_repository: PostRepositoryPort):
        self.post_repository = post_repository

    def execute(self) -> int:
        """Return the total number of stored posts."""
        return self.post_repository.count()
