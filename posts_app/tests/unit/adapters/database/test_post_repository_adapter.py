from datetime import datetime, timedelta

from domain.models.post import Post


def _new_post(route_id="route-1", owner="user-1"):
    return Post(
        route_id=route_id,
        user_id=owner,
        expire_at=datetime.utcnow() + timedelta(days=1),
        created_at=datetime.utcnow(),
    )


def test_create_and_get_by_id(repository):
    created = repository.create(_new_post())
    assert created.id is not None

    fetched = repository.get_by_id(created.id)
    assert fetched.route_id == "route-1"


def test_get_by_id_not_found(repository):
    assert repository.get_by_id("missing") is None


def test_list_no_filter(repository):
    repository.create(_new_post())
    repository.create(_new_post())
    assert len(repository.list()) == 2


def test_list_filter_by_route(repository):
    repository.create(_new_post(route_id="route-1"))
    repository.create(_new_post(route_id="route-2"))
    result = repository.list(route_id="route-1")
    assert len(result) == 1


def test_list_filter_by_owner(repository):
    repository.create(_new_post(owner="user-1"))
    repository.create(_new_post(owner="user-2"))
    result = repository.list(owner_id="user-2")
    assert len(result) == 1


def test_delete(repository):
    created = repository.create(_new_post())
    repository.delete(created.id)
    assert repository.get_by_id(created.id) is None


def test_count(repository):
    assert repository.count() == 0
    repository.create(_new_post())
    assert repository.count() == 1


def test_reset(repository):
    repository.create(_new_post())
    repository.reset()
    assert repository.count() == 0
