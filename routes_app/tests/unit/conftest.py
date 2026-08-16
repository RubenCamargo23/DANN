from datetime import datetime, timedelta

import pytest

from domain.models.route import Route


@pytest.fixture
def valid_route_data():
    """Fixture providing valid route creation data."""
    start = datetime.utcnow() + timedelta(days=1)
    return {
        "flight_id": "AA001",
        "source_airport_code": "BOG",
        "source_country": "Colombia",
        "destiny_airport_code": "MIA",
        "destiny_country": "USA",
        "bag_cost": 50,
        "planned_start_date": start,
        "planned_end_date": start + timedelta(hours=5),
    }


@pytest.fixture
def stored_route(valid_route_data):
    """Fixture providing a persisted route."""
    return Route(
        id="route-1",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        **valid_route_data,
    )
