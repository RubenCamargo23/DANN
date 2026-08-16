import pytest

from domain.use_cases.update_user_use_case import UpdateUserUseCase
from errors import UserNotFoundError


def test_update_user_success(mocker, stored_user):
    repository = mocker.Mock()
    repository.get_by_id.return_value = stored_user
    repository.update.side_effect = lambda user: user

    use_case = UpdateUserUseCase(repository)
    result = use_case.execute(stored_user.id, full_name="Jane Doe")

    assert result.full_name == "Jane Doe"
    repository.update.assert_called_once()


def test_update_user_not_found(mocker):
    repository = mocker.Mock()
    repository.get_by_id.return_value = None

    use_case = UpdateUserUseCase(repository)

    with pytest.raises(UserNotFoundError):
        use_case.execute("missing-id", full_name="Jane Doe")

    repository.update.assert_not_called()


def test_update_user_only_modifies_provided_fields(mocker, stored_user):
    repository = mocker.Mock()
    repository.get_by_id.return_value = stored_user
    repository.update.side_effect = lambda user: user

    use_case = UpdateUserUseCase(repository)
    result = use_case.execute(stored_user.id, dni="123456")

    assert result.dni == "123456"
    assert result.username == "jdoe"
