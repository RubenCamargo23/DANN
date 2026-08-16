from domain.models.user import User


def _new_user(username="jdoe", email="jdoe@example.com"):
    return User(
        username=username,
        email=email,
        password="hashed",
        salt="salt",
    )


def test_create_and_get_by_id(repository):
    created = repository.create(_new_user())
    assert created.id is not None

    fetched = repository.get_by_id(created.id)
    assert fetched.username == "jdoe"


def test_get_by_id_not_found(repository):
    assert repository.get_by_id("missing") is None


def test_get_by_username(repository):
    repository.create(_new_user())
    fetched = repository.get_by_username("jdoe")
    assert fetched is not None
    assert fetched.email == "jdoe@example.com"


def test_get_by_username_or_email(repository):
    repository.create(_new_user())
    assert repository.get_by_username_or_email("jdoe", "other@example.com") is not None
    assert repository.get_by_username_or_email("other", "jdoe@example.com") is not None
    assert repository.get_by_username_or_email("other", "other@example.com") is None


def test_get_by_token(repository):
    created = repository.create(_new_user())
    created.token = "some-token"
    repository.update(created)

    fetched = repository.get_by_token("some-token")
    assert fetched.id == created.id


def test_update(repository):
    created = repository.create(_new_user())
    created.full_name = "Jane Doe"
    updated = repository.update(created)
    assert updated.full_name == "Jane Doe"


def test_count(repository):
    assert repository.count() == 0
    repository.create(_new_user())
    assert repository.count() == 1


def test_reset(repository):
    repository.create(_new_user())
    assert repository.count() == 1
    repository.reset()
    assert repository.count() == 0
