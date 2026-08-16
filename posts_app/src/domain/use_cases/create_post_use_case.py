from clock import utcnow
from domain.models.post import Post
from domain.ports.post_repository_port import PostRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import InvalidExpirationDateError


class CreatePostUseCase(BaseUseCase):
    """Use case for creating a post."""

    def __init__(self, post_repository: PostRepositoryPort):
        self.post_repository = post_repository

    def execute(self, post: Post) -> Post:
        """Create a new post after validating the expiration date."""
        if post.expire_at <= utcnow():
            raise InvalidExpirationDateError("La fecha expiración no es válida")

        post.created_at = utcnow()
        return self.post_repository.create(post)
