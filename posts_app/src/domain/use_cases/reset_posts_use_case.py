from domain.ports.post_repository_port import PostRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class ResetPostsUseCase(BaseUseCase):
    """Use case for deleting all stored posts."""

    def __init__(self, post_repository: PostRepositoryPort):
        self.post_repository = post_repository

    def execute(self) -> None:
        """Delete all posts."""
        self.post_repository.reset()
