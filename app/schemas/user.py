from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, SecretStr


class User(BaseModel):
    uuid: UUID = Field(..., example="123e4567-e89b-12d3-a456-426614174000")
    email: EmailStr = Field(..., example="test@test.com")

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr = Field(..., example="test@test.com")
    password: SecretStr = Field(..., example="test1234")
