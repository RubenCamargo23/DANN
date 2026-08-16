from datetime import datetime, timedelta

import pytest

from domain.models.post import Post


@pytest.fixture
def valid_post_data():
    """Fixture providing valid post creation data."""
    return {
        "route_id": "route-1",
        "user_id": "user-1",
        "expire_at": datetime.utcnow() + timedelta(days=1),
    }


@pytest.fixture
def stored_post(valid_post_data):
    """Fixture providing a persisted post."""
    return Post(id="post-1", created_at=datetime.utcnow(), **valid_post_data)
