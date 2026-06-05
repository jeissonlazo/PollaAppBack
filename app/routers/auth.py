from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, VerifyEmailRequest
from app.services.auth_service import create_user, authenticate_user, verify_email
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    return await create_user(
        db, user.username, user.email, user.password, user.first_name, user.last_name
    )


@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):

    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}


@router.post("/verify-email")
def verify_email_endpoint(request: VerifyEmailRequest, db: Session = Depends(get_db)):

    success = verify_email(db=db, email=request.email, code=request.code)

    if not success:
        raise HTTPException(status_code=400, detail="Invalid code")

    return {"message": "Email verified"}
