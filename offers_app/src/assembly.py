from adapters.database.offer_repository_adapter import SQLAlchemyOfferRepositoryAdapter
from adapters.database.session import SessionLocal
from domain.use_cases.base_use_case import BaseUseCase
from domain.use_cases.count_offers_use_case import CountOffersUseCase
from domain.use_cases.create_offer_use_case import CreateOfferUseCase
from domain.use_cases.delete_offer_use_case import DeleteOfferUseCase
from domain.use_cases.get_offer_use_case import GetOfferUseCase
from domain.use_cases.list_offers_use_case import ListOffersUseCase
from domain.use_cases.reset_offers_use_case import ResetOffersUseCase

repository: SQLAlchemyOfferRepositoryAdapter = SQLAlchemyOfferRepositoryAdapter(
    SessionLocal
)


def build_create_offer_use_case() -> BaseUseCase:
    """Get create offer use case."""
    return CreateOfferUseCase(repository)


def build_get_offer_use_case() -> BaseUseCase:
    """Get offer use case."""
    return GetOfferUseCase(repository)


def build_list_offers_use_case() -> BaseUseCase:
    """Get list offers use case."""
    return ListOffersUseCase(repository)


def build_delete_offer_use_case() -> BaseUseCase:
    """Get delete offer use case."""
    return DeleteOfferUseCase(repository)


def build_count_offers_use_case() -> BaseUseCase:
    """Get count offers use case."""
    return CountOffersUseCase(repository)


def build_reset_offers_use_case() -> BaseUseCase:
    """Get reset offers use case."""
    return ResetOffersUseCase(repository)
