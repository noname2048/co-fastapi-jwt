import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.session import get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
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
    try:  # TODO: change logic BETA for Change if Table exists
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        test_db = TestingSessionLocal()
        yield test_db
    finally:
        test_db.close()
        Base.metadata.drop_all(bind=engine)
