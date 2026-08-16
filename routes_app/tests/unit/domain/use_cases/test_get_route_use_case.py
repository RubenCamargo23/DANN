import pytest

from domain.use_cases.get_route_use_case import GetRouteUseCase
from errors import RouteNotFoundError


def test_get_route_success(mocker, stored_route):
    repository = mocker.Mock()
    repository.get_by_id.return_value = stored_route

    use_case = GetRouteUseCase(repository)
    result = use_case.execute(stored_route.id)

    assert result.id == stored_route.id


def test_get_route_not_found(mocker):
    repository = mocker.Mock()
    repository.get_by_id.return_value = None

    use_case = GetRouteUseCase(repository)

    with pytest.raises(RouteNotFoundError):
        use_case.execute("missing-id")
