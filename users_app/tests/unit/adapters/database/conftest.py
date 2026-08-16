import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from adapters.database.session import Base
from adapters.database.user_repository_adapter import SQLAlchemyUserRepositoryAdapter


@pytest.fixture
def session_factory():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return factory


@pytest.fixture
def repository(session_factory):
    return SQLAlchemyUserRepositoryAdapter(session_factory)
