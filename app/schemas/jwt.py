from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str = Field(example="test@test.com")
    password: str = Field(example="test1234")


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
