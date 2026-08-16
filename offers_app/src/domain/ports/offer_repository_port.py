from abc import ABC, abstractmethod
from typing import List, Optional

from domain.models.offer import Offer


class OfferRepositoryPort(ABC):
    """Offer repository interface."""

    @abstractmethod
    def create(self, offer: Offer) -> Offer:
        """Create a new offer."""
        pass

    @abstractmethod
    def get_by_id(self, offer_id: str) -> Optional[Offer]:
        """Get offer by id."""
        pass

    @abstractmethod
    def list(
        self,
        post_id: Optional[str] = None,
        owner_id: Optional[str] = None,
    ) -> List[Offer]:
        """List offers, optionally filtered by post and/or owner."""
        pass

    @abstractmethod
    def delete(self, offer_id: str) -> None:
        """Delete an offer."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Count stored offers."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Delete all offers."""
        pass
