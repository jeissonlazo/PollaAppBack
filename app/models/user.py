from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    username = Column(
        String(50),
        unique=True,
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String,
        nullable=False
    )