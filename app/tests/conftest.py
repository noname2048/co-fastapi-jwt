import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.db.base import Base
from app.db.session import get_db
from app.main import app

TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test"
engine = create_engine(
    TEST_DATABASE_URL,
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def overried_get_db():
    try:
        test_db = TestingSessionLocal()
        yield test_db
    finally:
        test_db.close()


@pytest.fixture(autouse=True, scope="session")
def _sessionmaker():
    assert TEST_DATABASE_URL.endswith("test")
    if database_exists(TEST_DATABASE_URL):
        drop_database(TEST_DATABASE_URL)
    create_database(TEST_DATABASE_URL)

    try:
        Base.metadata.create_all(bind=engine)
        yield TestingSessionLocal
    finally:
        Base.metadata.drop_all(bind=engine)

    drop_database(TEST_DATABASE_URL)


@pytest.fixture(scope="function")
def db(_sessionmaker):
    try:
        test_db: Session = _sessionmaker()
        test_db.begin_nested()
        yield test_db
    finally:
        test_db.rollback()
        test_db.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def db_module(_sessionmaker):
    try:
        test_db: Session = _sessionmaker()
        test_db.begin_nested()
        yield test_db
    finally:
        test_db.rollback()
        test_db.close()


@pytest.fixture(scope="module")
def client_module(db_module):
    app.dependency_overrides[get_db] = lambda: db_module
    with TestClient(app) as client:
        yield client
