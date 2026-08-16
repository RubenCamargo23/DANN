from domain.use_cases.reset_users_use_case import ResetUsersUseCase


def test_reset_users(mocker):
    repository = mocker.Mock()

    use_case = ResetUsersUseCase(repository)
    use_case.execute()

    repository.reset.assert_called_once()
