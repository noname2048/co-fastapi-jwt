from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware

from .apis.v1.api import api_router as v1_api_router
from .core.config import settings

app = FastAPI(title="FastAPI JWT Tutorial")


@app.get("/", response_class=HTMLResponse)
async def root():
    return "<h1>Hello World</h1>"


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(v1_api_router, prefix="/api/v1")
