from datetime import datetime, timedelta

import pytest

from domain.use_cases.get_authenticated_user_use_case import (
    GetAuthenticatedUserUseCase,
)
from errors import InvalidTokenError


def test_get_authenticated_user_success(mocker, authenticated_user):
    repository = mocker.Mock()
    repository.get_by_token.return_value = authenticated_user

    use_case = GetAuthenticatedUserUseCase(repository)
    result = use_case.execute("valid-token")

    assert result.username == "jdoe"


def test_get_authenticated_user_expired_token(mocker, authenticated_user):
    authenticated_user.expire_at = datetime.utcnow() - timedelta(minutes=1)
    repository = mocker.Mock()
    repository.get_by_token.return_value = authenticated_user

    use_case = GetAuthenticatedUserUseCase(repository)

    with pytest.raises(InvalidTokenError):
        use_case.execute("valid-token")


def test_get_authenticated_user_not_found(mocker):
    repository = mocker.Mock()
    repository.get_by_token.return_value = None

    use_case = GetAuthenticatedUserUseCase(repository)

    with pytest.raises(InvalidTokenError):
        use_case.execute("missing-token")
