"""
JARVIS Email Tool

Provides email sending functionality.

Current Provider:
- SMTP

Responsibilities:
- Validate email addresses
- Validate message
- Send email securely

Future Providers:
- Gmail API
- Outlook API
- SendGrid
- Resend
"""

from __future__ import annotations

import logging
import re
import smtplib
import ssl
from email.message import EmailMessage
from typing import Any

from app.config.settings import settings
from app.tools.base import BaseTool
from app.tools.exceptions import (
    ToolExecutionError,
    ToolValidationError,
)
from app.tools.models import ToolCategory

logger = logging.getLogger(__name__)


_EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


class EmailTool(BaseTool):
    """Email sending tool."""

    @property
    def name(self) -> str:
        return "email"

    @property
    def description(self) -> str:
        return "Send an email."

    @property
    def category(self) -> ToolCategory:
        return ToolCategory.COMMUNICATION

    def availability(self) -> tuple[bool, str | None]:
        smtp_host = (settings.SMTP_HOST or "").strip()
        smtp_username = (settings.SMTP_USERNAME or "").strip()
        smtp_password = (
            settings.SMTP_PASSWORD.get_secret_value()
            if hasattr(settings.SMTP_PASSWORD, "get_secret_value")
            else settings.SMTP_PASSWORD
        )
        smtp_password = (smtp_password or "").strip()

        if not smtp_host or not smtp_username or not smtp_password:
            return False, "SMTP configuration is incomplete"

        return True, None

    def validate(self, **kwargs: Any) -> None:
        recipient = kwargs.get("recipient")
        subject = kwargs.get("subject")
        body = kwargs.get("body")

        if not isinstance(recipient, str):
            raise ToolValidationError("Recipient must be a string.")

        recipient = recipient.strip()
        if not recipient:
            raise ToolValidationError("Recipient cannot be empty.")
        if "\n" in recipient or "\r" in recipient:
            raise ToolValidationError("Recipient contains invalid characters.")
        if not _EMAIL_PATTERN.fullmatch(recipient):
            raise ToolValidationError("Invalid email address.")

        if not isinstance(subject, str):
            raise ToolValidationError("Subject must be a string.")

        subject = subject.strip()
        if not subject:
            raise ToolValidationError("Subject cannot be empty.")
        if "\n" in subject or "\r" in subject:
            raise ToolValidationError("Subject contains invalid characters.")

        if not isinstance(body, str):
            raise ToolValidationError("Body must be a string.")

        if not body.strip():
            raise ToolValidationError("Body cannot be empty.")

    def execute(self, **kwargs: Any) -> str:
        self.validate(**kwargs)

        recipient = kwargs["recipient"]
        subject = kwargs["subject"]
        body = kwargs["body"]

        message = EmailMessage()
        message["From"] = settings.SMTP_USERNAME
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        smtp_host = (settings.SMTP_HOST or "").strip()
        smtp_port = int(settings.SMTP_PORT or 587)
        smtp_username = (settings.SMTP_USERNAME or "").strip()
        smtp_password = (
            settings.SMTP_PASSWORD.get_secret_value()
            if hasattr(settings.SMTP_PASSWORD, "get_secret_value")
            else settings.SMTP_PASSWORD
        )
        smtp_password = (smtp_password or "").strip()

        if not smtp_host or not smtp_username or not smtp_password:
            raise ToolExecutionError("SMTP configuration is incomplete.")

        try:
            if smtp_port == 465:
                with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30) as smtp:
                    smtp.login(smtp_username, smtp_password)
                    smtp.send_message(message)
            else:
                with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as smtp:
                    smtp.starttls(context=ssl.create_default_context())
                    smtp.login(smtp_username, smtp_password)
                    smtp.send_message(message)

            return "Email sent successfully."

        except smtplib.SMTPAuthenticationError as error:
            logger.warning("SMTP authentication failed for email send", exc_info=error)
            raise ToolExecutionError("SMTP authentication failed.") from error
        except (
            smtplib.SMTPConnectError,
            smtplib.SMTPHeloError,
            smtplib.SMTPNotSupportedError,
            smtplib.SMTPRecipientsRefused,
            smtplib.SMTPException,
        ) as error:
            logger.warning("SMTP send failed", exc_info=error)
            raise ToolExecutionError(f"Failed to send email: {error}") from error
        except OSError as error:
            logger.warning("SMTP connection failed", exc_info=error)
            raise ToolExecutionError(f"Failed to send email: {error}") from error