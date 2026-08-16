import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import assembly
from adapters.database import session as db_session
from adapters.database.user_repository_adapter import SQLAlchemyUserRepositoryAdapter
from entrypoints.api.main import app


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db_session.engine = engine
    db_session.SessionLocal = session_factory
    assembly.repository = SQLAlchemyUserRepositoryAdapter(session_factory)

    with TestClient(app) as c:
        yield c
