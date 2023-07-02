from fastapi import APIRouter

from .auth import router as auth_router
from .user import router as user_router

api_router = APIRouter()
api_router.include_router(user_router, tags=["user"])
api_router.include_router(auth_router, tags=["auth"])
