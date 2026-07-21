"""
JARVIS Clipboard Manager

Responsibilities
----------------
- Read clipboard
- Write clipboard
- Clear clipboard
- Check clipboard

Contains NO business logic.
"""

from __future__ import annotations

import logging

import pyperclip

from app.system.models import SystemResponse, SystemStatus

logger = logging.getLogger(__name__)


class ClipboardManager:
    """Windows clipboard controller."""

    def copy(self, text: str) -> SystemResponse:
        """Copy text to clipboard."""
        try:
            pyperclip.copy(text)
        except (OSError, ValueError, pyperclip.PyperclipException) as exc:
            logger.exception("Unable to update clipboard: %s", exc)
            return SystemResponse(SystemStatus.FAILED, "Unable to update clipboard.")

        logger.info("Clipboard updated.")
        return SystemResponse(SystemStatus.SUCCESS, "Clipboard updated.")

    def paste(self) -> str:
        """Read clipboard."""
        try:
            return pyperclip.paste()
        except (OSError, ValueError, pyperclip.PyperclipException) as exc:
            logger.warning("Unable to read clipboard: %s", exc)
            return ""

    def clear(self) -> SystemResponse:
        """Clear clipboard."""
        try:
            pyperclip.copy("")
        except (OSError, ValueError, pyperclip.PyperclipException) as exc:
            logger.exception("Unable to clear clipboard: %s", exc)
            return SystemResponse(SystemStatus.FAILED, "Unable to clear clipboard.")

        logger.info("Clipboard cleared.")
        return SystemResponse(SystemStatus.SUCCESS, "Clipboard cleared.")

    def has_text(self) -> bool:
        """Check whether clipboard contains text."""
        return bool(self.paste().strip())

    def health_check(self) -> bool:
        """Verify Clipboard Manager."""
        try:
            current = self.paste()
            pyperclip.copy(current)
            return True
        except Exception as exc:  # noqa: BLE001
            logger.exception("Clipboard Manager health check failed: %s", exc)
            return False