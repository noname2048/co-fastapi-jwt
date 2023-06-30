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


app.dependency_overrides[get_db] = overried_get_db

client = TestClient(app)


@pytest.fixture(autouse=True, scope="session")
def db():
    # assert TEST_DATABASE_URL.endswith("test")
    # if database_exists(TEST_DATABASE_URL):
    #     drop_database(TEST_DATABASE_URL)
    # create_database(TEST_DATABASE_URL)

    try:  # TODO: change logic BETA for Change if Table exists
        Base.metadata.create_all(bind=engine)
        test_db = TestingSessionLocal()
        yield test_db
    finally:
        test_db.close()
        Base.metadata.drop_all(bind=engine)

    # drop_database(TEST_DATABASE_URL)


@pytest.fixture
def engine(db: Session) -> Session:
    db.begin_nested()
    yield db
    db.rollback()


@pytest.fixture
def client(session):
    app.dependency_overrides[get_db] = lambda: session
    return TestClient(app)
