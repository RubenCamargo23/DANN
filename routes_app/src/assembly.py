from adapters.database.route_repository_adapter import SQLAlchemyRouteRepositoryAdapter
from adapters.database.session import SessionLocal
from domain.use_cases.base_use_case import BaseUseCase
from domain.use_cases.count_routes_use_case import CountRoutesUseCase
from domain.use_cases.create_route_use_case import CreateRouteUseCase
from domain.use_cases.delete_route_use_case import DeleteRouteUseCase
from domain.use_cases.get_route_use_case import GetRouteUseCase
from domain.use_cases.list_routes_use_case import ListRoutesUseCase
from domain.use_cases.reset_routes_use_case import ResetRoutesUseCase

repository: SQLAlchemyRouteRepositoryAdapter = SQLAlchemyRouteRepositoryAdapter(
    SessionLocal
)


def build_create_route_use_case() -> BaseUseCase:
    """Get create route use case."""
    return CreateRouteUseCase(repository)


def build_get_route_use_case() -> BaseUseCase:
    """Get route use case."""
    return GetRouteUseCase(repository)


def build_list_routes_use_case() -> BaseUseCase:
    """Get list routes use case."""
    return ListRoutesUseCase(repository)


def build_delete_route_use_case() -> BaseUseCase:
    """Get delete route use case."""
    return DeleteRouteUseCase(repository)


def build_count_routes_use_case() -> BaseUseCase:
    """Get count routes use case."""
    return CountRoutesUseCase(repository)


def build_reset_routes_use_case() -> BaseUseCase:
    """Get reset routes use case."""
    return ResetRoutesUseCase(repository)
