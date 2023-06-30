from sqlalchemy.orm import Session

from app.models.user import User
from app.services import user as user_service


def test_user_create(session: Session):
    email = "test@test.com"
    password = "test1234"
    user = user_service.create_user(
        session,
        email=email,
        plain_password=password,
    )

    db_user = session.query(User).filter(User.email == email).one()
    assert db_user
    assert db_user.email == user.email == email


def test_user_second(session: Session):
    email = "test@test.com"
    password = "test1234"
    user = user_service.create_user(
        session,
        email=email,
        plain_password=password,
    )

    db_user = session.query(User).filter(User.email == email).one()
    assert db_user
    assert db_user.email == user.email == email
