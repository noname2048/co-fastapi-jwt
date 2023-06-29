from uuid import UUID

from pydantic import BaseModel, Field


class User(BaseModel):
    uuid: UUID
    email: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: str
    password: str
