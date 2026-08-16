from adapters.database.session import SessionLocal
from adapters.database.user_repository_adapter import SQLAlchemyUserRepositoryAdapter
from domain.use_cases.authenticate_user_use_case import AuthenticateUserUseCase
from domain.use_cases.base_use_case import BaseUseCase
from domain.use_cases.count_users_use_case import CountUsersUseCase
from domain.use_cases.create_user_use_case import CreateUserUseCase
from domain.use_cases.get_authenticated_user_use_case import (
    GetAuthenticatedUserUseCase,
)
from domain.use_cases.reset_users_use_case import ResetUsersUseCase
from domain.use_cases.update_user_use_case import UpdateUserUseCase

repository: SQLAlchemyUserRepositoryAdapter = SQLAlchemyUserRepositoryAdapter(
    SessionLocal
)


def build_create_user_use_case() -> BaseUseCase:
    """Get create user use case."""
    return CreateUserUseCase(repository)


def build_update_user_use_case() -> BaseUseCase:
    """Get update user use case."""
    return UpdateUserUseCase(repository)


def build_authenticate_user_use_case() -> BaseUseCase:
    """Get authenticate user use case."""
    return AuthenticateUserUseCase(repository)


def build_get_authenticated_user_use_case() -> BaseUseCase:
    """Get authenticated user use case."""
    return GetAuthenticatedUserUseCase(repository)


def build_count_users_use_case() -> BaseUseCase:
    """Get count users use case."""
    return CountUsersUseCase(repository)


def build_reset_users_use_case() -> BaseUseCase:
    """Get reset users use case."""
    return ResetUsersUseCase(repository)
