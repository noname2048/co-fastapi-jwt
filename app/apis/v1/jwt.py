from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Body, HTTPException

from app.models.user import User
from app.schemas.jwt import (
    LoginRequest,
    RenewAccessTokenRequest,
    RenewAccessTokenResponse,
    TokenResponse,
    ValidateAccessTokenRequest,
)
from app.services import jwt as jwt_service

router = APIRouter(tags=["jwt"])


@router.post("/login", response_model=TokenResponse)
def login_for_access_token(form: Annotated[LoginRequest, Body(embed=True)]):
    """
    email, password 를 입력받아 access_token 과 refresh_token 을 입력받습니다.
    """
    user: User = jwt_service.authenticate_user(
        email=form.email,
        password=form.password,
    )
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password",
        )

    access_token = jwt_service.create_access_token(data={"sub": user.id})
    refresh_token = jwt_service.create_refresh_token(data={"sub": user.id})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/token", response_model=TokenResponse)
def validate_access_token(
    form: Annotated[ValidateAccessTokenRequest, Body(embed=True)]
):
    """
    access_token 이 정상인지 확인합니다.
    """
    access_token = form.access_token
    jwt_service.validate_access_token(access_token=access_token)


@router.post("/token/refresh", response_model=RenewAccessTokenResponse)
def renew_access_token_api(form: Annotated[RenewAccessTokenRequest, Body(embed=True)]):
    """
    refresh token을 이용해 access_token을 갱신합니다.
    refresh token의 expire 가 7일 이내라면 refresh token도 함께 반환합니다.
    """
    access_token, refresh_token = jwt_service.renew_access_token(
        refresh_token=form.refresh_token, timestamp=datetime.utcnow()
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )
