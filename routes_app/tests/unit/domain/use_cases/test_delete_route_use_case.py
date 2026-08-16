import pytest

from domain.use_cases.delete_route_use_case import DeleteRouteUseCase
from errors import RouteNotFoundError


def test_delete_route_success(mocker, stored_route):
    repository = mocker.Mock()
    repository.get_by_id.return_value = stored_route

    use_case = DeleteRouteUseCase(repository)
    use_case.execute(stored_route.id)

    repository.delete.assert_called_once_with(stored_route.id)


def test_delete_route_not_found(mocker):
    repository = mocker.Mock()
    repository.get_by_id.return_value = None

    use_case = DeleteRouteUseCase(repository)

    with pytest.raises(RouteNotFoundError):
        use_case.execute("missing-id")

    repository.delete.assert_not_called()
