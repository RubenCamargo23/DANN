import uuid

from sqlalchemy import Column, DateTime, Integer, String

from adapters.database.session import Base
from clock import utcnow


def generate_uuid() -> str:
    return str(uuid.uuid4())


class RouteModel(Base):
    """SQLAlchemy model for the routes table."""

    __tablename__ = "routes"

    id = Column(String, primary_key=True, default=generate_uuid)
    flight_id = Column(String, unique=True, nullable=False, index=True)
    source_airport_code = Column(String, nullable=False)
    source_country = Column(String, nullable=False)
    destiny_airport_code = Column(String, nullable=False)
    destiny_country = Column(String, nullable=False)
    bag_cost = Column(Integer, nullable=False)
    planned_start_date = Column(DateTime, nullable=False)
    planned_end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)
