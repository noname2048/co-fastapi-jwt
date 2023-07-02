from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from pydantic import Field, SecretStr
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import user as UserSchema
from app.services import user as user_service

router = APIRouter()


@router.get("/user/me", response_model=UserSchema.User)
async def retrieve_user_me(db: Session = Depends(get_db)):
    """자기 자신에 대한 정보를 확인 할 수 있습니다."""
    return {"message": "Hello World"}


@router.patch("/user/me", response_model=UserSchema.User)
async def update_user(id: int, db: Session = Depends(get_db)):
    """자기 자신의 정보를 수정 할 수 있습니다."""


@router.delete("/user/me", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user(db: Session = Depends(get_db)):
    """자기 자신의 정보를 삭제 조치 할 수 있습니다."""
    return


@router.get("/users", response_model=list[UserSchema.User])
async def staff_list_users():
    """관리자의 경우 유저 목록을 조회할 수 있습니다."""
    return {"message": "Hello World"}


@router.get("/user/:id", response_model=UserSchema.User)
async def staff_retrieve_user(id: int, db: Session = Depends(get_db)):
    """관리자의 경우 특정 유저를 조회할 수 있습니다."""
    return {"message": "Hello World"}


@router.delete("/user/:id", status_code=status.HTTP_204_NO_CONTENT)
async def staff_deactivate_user(id: int, db: Session = Depends(get_db)):
    """관리자의 경우 유저를 삭제 조치 할 수 있습니다."""
    return
