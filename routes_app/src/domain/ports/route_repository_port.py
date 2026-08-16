from abc import ABC, abstractmethod
from typing import List, Optional

from domain.models.route import Route


class RouteRepositoryPort(ABC):
    """Route repository interface."""

    @abstractmethod
    def create(self, route: Route) -> Route:
        """Create a new route."""
        pass

    @abstractmethod
    def get_by_id(self, route_id: str) -> Optional[Route]:
        """Get route by id."""
        pass

    @abstractmethod
    def get_by_flight_id(self, flight_id: str) -> Optional[Route]:
        """Get route by flight id."""
        pass

    @abstractmethod
    def list(self, flight_id: Optional[str] = None) -> List[Route]:
        """List routes, optionally filtered by flight id."""
        pass

    @abstractmethod
    def delete(self, route_id: str) -> None:
        """Delete a route."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Count stored routes."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Delete all routes."""
        pass
