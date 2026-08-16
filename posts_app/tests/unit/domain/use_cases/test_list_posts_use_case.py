from datetime import datetime, timedelta

from domain.models.post import Post
from domain.use_cases.list_posts_use_case import ListPostsUseCase


def test_list_posts_no_filter(mocker, stored_post):
    repository = mocker.Mock()
    repository.list.return_value = [stored_post]

    use_case = ListPostsUseCase(repository)
    result = use_case.execute()

    assert result == [stored_post]
    repository.list.assert_called_once_with(route_id=None, owner_id=None)


def test_list_posts_filter_expired(mocker, valid_post_data):
    expired = Post(
        **{**valid_post_data, "expire_at": datetime.utcnow() - timedelta(days=1)}
    )
    active = Post(**valid_post_data)
    repository = mocker.Mock()
    repository.list.return_value = [expired, active]

    use_case = ListPostsUseCase(repository)

    assert use_case.execute(expire=True) == [expired]
    assert use_case.execute(expire=False) == [active]


def test_list_posts_with_route_and_owner_filter(mocker, stored_post):
    repository = mocker.Mock()
    repository.list.return_value = [stored_post]

    use_case = ListPostsUseCase(repository)
    use_case.execute(route_id="route-1", owner_id="user-1")

    repository.list.assert_called_once_with(route_id="route-1", owner_id="user-1")
