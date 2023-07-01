from sqlalchemy.orm import Session

from app.models.user import User
from app.services import user as user_service


def test_user_create(db):
    email = "test@test.com"
    password = "test1234"
    user = user_service.create_user(
        db,
        email=email,
        plain_password=password,
    )

    db_user = db.query(User).filter(User.email == email).one()
    assert db_user
    assert db_user.email == user.email == email


def test_user_second(db):
    email = "test@test.com"
    password = "test1234"
    user = user_service.create_user(
        db,
        email=email,
        plain_password=password,
    )

    db_user = db.query(User).filter(User.email == email).one()
    assert db_user
    assert db_user.email == user.email == email
