import pytest

from domain.use_cases.delete_post_use_case import DeletePostUseCase
from errors import PostNotFoundError


def test_delete_post_success(mocker, stored_post):
    repository = mocker.Mock()
    repository.get_by_id.return_value = stored_post

    use_case = DeletePostUseCase(repository)
    use_case.execute(stored_post.id)

    repository.delete.assert_called_once_with(stored_post.id)


def test_delete_post_not_found(mocker):
    repository = mocker.Mock()
    repository.get_by_id.return_value = None

    use_case = DeletePostUseCase(repository)

    with pytest.raises(PostNotFoundError):
        use_case.execute("missing-id")

    repository.delete.assert_not_called()
