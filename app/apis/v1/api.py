from fastapi import APIRouter

from .jwt import router as jwt_router
from .user import router as user_router

api_router = APIRouter()
api_router.include_router(user_router, tags=["user"])
# api_router.include_router(jwt_router, tags=["jwt"])
