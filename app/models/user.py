from sqlalchemy import Boolean, Column, DateTime, String
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

    first_name = Column(String(50), unique=False, nullable=False)

    last_name = Column(String(50), unique=False, nullable=False)

    email_verified = Column(Boolean, default=False)

    verification_code = Column(String(5), nullable=True)

    verification_expires = Column(DateTime, nullable=True)

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String,
        nullable=False
    )
