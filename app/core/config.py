from pathlib import Path
from typing import List

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    REFRESH_TOKEN_RENEW_DAYS: int

    DB_URL: str
    DB_ECHO: bool

    BACKEND_CORS_ORIGINS: list[str]

    class Config:
        env_file_encoding = "utf-8"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> str | List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        return v


REPO_DIR = Path(__file__).parent.parent.parent
ENV_DIR = REPO_DIR / "envs/.env.local"
settings = Settings(_env_file=ENV_DIR)
