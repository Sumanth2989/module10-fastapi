# tests/test_users_integration.py
import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import ProgrammingError
import psycopg2

from app.db import Base
from app import models, schemas, crud

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "sqlite:///./test.db",
)

# Ensure the target database exists when pointing at Postgres; otherwise, use SQLite.
def _ensure_database_exists(url: str) -> None:
    parsed = make_url(url)
    if not parsed.drivername.startswith("postgresql"):
        return

    admin_url = parsed.set(database="postgres")
    engine = create_engine(admin_url, isolation_level="AUTOCOMMIT", future=True)
    try:
        with engine.connect() as conn:
            conn.execute(text(f'CREATE DATABASE "{parsed.database}"'))
    except ProgrammingError as exc:
        # Ignore "database already exists" errors so repeated test runs work.
        if not isinstance(getattr(exc, "orig", None), psycopg2.errors.DuplicateDatabase):
            raise
    finally:
        engine.dispose()


_ensure_database_exists(TEST_DATABASE_URL)

connect_args = {"check_same_thread": False} if TEST_DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(TEST_DATABASE_URL, connect_args=connect_args, future=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_user_and_uniqueness(db_session):
    user_in = schemas.UserCreate(
        username="uniqueuser",
        email="unique@example.com",
        password="password123",
    )
    user = crud.create_user(db_session, user_in)
    assert user.id is not None

    # try recreating with same email
    user_in2 = schemas.UserCreate(
        username="othername",
        email="unique@example.com",
        password="password123",
    )
    with pytest.raises(Exception):
        crud.create_user(db_session, user_in2)


def test_invalid_email_schema_integration():
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        schemas.UserCreate(
            username="user",
            email="invalidemail",
            password="password123",
        )
