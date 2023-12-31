from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas import user as user_schema
from app.schemas.jwt import (
    LoginRequest,
    RenewAccessTokenRequest,
    RenewAccessTokenResponse,
    TokenResponse,
    ValidateAccessTokenRequest,
)
from app.services import jwt as jwt_service
from app.services import user as user_service

router = APIRouter(tags=["jwt"])


@router.post("/auth/signup", response_model=user_schema.User)
def signup(
    email: Annotated[str, Body(...)],
    password: Annotated[str, Body(...)],
    db: Session = Depends(get_db),
):
    user = user_service.create_user(
        db,
        email=email,
        plain_password=password,
    )
    return user


@router.post("/auth/login", response_model=TokenResponse)
def login_for_access_token(
    form: Annotated[LoginRequest, Body(..., embed=False)],
    db: Session = Depends(get_db),
):
    """
    email, password 를 입력받아
    access_token 과 refresh_token 을 반환합니다.
    """
    user: User = jwt_service.authenticate_user(
        db,
        email=form.email,
        password=form.password,
    )
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password",
        )

    access_token = jwt_service.create_access_token(user=user)
    refresh_token = jwt_service.create_refresh_token(db=db, user=user)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/auth/verify", status_code=status.HTTP_200_OK)
def validate_access_token(
    form: Annotated[ValidateAccessTokenRequest, Body(embed=False)],
):
    """
    access_token 이 정상인지 확인합니다.
    """
    access_token = form.access_token
    jwt_service.validate_access_token(token=access_token)
    return {"message": "valid access token"}


@router.post("/auth/refresh", response_model=RenewAccessTokenResponse)
def renew_access_token_api(
    form: Annotated[RenewAccessTokenRequest, Body()],
    db: Session = Depends(get_db),
):
    """
    refresh token을 이용해 access_token을 갱신합니다.
    refresh token의 expire 가 7일 이내라면 refresh token도 함께 반환합니다.
    """
    access_token, refresh_token = jwt_service.renew_access_token(
        db,
        refresh_token=form.refresh_token,
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )
