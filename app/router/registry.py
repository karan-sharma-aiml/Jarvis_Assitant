"""
Tool Registry

Maps IntentName -> ToolRoute.

Responsibilities
----------------
- Store routing table.
- Return ToolRoute for an intent.
- Validate supported intents.
- Health checks.

Contains NO execution logic.
"""

from __future__ import annotations

import logging

from app.intent.models import IntentName
from app.router.models import ToolRoute

logger = logging.getLogger(__name__)


class ToolRegistry:
    """
    Central registry for all tool routes.
    """

    _ROUTES: dict[IntentName, ToolRoute] = {

        # -------------------------------------------------
        # Applications
        # -------------------------------------------------

        IntentName.OPEN_APPLICATION: ToolRoute(
            manager="ApplicationManager",
            method="open",
            required_entities=("application",),
            priority=1,
        ),

        IntentName.CLOSE_APPLICATION: ToolRoute(
            manager="ApplicationManager",
            method="close",
            required_entities=("application",),
            priority=1,
        ),

        # -------------------------------------------------
        # Files
        # -------------------------------------------------

        IntentName.CREATE_FILE: ToolRoute(
            manager="FileManager",
            method="create_file",
            required_entities=("path",),
        ),

        IntentName.CREATE_FOLDER: ToolRoute(
            manager="FileManager",
            method="create_folder",
            required_entities=("path",),
        ),

        IntentName.DELETE_PATH: ToolRoute(
            manager="FileManager",
            method="delete",
            required_entities=("path",),
            requires_confirmation=True,
        ),

        IntentName.COPY_PATH: ToolRoute(
            manager="FileManager",
            method="copy",
            required_entities=("source", "destination"),
        ),

        IntentName.MOVE_PATH: ToolRoute(
            manager="FileManager",
            method="move",
            required_entities=("source", "destination"),
        ),

        IntentName.RENAME_PATH: ToolRoute(
            manager="FileManager",
            method="rename",
            required_entities=("source", "destination"),
        ),

        # -------------------------------------------------
        # Volume
        # -------------------------------------------------

        IntentName.SET_VOLUME: ToolRoute(
            manager="VolumeManager",
            method="set_volume",
            required_entities=("value",),
        ),

        IntentName.INCREASE_VOLUME: ToolRoute(
            manager="VolumeManager",
            method="increase_volume",
        ),

        IntentName.DECREASE_VOLUME: ToolRoute(
            manager="VolumeManager",
            method="decrease_volume",
        ),

        IntentName.MUTE_VOLUME: ToolRoute(
            manager="VolumeManager",
            method="mute",
        ),

        IntentName.UNMUTE_VOLUME: ToolRoute(
            manager="VolumeManager",
            method="unmute",
        ),

        # -------------------------------------------------
        # Brightness
        # -------------------------------------------------

        IntentName.SET_BRIGHTNESS: ToolRoute(
            manager="BrightnessManager",
            method="set_brightness",
            required_entities=("value",),
        ),

        IntentName.INCREASE_BRIGHTNESS: ToolRoute(
            manager="BrightnessManager",
            method="increase_brightness",
        ),

        IntentName.DECREASE_BRIGHTNESS: ToolRoute(
            manager="BrightnessManager",
            method="decrease_brightness",
        ),

        # -------------------------------------------------
        # Clipboard
        # -------------------------------------------------

        IntentName.COPY_TEXT: ToolRoute(
            manager="ClipboardManager",
            method="copy",
            required_entities=("text",),
        ),

        IntentName.PASTE_TEXT: ToolRoute(
            manager="ClipboardManager",
            method="paste",
        ),

        IntentName.CLEAR_CLIPBOARD: ToolRoute(
            manager="ClipboardManager",
            method="clear",
        ),

        # -------------------------------------------------
        # Screenshot
        # -------------------------------------------------

        IntentName.TAKE_SCREENSHOT: ToolRoute(
            manager="ScreenshotManager",
            method="take_screenshot",
        ),

        # -------------------------------------------------
        # Power
        # -------------------------------------------------

        IntentName.SHUTDOWN: ToolRoute(
            manager="PowerManager",
            method="shutdown",
            requires_confirmation=True,
        ),

        IntentName.RESTART: ToolRoute(
            manager="PowerManager",
            method="restart",
            requires_confirmation=True,
        ),

        IntentName.SLEEP: ToolRoute(
            manager="PowerManager",
            method="sleep",
        ),

        IntentName.HIBERNATE: ToolRoute(
            manager="PowerManager",
            method="hibernate",
        ),

        IntentName.LOCK: ToolRoute(
            manager="PowerManager",
            method="lock",
        ),

        IntentName.LOGOFF: ToolRoute(
            manager="PowerManager",
            method="logoff",
            requires_confirmation=True,
        ),
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

        logger.debug("Unsupported route intent value %r; returning None", intent)
        return None

    @classmethod
    def get(cls, intent: IntentName | str | None) -> ToolRoute | None:
        """Return the ToolRoute for an intent."""
        normalized = cls._coerce_intent(intent)
        if normalized is None:
            return None
        return cls._ROUTES.get(normalized)

    @classmethod
    def exists(cls, intent: IntentName | str | None) -> bool:
        """Check whether a route exists."""
        normalized = cls._coerce_intent(intent)
        return normalized is not None and normalized in cls._ROUTES

    @classmethod
    def all(cls) -> dict[IntentName, ToolRoute]:
        """Return all registered routes."""
        return dict(cls._ROUTES)

    @classmethod
    def count(cls) -> int:
        """
        Return number of registered routes.
        """
        return len(cls._ROUTES)

    @classmethod
    def health_check(cls) -> bool:
        """
        Registry health.
        """
        return cls.count() > 0

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(routes={self.count()})"
        )