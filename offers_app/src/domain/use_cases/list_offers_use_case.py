from typing import List, Optional

from domain.models.offer import Offer
from domain.ports.offer_repository_port import OfferRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class ListOffersUseCase(BaseUseCase):
    """Use case for listing/filtering offers."""

    def __init__(self, offer_repository: OfferRepositoryPort):
        self.offer_repository = offer_repository

    def execute(
        self,
        post_id: Optional[str] = None,
        owner_id: Optional[str] = None,
    ) -> List[Offer]:
        """Return offers matching the given filters."""
        return self.offer_repository.list(post_id=post_id, owner_id=owner_id)
