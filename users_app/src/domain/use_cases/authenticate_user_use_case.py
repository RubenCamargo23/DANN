from datetime import timedelta

from clock import utcnow
from domain.models.user import User
from domain.ports.user_repository_port import UserRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import InvalidCredentialsError
from security import generate_token, hash_password

TOKEN_TTL_MINUTES = 60


class AuthenticateUserUseCase(BaseUseCase):
    """Use case for authenticating a user and generating a session token."""

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    def execute(self, username: str, password: str) -> User:
        """Validate credentials and generate a new session token."""
        user = self.user_repository.get_by_username(username)
        if not user or hash_password(password, user.salt) != user.password:
            raise InvalidCredentialsError("Invalid username or password")

        user.token = generate_token()
        user.expire_at = utcnow() + timedelta(minutes=TOKEN_TTL_MINUTES)
        return self.user_repository.update(user)
