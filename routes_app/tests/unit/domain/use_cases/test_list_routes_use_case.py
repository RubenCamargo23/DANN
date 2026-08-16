from domain.use_cases.list_routes_use_case import ListRoutesUseCase


def test_list_routes_no_filter(mocker, stored_route):
    repository = mocker.Mock()
    repository.list.return_value = [stored_route]

    use_case = ListRoutesUseCase(repository)
    result = use_case.execute()

    assert result == [stored_route]
    repository.list.assert_called_once_with(flight_id=None)


def test_list_routes_with_filter(mocker, stored_route):
    repository = mocker.Mock()
    repository.list.return_value = [stored_route]

    use_case = ListRoutesUseCase(repository)
    use_case.execute(flight_id="AA001")

    repository.list.assert_called_once_with(flight_id="AA001")
