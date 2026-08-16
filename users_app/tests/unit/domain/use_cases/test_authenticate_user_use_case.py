import pytest

from domain.use_cases.authenticate_user_use_case import AuthenticateUserUseCase
from errors import InvalidCredentialsError
from security import hash_password


def test_authenticate_success(mocker, stored_user):
    stored_user.password = hash_password("secret123", stored_user.salt)
    repository = mocker.Mock()
    repository.get_by_username.return_value = stored_user
    repository.update.side_effect = lambda user: user

    use_case = AuthenticateUserUseCase(repository)
    result = use_case.execute("jdoe", "secret123")

    assert result.token is not None
    assert result.expire_at is not None


def test_authenticate_wrong_password(mocker, stored_user):
    stored_user.password = hash_password("secret123", stored_user.salt)
    repository = mocker.Mock()
    repository.get_by_username.return_value = stored_user

    use_case = AuthenticateUserUseCase(repository)

    with pytest.raises(InvalidCredentialsError):
        use_case.execute("jdoe", "wrong-password")


def test_authenticate_user_not_found(mocker):
    repository = mocker.Mock()
    repository.get_by_username.return_value = None

    use_case = AuthenticateUserUseCase(repository)

    with pytest.raises(InvalidCredentialsError):
        use_case.execute("missing", "secret123")
