from domain.use_cases.reset_routes_use_case import ResetRoutesUseCase


def test_reset_routes(mocker):
    repository = mocker.Mock()

    use_case = ResetRoutesUseCase(repository)
    use_case.execute()

    repository.reset.assert_called_once()
