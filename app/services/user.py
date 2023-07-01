from uuid import UUID

from fastapi import status
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def create_user(db: Session, email: str, plain_password: str):
    email_already_exists_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
    )

    hashed_password = hash_password(plain_password)
    db_user = User(email=email, hashed_password=hashed_password)
    try:
        db.add(db_user)
        db.flush()
        db.refresh(db_user)
    except IntegrityError:
        raise email_already_exists_exception
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, id: int) -> User:
    return db.query(User).filter(User.id == id).first()


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def reset_password(db: Session, uuid: UUID, email: str, password: str) -> None:
    user_not_exists_exception = HTTPException(
        detail="User not exists",
        status_code=status.HTTP_404_NOT_FOUND,
    )

    try:
        db_user = db.query(User).filter(User.email == email).one()
    except NoResultFound:
        raise user_not_exists_exception
    db_user.hashed_password = password
    db.add(db_user)
    db.flush()
    return None
