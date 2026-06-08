from sqlalchemy.orm import Session
from datetime import datetime
from datetime import timedelta
from app.models.user import User
from app.core.email_verification import generate_verification_code
from app.core.security import hash_password, verify_password
from app.services.email_service import send_verification_email
from sqlalchemy import or_
from fastapi import HTTPException
import traceback

async def create_user(
    db: Session,
    username: str,
    email: str,
    password: str,
    first_name: str | None = None,
    last_name: str | None = None,
):

    existing_user = (
        db.query(User)
        .filter(or_(User.username == username, User.email == email))
        .first()
    )

    if existing_user:
        if existing_user.username == username:
            raise HTTPException(status_code=409, detail="Username already exists")

        if existing_user.email == email:
            raise HTTPException(status_code=409, detail="Email already exists")

    verification_code = generate_verification_code()

    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
        email_verified=False,
        first_name=first_name,
        last_name=last_name,
        verification_code=verification_code,
        verification_expires=datetime.utcnow() + timedelta(minutes=15),
    )

    try:
        send_verification_email(user.email, verification_code)
    except Exception as e:
        traceback.print_exc()

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
def authenticate_user(db: Session, usernameOrEmail: str, password: str):

    user = (
        db.query(User)
        .filter((User.username == usernameOrEmail) | (User.email == usernameOrEmail))
        .first()
    )

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


def verify_email(db, email, code):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return False

    if user.email_verified:
        return True

    if user.verification_code != code:
        return False

    if user.verification_expires < datetime.utcnow():
        return False

    user.email_verified = True

    user.verification_code = None
    user.verification_expires = None

    db.commit()

    return True
