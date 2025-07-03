"""
Configuration for testing the project.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session


from fastapi.testclient import TestClient

from app.main import app
from ..models.user import Base
from ..repository.user_repository import get_session_db


SQLITE_DATABASE_URL = "sqlite:///./test_db.db"

# Create a SQLAlchemy engine
engine = create_engine(
    SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create a sessionmaker to manage sessions
TestingUserSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Create tables in the database
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Create a new database session with a rollback at the end of the test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingUserSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()
