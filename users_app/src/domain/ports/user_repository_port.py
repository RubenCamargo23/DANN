from abc import ABC, abstractmethod
from typing import Optional

from domain.models.user import User


class UserRepositoryPort(ABC):
    """User repository interface."""

    @abstractmethod
    def create(self, user: User) -> User:
        """Create a new user."""
        pass

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by id."""
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        pass

    @abstractmethod
    def get_by_username_or_email(self, username: str, email: str) -> Optional[User]:
        """Get user by username or email."""
        pass

    @abstractmethod
    def get_by_token(self, token: str) -> Optional[User]:
        """Get user by session token."""
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Update an existing user."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Count stored users."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Delete all users."""
        pass
