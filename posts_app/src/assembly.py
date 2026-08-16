from adapters.database.post_repository_adapter import SQLAlchemyPostRepositoryAdapter
from adapters.database.session import SessionLocal
from domain.use_cases.base_use_case import BaseUseCase
from domain.use_cases.count_posts_use_case import CountPostsUseCase
from domain.use_cases.create_post_use_case import CreatePostUseCase
from domain.use_cases.delete_post_use_case import DeletePostUseCase
from domain.use_cases.get_post_use_case import GetPostUseCase
from domain.use_cases.list_posts_use_case import ListPostsUseCase
from domain.use_cases.reset_posts_use_case import ResetPostsUseCase

repository: SQLAlchemyPostRepositoryAdapter = SQLAlchemyPostRepositoryAdapter(
    SessionLocal
)


def build_create_post_use_case() -> BaseUseCase:
    """Get create post use case."""
    return CreatePostUseCase(repository)


def build_get_post_use_case() -> BaseUseCase:
    """Get post use case."""
    return GetPostUseCase(repository)


def build_list_posts_use_case() -> BaseUseCase:
    """Get list posts use case."""
    return ListPostsUseCase(repository)


def build_delete_post_use_case() -> BaseUseCase:
    """Get delete post use case."""
    return DeletePostUseCase(repository)


def build_count_posts_use_case() -> BaseUseCase:
    """Get count posts use case."""
    return CountPostsUseCase(repository)


def build_reset_posts_use_case() -> BaseUseCase:
    """Get reset posts use case."""
    return ResetPostsUseCase(repository)
