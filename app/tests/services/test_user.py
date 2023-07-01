import pytest
from sqlalchemy.orm import Session

from app.models.user import User
from app.services import user as user_service


def test_create_user(db):
    user = user_service.create_user(
        db=db,
        email="sungwook.csw@gmail.com",
        plain_password="12345",
    )

    assert isinstance(user, User)
