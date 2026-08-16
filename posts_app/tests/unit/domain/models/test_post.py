import pytest
from pydantic import ValidationError

from domain.models.post import Post


def test_create_post_with_valid_data(valid_post_data):
    post = Post(**valid_post_data)
    assert post.route_id == "route-1"
    assert post.id is None


def test_post_requires_route_id(valid_post_data):
    data = {**valid_post_data, "route_id": ""}
    with pytest.raises(ValidationError):
        Post(**data)


def test_post_requires_expire_at(valid_post_data):
    data = {k: v for k, v in valid_post_data.items() if k != "expire_at"}
    with pytest.raises(ValidationError):
        Post(**data)
