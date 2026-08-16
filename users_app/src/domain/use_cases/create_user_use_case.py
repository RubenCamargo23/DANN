from datetime import datetime

from domain.models.user import User, UserStatus
from domain.ports.user_repository_port import UserRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import UserAlreadyExistsError
from security import generate_salt, hash_password


class CreateUserUseCase(BaseUseCase):
    """Use case for creating a user."""

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    def execute(self, user: User) -> User:
        """Create a new user, hashing its password with a random salt."""
        existing = self.user_repository.get_by_username_or_email(
            user.username, user.email
        )
        if existing:
            raise UserAlreadyExistsError(
                f"User with username {user.username} or email {user.email} already exists"
            )

        salt = generate_salt()
        user.salt = salt
        user.password = hash_password(user.password, salt)
        user.status = UserStatus.POR_VERIFICAR
        user.created_at = datetime.utcnow()
        user.updated_at = user.created_at
        return self.user_repository.create(user)
