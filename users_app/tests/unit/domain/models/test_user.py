import pytest
from pydantic import ValidationError

from domain.models.user import User, UserStatus


def test_create_user_with_valid_data(valid_user_data):
    user = User(**valid_user_data)
    assert user.username == "jdoe"
    assert user.status == UserStatus.POR_VERIFICAR
    assert user.id is None


def test_user_requires_username():
    with pytest.raises(ValidationError):
        User(username="", password="secret123", email="jdoe@example.com")


def test_user_requires_valid_email():
    with pytest.raises(ValidationError):
        User(username="jdoe", password="secret123", email="not-an-email")


def test_user_optional_fields_default_to_none():
    user = User(username="jdoe", password="secret123", email="jdoe@example.com")
    assert user.dni is None
    assert user.full_name is None
    assert user.phone_number is None
    assert user.token is None
