from datetime import datetime, timedelta

from domain.models.route import Route


def _new_route(flight_id="AA001"):
    start = datetime.utcnow() + timedelta(days=1)
    return Route(
        flight_id=flight_id,
        source_airport_code="BOG",
        source_country="Colombia",
        destiny_airport_code="MIA",
        destiny_country="USA",
        bag_cost=50,
        planned_start_date=start,
        planned_end_date=start + timedelta(hours=5),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


def test_create_and_get_by_id(repository):
    created = repository.create(_new_route())
    assert created.id is not None

    fetched = repository.get_by_id(created.id)
    assert fetched.flight_id == "AA001"


def test_get_by_id_not_found(repository):
    assert repository.get_by_id("missing") is None


def test_get_by_flight_id(repository):
    repository.create(_new_route())
    assert repository.get_by_flight_id("AA001") is not None
    assert repository.get_by_flight_id("missing") is None


def test_list_no_filter(repository):
    repository.create(_new_route("AA001"))
    repository.create(_new_route("BB002"))
    assert len(repository.list()) == 2


def test_list_with_filter(repository):
    repository.create(_new_route("AA001"))
    repository.create(_new_route("BB002"))
    result = repository.list(flight_id="AA001")
    assert len(result) == 1
    assert result[0].flight_id == "AA001"


def test_delete(repository):
    created = repository.create(_new_route())
    repository.delete(created.id)
    assert repository.get_by_id(created.id) is None


def test_count(repository):
    assert repository.count() == 0
    repository.create(_new_route())
    assert repository.count() == 1


def test_reset(repository):
    repository.create(_new_route())
    repository.reset()
    assert repository.count() == 0
