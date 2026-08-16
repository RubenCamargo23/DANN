from datetime import datetime, timedelta

import pytest

from domain.models.user import User, UserStatus


@pytest.fixture
def valid_user_data():
    """Fixture providing valid user creation data."""
    return {
        "username": "jdoe",
        "password": "secret123",
        "email": "jdoe@example.com",
    }


@pytest.fixture
def stored_user():
    """Fixture providing a persisted user with hashed password."""
    return User(
        id="user-1",
        username="jdoe",
        email="jdoe@example.com",
        password="hashed-password",
        salt="some-salt",
        status=UserStatus.POR_VERIFICAR,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@pytest.fixture
def authenticated_user():
    """Fixture providing a user with a valid, non-expired token."""
    return User(
        id="user-1",
        username="jdoe",
        email="jdoe@example.com",
        password="hashed-password",
        salt="some-salt",
        token="valid-token",
        status=UserStatus.VERIFICADO,
        expire_at=datetime.utcnow() + timedelta(minutes=30),
    )
