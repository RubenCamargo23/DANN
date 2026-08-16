import pytest

from domain.models.user import User
from domain.use_cases.create_user_use_case import CreateUserUseCase
from errors import UserAlreadyExistsError


def test_create_user_success(mocker, valid_user_data):
    repository = mocker.Mock()
    repository.get_by_username_or_email.return_value = None
    repository.create.side_effect = lambda user: user

    use_case = CreateUserUseCase(repository)
    result = use_case.execute(User(**valid_user_data))

    assert result.username == "jdoe"
    assert result.salt is not None
    assert result.password != "secret123"
    repository.create.assert_called_once()


def test_create_user_already_exists(mocker, valid_user_data, stored_user):
    repository = mocker.Mock()
    repository.get_by_username_or_email.return_value = stored_user

    use_case = CreateUserUseCase(repository)

    with pytest.raises(UserAlreadyExistsError):
        use_case.execute(User(**valid_user_data))

    repository.create.assert_not_called()
