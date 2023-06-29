from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class ValidateAccessTokenRequest(BaseModel):
    access_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class RenewAccessTokenRequest(BaseModel):
    refresh_token: str


class RenewAccessTokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None
