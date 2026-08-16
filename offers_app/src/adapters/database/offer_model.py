import uuid

from sqlalchemy import Boolean, Column, DateTime, Float, String

from adapters.database.session import Base
from clock import utcnow


def generate_uuid() -> str:
    return str(uuid.uuid4())


class OfferModel(Base):
    """SQLAlchemy model for the offers table."""

    __tablename__ = "offers"

    id = Column(String, primary_key=True, default=generate_uuid)
    post_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    description = Column(String(140), nullable=False)
    size = Column(String, nullable=False)
    fragile = Column(Boolean, nullable=False, default=False)
    offer = Column(Float, nullable=False)
    created_at = Column(DateTime, default=utcnow)
