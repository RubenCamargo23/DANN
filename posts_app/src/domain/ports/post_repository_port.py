from abc import ABC, abstractmethod
from typing import List, Optional

from domain.models.post import Post


class PostRepositoryPort(ABC):
    """Post repository interface."""

    @abstractmethod
    def create(self, post: Post) -> Post:
        """Create a new post."""
        pass

    @abstractmethod
    def get_by_id(self, post_id: str) -> Optional[Post]:
        """Get post by id."""
        pass

    @abstractmethod
    def list(
        self,
        route_id: Optional[str] = None,
        owner_id: Optional[str] = None,
    ) -> List[Post]:
        """List posts, optionally filtered by route and/or owner."""
        pass

    @abstractmethod
    def delete(self, post_id: str) -> None:
        """Delete a post."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Count stored posts."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Delete all posts."""
        pass
