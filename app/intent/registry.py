"""
Intent Registry

Central registry for all supported intents.

Responsibilities
----------------
- Store all supported intents.
- Provide descriptions.
- Validate supported intents.
- Keep a single source of truth for the planner,
  router and executor.

This module contains NO intent detection logic.
"""

from __future__ import annotations

import logging

from app.intent.models import IntentName

logger = logging.getLogger(__name__)


class IntentRegistry:
    """
    Registry of all supported intents.
    """

    _DESCRIPTIONS: dict[IntentName, str] = {
        IntentName.OPEN_APPLICATION: "Open an application.",
        IntentName.CLOSE_APPLICATION: "Close an application.",

        IntentName.CREATE_FILE: "Create a file.",
        IntentName.CREATE_FOLDER: "Create a folder.",
        IntentName.DELETE_PATH: "Delete a file or folder.",
        IntentName.COPY_PATH: "Copy a file or folder.",
        IntentName.MOVE_PATH: "Move a file or folder.",
        IntentName.RENAME_PATH: "Rename a file or folder.",

        IntentName.SET_VOLUME: "Set system volume.",
        IntentName.INCREASE_VOLUME: "Increase system volume.",
        IntentName.DECREASE_VOLUME: "Decrease system volume.",
        IntentName.MUTE_VOLUME: "Mute system volume.",
        IntentName.UNMUTE_VOLUME: "Unmute system volume.",

        IntentName.SET_BRIGHTNESS: "Set screen brightness.",
        IntentName.INCREASE_BRIGHTNESS: "Increase brightness.",
        IntentName.DECREASE_BRIGHTNESS: "Decrease brightness.",

        IntentName.COPY_TEXT: "Copy text.",
        IntentName.PASTE_TEXT: "Paste clipboard text.",
        IntentName.CLEAR_CLIPBOARD: "Clear clipboard.",

        IntentName.TAKE_SCREENSHOT: "Capture screen.",

        IntentName.SHUTDOWN: "Shutdown computer.",
        IntentName.RESTART: "Restart computer.",
        IntentName.SLEEP: "Sleep computer.",
        IntentName.HIBERNATE: "Hibernate computer.",
        IntentName.LOCK: "Lock computer.",
        IntentName.LOGOFF: "Logoff user.",

        IntentName.CHAT: "General conversation.",

        IntentName.UNKNOWN: "Unknown intent.",
    }

    @staticmethod
    def _coerce_intent(intent: IntentName | str | None) -> IntentName | None:
        """Normalize an intent input to an IntentName enum when possible."""
        if isinstance(intent, IntentName):
            return intent

        if isinstance(intent, str):
            normalized = intent.strip().lower()
            for candidate in IntentName:
                if candidate.value == normalized:
                    return candidate

        logger.debug("Unsupported intent value %r; returning None", intent)
        return None

    @classmethod
    def exists(
        cls,
        intent: IntentName | str | None,
    ) -> bool:
        """Return True if intent is registered."""
        normalized = cls._coerce_intent(intent)
        return normalized is not None and normalized in cls._DESCRIPTIONS

    @classmethod
    def description(
        cls,
        intent: IntentName | str | None,
    ) -> str:
        """Return intent description."""
        normalized = cls._coerce_intent(intent)
        if normalized is None:
            return "Unknown intent."
        return cls._DESCRIPTIONS.get(normalized, "Unknown intent.")

    @classmethod
    def all(
        cls,
    ) -> tuple[IntentName, ...]:
        """
        Return every registered intent.
        """
        return tuple(cls._DESCRIPTIONS.keys())

    @classmethod
    def count(
        cls,
    ) -> int:
        """
        Number of supported intents.
        """
        return len(cls._DESCRIPTIONS)

    @classmethod
    def health_check(
        cls,
    ) -> bool:
        """
        Registry health.
        """
        return cls.count() > 0

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(intents={self.count()})"
        )