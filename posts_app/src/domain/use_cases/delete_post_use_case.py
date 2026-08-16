from domain.ports.post_repository_port import PostRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import PostNotFoundError


class DeletePostUseCase(BaseUseCase):
    """Use case for deleting a post."""

    def __init__(self, post_repository: PostRepositoryPort):
        self.post_repository = post_repository

    def execute(self, post_id: str) -> None:
        """Delete a post or raise if not found."""
        post = self.post_repository.get_by_id(post_id)
        if not post:
            raise PostNotFoundError(f"Post with id {post_id} not found")
        self.post_repository.delete(post_id)
