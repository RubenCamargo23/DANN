import pytest
from pydantic import ValidationError

from domain.models.route import Route


def test_create_route_with_valid_data(valid_route_data):
    route = Route(**valid_route_data)
    assert route.flight_id == "AA001"
    assert route.id is None


def test_route_requires_flight_id():
    with pytest.raises(ValidationError):
        Route(
            flight_id="",
            source_airport_code="BOG",
            source_country="Colombia",
            destiny_airport_code="MIA",
            destiny_country="USA",
            bag_cost=50,
            planned_start_date="2027-01-01T10:00:00",
            planned_end_date="2027-01-01T15:00:00",
        )


def test_route_rejects_negative_bag_cost(valid_route_data):
    data = {**valid_route_data, "bag_cost": -1}
    with pytest.raises(ValidationError):
        Route(**data)
