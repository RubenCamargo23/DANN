from datetime import datetime

from domain.models.offer import Offer, PackageSize


def _new_offer(post_id="post-1", owner="user-1"):
    return Offer(
        post_id=post_id,
        user_id=owner,
        description="Paquete de prueba",
        size=PackageSize.MEDIUM,
        fragile=False,
        offer=100.0,
        created_at=datetime.utcnow(),
    )


def test_create_and_get_by_id(repository):
    created = repository.create(_new_offer())
    assert created.id is not None

    fetched = repository.get_by_id(created.id)
    assert fetched.post_id == "post-1"


def test_get_by_id_not_found(repository):
    assert repository.get_by_id("missing") is None


def test_list_no_filter(repository):
    repository.create(_new_offer())
    repository.create(_new_offer())
    assert len(repository.list()) == 2


def test_list_filter_by_post(repository):
    repository.create(_new_offer(post_id="post-1"))
    repository.create(_new_offer(post_id="post-2"))
    result = repository.list(post_id="post-1")
    assert len(result) == 1


def test_list_filter_by_owner(repository):
    repository.create(_new_offer(owner="user-1"))
    repository.create(_new_offer(owner="user-2"))
    result = repository.list(owner_id="user-2")
    assert len(result) == 1


def test_delete(repository):
    created = repository.create(_new_offer())
    repository.delete(created.id)
    assert repository.get_by_id(created.id) is None


def test_count(repository):
    assert repository.count() == 0
    repository.create(_new_offer())
    assert repository.count() == 1


def test_reset(repository):
    repository.create(_new_offer())
    repository.reset()
    assert repository.count() == 0
