from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate
from app.services.auth_service import (
    create_user,
    authenticate_user
)
from app.core.security import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    return create_user(
        db,
        user.username,
        user.email,
        user.password
    )


@router.post("/login")
def login(
    username: str,
    password: str,
    db: Session = Depends(get_db)
):

    user = authenticate_user(
        db,
        username,
        password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {
            "sub": str(user.id)
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }