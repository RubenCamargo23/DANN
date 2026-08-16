import pytest

from domain.use_cases.get_post_use_case import GetPostUseCase
from errors import PostNotFoundError


def test_get_post_success(mocker, stored_post):
    repository = mocker.Mock()
    repository.get_by_id.return_value = stored_post

    use_case = GetPostUseCase(repository)
    result = use_case.execute(stored_post.id)

    assert result.id == stored_post.id


def test_get_post_not_found(mocker):
    repository = mocker.Mock()
    repository.get_by_id.return_value = None

    use_case = GetPostUseCase(repository)

    with pytest.raises(PostNotFoundError):
        use_case.execute("missing-id")
