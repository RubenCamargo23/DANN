from datetime import datetime, timezone


def utcnow() -> datetime:
    """Return the current UTC time as a naive datetime (no tzinfo).

    Uses timezone-aware datetime.now(timezone.utc) internally, per
    datetime.utcnow's deprecation, then strips tzinfo to stay consistent
    with the naive datetimes stored by SQLAlchemy's DateTime columns.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)
