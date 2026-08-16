from clock import utcnow
from domain.models.user import User
from domain.ports.user_repository_port import UserRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import InvalidTokenError


class GetAuthenticatedUserUseCase(BaseUseCase):
    """Use case for retrieving the user that owns a session token."""

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    def execute(self, token: str) -> User:
        """Return the user owning the token, if valid and not expired."""
        user = self.user_repository.get_by_token(token)
        if not user or not user.expire_at or user.expire_at < utcnow():
            raise InvalidTokenError("Invalid or expired token")
        return user
