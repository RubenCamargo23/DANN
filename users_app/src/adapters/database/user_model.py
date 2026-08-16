import uuid

from sqlalchemy import Column, DateTime, String

from adapters.database.session import Base
from clock import utcnow


def generate_uuid() -> str:
    return str(uuid.uuid4())


class UserModel(Base):
    """SQLAlchemy model for the users table."""

    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    phone_number = Column(String, nullable=True)
    dni = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    token = Column(String, nullable=True)
    status = Column(String, nullable=False, default="POR_VERIFICAR")
    expire_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)
