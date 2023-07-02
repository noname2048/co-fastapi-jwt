from datetime import datetime, timedelta
from typing import Annotated
from uuid import uuid4

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.jwt import RefreshToken
from app.models.user import User
from app.services.user import get_user_by_email, get_user_by_id

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS
REFRESH_TOKEN_RENEW_DAYS = settings.REFRESH_TOKEN_RENEW_DAYS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)


def authenticate_user(db, email: str, password: str):
    user: User = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    user: User,
    expires_delta: timedelta = None,
    current_time: datetime = None,
) -> str:
    """
    user 의 uuid 를 payload 에 넣어 access_token 을 생성합니다.
    """
    expires_delta = expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    current_time = current_time or datetime.utcnow()

    to_encode = {
        "aud": str(user.uuid),
        "exp": datetime.utcnow() + expires_delta,
        "token_type": "access",
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def validate_access_token(token, current_time: datetime = None) -> None:
    current_time = current_time or datetime.utcnow()

    invalid_token_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid token",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise invalid_token_exception

    if payload["token_type"] != "access":
        raise invalid_token_exception

    if payload["exp"] < current_time:
        raise invalid_token_exception


def create_refresh_token(
    db: Session,
    user: User,
    expires_delta: timedelta = None,
    current_time: datetime = None,
) -> str:
    """
    refresh token 을 생성하고 jit를 DB에 저장합니다.
    """
    expires_delta = expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    current_time = current_time or datetime.utcnow()

    db_refresh_token: RefreshToken = RefreshToken(uuid=uuid4(), user_id=user.uuid)
    db.add(db_refresh_token)
    db.flush()
    db.refresh(db_refresh_token)

    to_encode = {
        "aud": str(user.uuid),
        "jit": str(db_refresh_token.uuid),
        "exp": current_time + expires_delta,
        "token_type": "refresh",
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def renew_access_token(db: Session, refresh_token: str, timestamp: datetime):
    """refresh token 을 받아 access token 을 갱신합니다.
    refresh token 은 DB를 체크합니다.

    - 토큰검증
    - 토큰타입검증
    - 만료검증
    - DB 검증 (성능을 위해 최대한 나중에 합니다)
    - 토큰갱신
    """

    # generral token error
    invalid_token_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid token",
    )

    try:
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except JWTError:
        raise invalid_token_exception

    # 타입 검증
    if payload["token_type"] != "refresh":
        raise invalid_token_exception

    # 만료 검증
    exp = payload.get("exp")
    if datetime.stptime(exp, "%Y-%m-%d %H:%M:%S.%f %z") < timestamp:
        expired_token_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expired token",
        )
        raise expired_token_exception

    # jit 검증
    jit = payload["jit"]
    db_refresh_token = db.query(RefreshToken).filter(RefreshToken.uuid == jit).one()
    if not db_refresh_token:
        raise invalid_token_exception

    # aud 검증
    uuid = payload["uuid"]
    db_user = db.query(User).filter(User.uuid == uuid, User.is_activate is True).one()
    if not db_user:
        raise invalid_token_exception

    access_token = create_access_token(data=payload)

    if exp > timestamp - timedelta(days=REFRESH_TOKEN_RENEW_DAYS):
        refresh_token = create_refresh_token(data=payload)
        return access_token, refresh_token

    return access_token, refresh_token


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """access token을 받아서 user를 반환합니다."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        token_type: str = payload.get("token_type")
        # email is required
        if id is None:
            raise credentials_exception
        # token type access only
        if token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_id(id=id)
    if user is None:
        raise credentials_exception
    return user
