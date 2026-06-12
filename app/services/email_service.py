import os
import resend
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")


def send_verification_email(email: str, code: str):
    resend.Emails.send(
        {
            "from": "noreply@pollapp.xyz",
            "to": email,
            "subject": "Verifica tu correo",
            "html": f"""
            <h2>Bienvenido a pollapp 👋</h2>
            <p>este es tu codigo de verificacion: {code}</p>
            <a"
              style="background:#4f46e5;color:white;padding:12px 24px;
                      border-radius:6px;text-decoration:none;display:inline-block">
              {code}
            </a>
            <p style="color:#888;font-size:12px;margin-top:16px">
              Este enlace expira en 1 hora.
            </p>
        """,
        }
    )


def send_reset_password_email(email: str, code: str):
    resend.Emails.send(
        {
            "from": "noreply@pollapp.xyz",
            "to": email,
            "subject": "Password recovery",
            "html": f"""
        <h2>Password Recovery</h2>
        <p>Your verification code is:</p>
        <h1>{code}</h1>
        <p>This code expires in 15 minutes.</p>
        """,
        }
    )
