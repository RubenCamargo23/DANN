from datetime import datetime

from domain.models.offer import Offer
from domain.ports.offer_repository_port import OfferRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class CreateOfferUseCase(BaseUseCase):
    """Use case for creating an offer."""

    def __init__(self, offer_repository: OfferRepositoryPort):
        self.offer_repository = offer_repository

    def execute(self, offer: Offer) -> Offer:
        """Create a new offer."""
        offer.created_at = datetime.utcnow()
        return self.offer_repository.create(offer)
