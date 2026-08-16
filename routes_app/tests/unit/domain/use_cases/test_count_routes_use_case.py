from domain.use_cases.count_routes_use_case import CountRoutesUseCase


def test_count_routes(mocker):
    repository = mocker.Mock()
    repository.count.return_value = 2

    use_case = CountRoutesUseCase(repository)

    assert use_case.execute() == 2
