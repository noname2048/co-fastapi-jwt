from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from pydantic import Field, SecretStr
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import user as UserSchema
from app.services import user as user_service

router = APIRouter()


@router.get("/users", response_model=list[UserSchema.User])
async def list_users():
    return {"message": "Hello World"}


@router.post("/users", response_model=UserSchema.User)
async def create_user(
    email: Annotated[str, Body(...)],
    password: Annotated[str, Body(...)],
    db: Session = Depends(get_db),
):
    user = user_service.create_user(
        db,
        email=email,
        plain_password=str(password),
    )
    return user


@router.get("/user/:id", response_model=UserSchema.User)
async def retrieve_user(id: int, db: Session = Depends(get_db)):
    return {"message": "Hello World"}


@router.patch("/user/:id", response_model=UserSchema.User)
async def update_user(id: int, db: Session = Depends(get_db)):
    return {"message": "Hello World"}


@router.delete("/user/:id", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(get_db)):
    return


@router.get("/user/me", response_model=UserSchema.User)
async def retrieve_user_me(db: Session = Depends(get_db)):
    return {"message": "Hello World"}
