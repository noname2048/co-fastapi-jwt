from datetime import datetime

from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.session import Base


class RefreshToken(Base):
    __tablename__ = "refresh_token"
    uuid = Column(UUID, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("user.uuid"), nullable=False)
    user = relationship("User", back_populates="refresh_token")

    is_active = Column(Boolean, default=True)
    is_created = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_updated = Column(DateTime, onupdate=datetime.utcnow)
