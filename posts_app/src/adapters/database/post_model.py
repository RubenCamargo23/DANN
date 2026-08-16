import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String

from adapters.database.session import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class PostModel(Base):
    """SQLAlchemy model for the posts table."""

    __tablename__ = "posts"

    id = Column(String, primary_key=True, default=generate_uuid)
    route_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    expire_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
