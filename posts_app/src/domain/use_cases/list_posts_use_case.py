from typing import List, Optional

from clock import utcnow
from domain.models.post import Post
from domain.ports.post_repository_port import PostRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class ListPostsUseCase(BaseUseCase):
    """Use case for listing/filtering posts."""

    def __init__(self, post_repository: PostRepositoryPort):
        self.post_repository = post_repository

    def execute(
        self,
        expire: Optional[bool] = None,
        route_id: Optional[str] = None,
        owner_id: Optional[str] = None,
    ) -> List[Post]:
        """Return posts matching the given filters."""
        posts = self.post_repository.list(route_id=route_id, owner_id=owner_id)

        if expire is not None:
            now = utcnow()
            if expire:
                posts = [p for p in posts if p.expire_at <= now]
            else:
                posts = [p for p in posts if p.expire_at > now]

        return posts
