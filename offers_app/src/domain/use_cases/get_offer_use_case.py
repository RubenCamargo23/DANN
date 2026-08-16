from domain.models.offer import Offer
from domain.ports.offer_repository_port import OfferRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import OfferNotFoundError


class GetOfferUseCase(BaseUseCase):
    """Use case for getting an offer by id."""

    def __init__(self, offer_repository: OfferRepositoryPort):
        self.offer_repository = offer_repository

    def execute(self, offer_id: str) -> Offer:
        """Return an offer or raise if not found."""
        offer = self.offer_repository.get_by_id(offer_id)
        if not offer:
            raise OfferNotFoundError(f"Offer with id {offer_id} not found")
        return offer
