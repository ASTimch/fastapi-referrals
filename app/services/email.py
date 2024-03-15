import smtplib
from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_referral_code_template(
    email_to: EmailStr,
    referral_code: str,
):
    email = EmailMessage()

    email["Subject"] = "Реферальный код"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Текущий реферальный код</h1>
            {referral_code}
        """,
        subtype="html",
    )
    return email


def send_referral_code_email(email_to: EmailStr, referral_code: str):
    msg_content = create_referral_code_template(email_to, referral_code)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
