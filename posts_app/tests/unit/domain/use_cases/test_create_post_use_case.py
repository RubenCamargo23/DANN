from datetime import datetime, timedelta

import pytest

from domain.models.post import Post
from domain.use_cases.create_post_use_case import CreatePostUseCase
from errors import InvalidExpirationDateError


def test_create_post_success(mocker, valid_post_data):
    repository = mocker.Mock()
    repository.create.side_effect = lambda post: post

    use_case = CreatePostUseCase(repository)
    result = use_case.execute(Post(**valid_post_data))

    assert result.route_id == "route-1"
    repository.create.assert_called_once()


def test_create_post_invalid_expire_date(mocker, valid_post_data):
    data = {**valid_post_data, "expire_at": datetime.utcnow() - timedelta(days=1)}
    repository = mocker.Mock()
    post = Post(**data)

    use_case = CreatePostUseCase(repository)

    with pytest.raises(InvalidExpirationDateError):
        use_case.execute(post)

    repository.create.assert_not_called()
