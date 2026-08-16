from domain.models.post import Post
from domain.ports.post_repository_port import PostRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import PostNotFoundError


class GetPostUseCase(BaseUseCase):
    """Use case for getting a post by id."""

    def __init__(self, post_repository: PostRepositoryPort):
        self.post_repository = post_repository

    def execute(self, post_id: str) -> Post:
        """Return a post or raise if not found."""
        post = self.post_repository.get_by_id(post_id)
        if not post:
            raise PostNotFoundError(f"Post with id {post_id} not found")
        return post
