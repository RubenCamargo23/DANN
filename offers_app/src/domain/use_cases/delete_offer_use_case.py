from domain.ports.offer_repository_port import OfferRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import OfferNotFoundError


class DeleteOfferUseCase(BaseUseCase):
    """Use case for deleting an offer."""

    def __init__(self, offer_repository: OfferRepositoryPort):
        self.offer_repository = offer_repository

    def execute(self, offer_id: str) -> None:
        """Delete an offer or raise if not found."""
        offer = self.offer_repository.get_by_id(offer_id)
        if not offer:
            raise OfferNotFoundError(f"Offer with id {offer_id} not found")
        self.offer_repository.delete(offer_id)
