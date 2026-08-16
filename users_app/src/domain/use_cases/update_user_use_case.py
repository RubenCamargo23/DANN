from typing import Optional

from clock import utcnow
from domain.models.user import User
from domain.ports.user_repository_port import UserRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import UserNotFoundError


class UpdateUserUseCase(BaseUseCase):
    """Use case for updating a user."""

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    def execute(
        self,
        user_id: str,
        status: Optional[str] = None,
        dni: Optional[str] = None,
        full_name: Optional[str] = None,
        phone_number: Optional[str] = None,
    ) -> User:
        """Update fields of an existing user."""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")

        if status is not None:
            user.status = status
        if dni is not None:
            user.dni = dni
        if full_name is not None:
            user.full_name = full_name
        if phone_number is not None:
            user.phone_number = phone_number
        user.updated_at = utcnow()

        return self.user_repository.update(user)
