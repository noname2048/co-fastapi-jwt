from typing import Annotated

from fastapi import APIRouter, Body, status
from fastapi.responses import Response

from app.schemas import user as UserSchema
from app.services import user as user_service

router = APIRouter()


@router.get("/users", response_model=list[UserSchema.User])
async def list_users():
    return {"message": "Hello World"}


@router.post("/users")
async def create_user(db, body: Annotated[UserSchema.UserCreate, Body(embed=True)]):
    user = user_service.create_user(db, email=body.email, password=body.password)
    return user


@router.get("/user/:id", response_model=UserSchema.User)
async def retrieve_user(id: int):
    return {"message": "Hello World"}


@router.patch("/user/:id", response_model=UserSchema.User)
async def update_user(id: int):
    return {"message": "Hello World"}


@router.delete("/user/:id", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int):
    return


@router.get("/user/me", response_model=UserSchema.User)
async def retrieve_user_me():
    return {"message": "Hello World"}
