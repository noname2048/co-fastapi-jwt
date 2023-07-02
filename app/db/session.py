from contextvars import ContextVar
from functools import wraps
from typing import Callable, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DB_URL,
    echo=settings.DB_ECHO,
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
        db.rollback()  # every uncommited transaction will be rollbacked
    finally:
        db.close()
