from domain.use_cases.count_users_use_case import CountUsersUseCase


def test_count_users(mocker):
    repository = mocker.Mock()
    repository.count.return_value = 3

    use_case = CountUsersUseCase(repository)

    assert use_case.execute() == 3
