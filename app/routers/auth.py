from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import (
    ChangePasswordRequest,
    RecoveryCode,
    UserCreate,
    ValidateCode,
    VerifyEmailRequest,
)
from app.services.auth_service import (
    change_password,
    create_user,
    authenticate_user,
    forgot_password,
    validate_reset_code,
    verify_email,
)
from app.core.security import create_access_token
from app.schemas.user import LoginRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    print(f"Registering user: {user.username}, {user.email}")
    return await create_user(
        db, user.username, user.email, user.password, user.first_name, user.last_name
    )


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):

    user = authenticate_user(db, request.usernameOrEmail, request.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id), "roles": user.roles})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "roles": user.roles,
        },
    }


@router.post("/verify-email")
def verify_email_endpoint(request: VerifyEmailRequest, db: Session = Depends(get_db)):

    success = verify_email(db=db, email=request.email, code=request.code)

    if not success:
        raise HTTPException(status_code=400, detail="Invalid code")

    return {"message": "Email verified"}


@router.post("/send-recovery-code")
async def forgot_password_endpoint(
    request: RecoveryCode, db: Session = Depends(get_db)
):
    print(f"Received forgot password request for: {request.usernameOrEmail}")
    success = await forgot_password(db=db, username_or_email=request.usernameOrEmail)

    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Verification code sent"}


@router.post("/validate-recovery-code")
def forgot_password_code_validation_endpoint(
    request: ValidateCode, db: Session = Depends(get_db)
):
    print(f"Received recovery code validation request for: {request.usernameOrEmail}")
    success = validate_reset_code(
        db=db, username_or_email=request.usernameOrEmail, code=request.code
    )

    if not success:
        raise HTTPException(status_code=400, detail="Invalid code")

    return {"message": "Code is valid"}


@router.post("/reset-password")
def reset_password_endpoint(
    request: ChangePasswordRequest, db: Session = Depends(get_db)
):
    print(f"Received password reset request for: {request.usernameOrEmail}")
    success = change_password(
        db=db,
        username_or_email=request.usernameOrEmail,
        code=request.code,
        new_password=request.new_password,
    )

    if not success:
        raise HTTPException(status_code=400, detail="Invalid code")

    return {"message": "Code is valid"}
