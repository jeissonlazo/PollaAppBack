from click import UUID
from pydantic import BaseModel, EmailStr

from app.core.database import Base

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    first_name: str | None = None
    last_name: str | None = None

    class Config:
        from_attributes = True


class VerifyEmailRequest(BaseModel):
    email: EmailStr
    code: str


class LoginRequest(BaseModel):
    usernameOrEmail: str
    password: str


class RecoveryCode(BaseModel):
    usernameOrEmail: str


class ValidateCode(BaseModel):
    usernameOrEmail: str
    code: str


class ChangePasswordRequest(BaseModel):
    usernameOrEmail: str
    code: str
    new_password: str
