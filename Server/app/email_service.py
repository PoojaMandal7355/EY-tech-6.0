"""Email service for sending password reset emails via Gmail."""

import asyncio
import logging
import os
import smtplib
from concurrent.futures import ThreadPoolExecutor
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .config import settings


executor = ThreadPoolExecutor(max_workers=5)
logger = logging.getLogger(__name__)


class EmailService:
    """Gmail SMTP email service."""

    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = settings.GMAIL_EMAIL
        self.sender_password = settings.GMAIL_APP_PASSWORD
        self.sender_name = "PharmaPilot"
        logger.info(
          "EmailService loaded",
          extra={"has_email": bool(self.sender_email), "has_password": bool(self.sender_password)},
        )

    def is_configured(self) -> bool:
        """Check if Gmail is properly configured."""
        return bool(self.sender_email and self.sender_password)

    def send_password_reset_email(self, recipient_email: str, reset_token: str, user_name: str = "User") -> bool:
        """Send password reset email."""
        if not self.is_configured():
            logger.warning("EmailService not configured: missing GMAIL_EMAIL or GMAIL_APP_PASSWORD")
            return False

        try:
            frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
            reset_link = f"{frontend_url}/reset-password?token={reset_token}"

            message = MIMEMultipart("alternative")
            message["Subject"] = "Reset Your PharmaPilot Password"
            message["From"] = f"{self.sender_name} <{self.sender_email}>"
            message["To"] = recipient_email

            html_content = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  </head>
  <body style=\"font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px; margin: 0;\">
    <div style=\"max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);\">
      <h2 style=\"color: #333; text-align: center; margin-bottom: 20px;\">🔐 Reset Your Password</h2>
      <p style=\"color: #666; font-size: 14px;\">Hi {user_name},</p>
      <p style=\"color: #666; font-size: 14px; line-height: 1.6;\">
        We received a request to reset your PharmaPilot password. Click the button below to create a new password.
      </p>
      <div style=\"text-align: center; margin: 30px 0;\">
        <a href=\"{reset_link}\" style=\"background-color: #009688; color: white; padding: 15px 40px; text-decoration: none; border-radius: 4px; font-weight: bold; display: inline-block; font-size: 16px;\">
          Reset Password
        </a>
      </div>
      <p style=\"color: #666; font-size: 13px; line-height: 1.6;\">
        Or copy and paste this link in your browser:
      </p>
      <p style=\"background-color: #f0f0f0; padding: 12px; border-radius: 4px; word-wrap: break-word; overflow-wrap: break-word; font-size: 12px; color: #333;\">
        {reset_link}
      </p>
      <div style=\"background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 12px; margin: 20px 0; border-radius: 4px;\">
        <p style=\"color: #856404; font-size: 12px; margin: 0; line-height: 1.5;\">
          <strong>⏰ Important:</strong> This link expires in 30 minutes. If you didn't request this, please ignore this email.
        </p>
      </div>
      <hr style=\"border: none; border-top: 1px solid #ddd; margin: 20px 0;\">
      <p style=\"color: #999; font-size: 12px; text-align: center; margin: 0;\">
        PharmaPilot - AI-Powered Pharmaceutical Research Platform<br>
        © 2025 EY Technathon 6.0
      </p>
    </div>
  </body>
</html>
"""

            text_content = f"""
Reset Your PharmaPilot Password

Hi {user_name},

We received a request to reset your PharmaPilot password.

Click this link to reset your password:
{reset_link}

This link expires in 30 minutes.

If you didn't request this, please ignore this email.

PharmaPilot - AI-Powered Pharmaceutical Research Platform
"""

            message.attach(MIMEText(text_content, "plain"))
            message.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)

            logger.info(
                "Password reset email sent",
                extra={"recipient": recipient_email, "reset_link": reset_link},
            )
            return True
        except smtplib.SMTPAuthenticationError as exc:
            logger.exception("SMTP authentication failed for password reset email", exc_info=exc)
            return False
        except smtplib.SMTPException as exc:
            logger.exception("SMTP error sending password reset email", exc_info=exc)
            return False
        except Exception as exc:
            logger.exception("Unexpected error sending password reset email", exc_info=exc)
            return False

    async def send_password_reset_email_async(self, recipient_email: str, reset_token: str, user_name: str = "User") -> bool:
        """Async wrapper for send_password_reset_email."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            executor,
            self.send_password_reset_email,
            recipient_email,
            reset_token,
            user_name,
        )

    def send_verification_email(self, recipient_email: str, verification_token: str, user_name: str = "User") -> bool:
        """Send email verification email (not used yet)."""
        if not self.is_configured():
            return False

        try:
            verify_link = f"http://localhost:5173/verify-email?token={verification_token}"

            message = MIMEMultipart("alternative")
            message["Subject"] = "Verify Your PharmaPilot Email"
            message["From"] = f"{self.sender_name} <{self.sender_email}>"
            message["To"] = recipient_email

            html_content = f"""
<html>
  <body style=\"font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;\">
    <div style=\"max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px;\">
      <h2 style=\"color: #333; text-align: center;\">📧 Verify Your Email</h2>
      <p style=\"color: #666;\">Hi {user_name},</p>
      <p style=\"color: #666;\">Please verify your email address by clicking the button below:</p>
      <div style=\"text-align: center; margin: 30px 0;\">
        <a href=\"{verify_link}\" style=\"background-color: #009688; color: white; padding: 12px 30px; text-decoration: none; border-radius: 4px;\">
          Verify Email
        </a>
      </div>
    </div>
  </body>
</html>
"""

            message.attach(MIMEText(f"Verify your email: {verify_link}", "plain"))
            message.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)

            return True
        except Exception:
            return False


email_service = EmailService()
