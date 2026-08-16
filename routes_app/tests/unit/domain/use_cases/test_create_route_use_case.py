import pytest

from domain.models.route import Route
from domain.use_cases.create_route_use_case import CreateRouteUseCase
from errors import InvalidRouteDatesError, RouteAlreadyExistsError


def test_create_route_success(mocker, valid_route_data):
    repository = mocker.Mock()
    repository.get_by_flight_id.return_value = None
    repository.create.side_effect = lambda route: route

    use_case = CreateRouteUseCase(repository)
    result = use_case.execute(Route(**valid_route_data))

    assert result.flight_id == "AA001"
    repository.create.assert_called_once()


def test_create_route_duplicate_flight(mocker, valid_route_data, stored_route):
    repository = mocker.Mock()
    repository.get_by_flight_id.return_value = stored_route
    route = Route(**valid_route_data)

    use_case = CreateRouteUseCase(repository)

    with pytest.raises(RouteAlreadyExistsError):
        use_case.execute(route)

    repository.create.assert_not_called()


def test_create_route_invalid_dates(mocker, valid_route_data):
    data = {**valid_route_data}
    data["planned_end_date"] = data["planned_start_date"]
    repository = mocker.Mock()
    route = Route(**data)

    use_case = CreateRouteUseCase(repository)

    with pytest.raises(InvalidRouteDatesError):
        use_case.execute(route)

    repository.create.assert_not_called()
