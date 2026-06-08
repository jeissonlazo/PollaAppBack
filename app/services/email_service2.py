from pydoc import html

from fastapi_mail import FastMail
from fastapi_mail import MessageSchema

from app.core.mail import conf


async def send_verification_email(email: str, code: str):

    message = MessageSchema(
        subject="Confirm your account",
        recipients=[email],
        body=f"""
        Welcome to Polla Mundial!

        Your verification code is:

        {code}

        This code expires in 15 minutes.
        """,
        subtype="plain",
    )

    fm = FastMail(conf)

    await fm.send_message(message)
