from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    username = Column(String(50), unique=True, nullable=False)

    first_name = Column(String(50), unique=False, nullable=False)

    last_name = Column(String(50), unique=False, nullable=False)

    email_verified = Column(Boolean, default=False)

    verification_code = Column(String(5), nullable=True)

    verification_expires = Column(DateTime, nullable=True)

    email = Column(String(100), unique=True, nullable=False)

    password_hash = Column(String, nullable=False)

    reset_code = Column(String(5), nullable=True)
    reset_code_expires = Column(DateTime, nullable=True)


class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
