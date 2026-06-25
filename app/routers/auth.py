from fastapi import APIRouter, Request
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.oauth import oauth
from starlette.responses import RedirectResponse
from app.core.config import GOOGLE_REDIRECT_URI
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
    get_user_by_email,
)
from app.core.security import create_access_token
from app.schemas.user import LoginRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
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
    success = await forgot_password(db=db, username_or_email=request.usernameOrEmail)

    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Verification code sent"}


@router.post("/validate-recovery-code")
def forgot_password_code_validation_endpoint(
    request: ValidateCode, db: Session = Depends(get_db)
):
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
    success = change_password(
        db=db,
        username_or_email=request.usernameOrEmail,
        code=request.code,
        new_password=request.new_password,
    )

    if not success:
        raise HTTPException(status_code=400, detail="Invalid code")

    return {"message": "Code is valid"}


@router.get("/google/callback")
async def google_callback(request: Request):

    token = await oauth.google.authorize_access_token(request)

    user_info = token["userinfo"]

    email = user_info["email"]
    first_name = user_info["given_name"]
    last_name = user_info["family_name"]
    external_id = user_info["sub"]

    # buscar usuario en la BD
    db = next(get_db())
    user = get_user_by_email(db, email)
    if not user:
        # si no existe -> crearlo
        user = create_user(
            db=db,
            username=email.split("@")[0],
            email=email,
            password=external_id,  # usar el external_id como contraseña temporal
            first_name=first_name,
            last_name=last_name,
        )
    else:
        # si existe -> actualizar datos
        user.first_name = first_name
        user.last_name = last_name
        user.external_id = external_id
        db.commit()
        db.refresh(user)
    jwt_token = create_access_token({"sub": str(user.id), "roles": user.roles})

    return RedirectResponse(
        f"{GOOGLE_REDIRECT_URI}?token={jwt_token}&user_id={user.id}&username={user.username}&email={user.email}&first_name={user.first_name}&last_name={user.last_name}&id={user.id}&roles={','.join(str(role) for role in user.roles)}"
    )


@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)
