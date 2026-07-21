"""
Intent models for the JARVIS AI Assistant.

This module defines the shared data models used by the
intent detection pipeline.

Business logic should NOT be placed in this file.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class IntentSource(str, Enum):
    """
    Origin of the detected intent.
    """

    TEXT = "text"
    VOICE = "voice"
    API = "api"
    CLI = "cli"
    GUI = "gui"
    AUTOMATION = "automation"
    UNKNOWN = "unknown"


class IntentName(str, Enum):
    """
    Supported intent names.
    """

    OPEN_APPLICATION = "open_application"
    CLOSE_APPLICATION = "close_application"

    CREATE_FILE = "create_file"
    CREATE_FOLDER = "create_folder"
    DELETE_PATH = "delete_path"
    COPY_PATH = "copy_path"
    MOVE_PATH = "move_path"
    RENAME_PATH = "rename_path"

    SET_VOLUME = "set_volume"
    INCREASE_VOLUME = "increase_volume"
    DECREASE_VOLUME = "decrease_volume"
    MUTE_VOLUME = "mute_volume"
    UNMUTE_VOLUME = "unmute_volume"

    SET_BRIGHTNESS = "set_brightness"
    INCREASE_BRIGHTNESS = "increase_brightness"
    DECREASE_BRIGHTNESS = "decrease_brightness"

    COPY_TEXT = "copy_text"
    PASTE_TEXT = "paste_text"
    CLEAR_CLIPBOARD = "clear_clipboard"

    TAKE_SCREENSHOT = "take_screenshot"

    SHUTDOWN = "shutdown"
    RESTART = "restart"
    LOCK = "lock"
    SLEEP = "sleep"
    HIBERNATE = "hibernate"
    LOGOFF = "logoff"

    CHAT = "chat"

    UNKNOWN = "unknown"


@dataclass(slots=True)
class Intent:
    """
    Represents one detected user intent.
    """

    name: IntentName

    confidence: float = 1.0

    source: IntentSource = IntentSource.TEXT

    entities: dict[str, object] = field(default_factory=dict)

    original_text: str = ""

    metadata: dict[str, object] = field(default_factory=dict)

    @property
    def is_unknown(self) -> bool:
        """
        Returns True if the detector could not determine
        the user's intent.
        """
        return self.name == IntentName.UNKNOWN

    @property
    def is_confident(self) -> bool:
        """
        Returns True if confidence is high enough.
        """
        return self.confidence >= 0.80

    def has_entity(self, key: str) -> bool:
        """
        Check whether an entity exists.
        """
        return key in self.entities

    def get_entity(
        self,
        key: str,
        default: object | None = None,
    ) -> object | None:
        """
        Return one entity.
        """
        return self.entities.get(key, default)

    def add_entity(
        self,
        key: str,
        value: object,
    ) -> None:
        """
        Add or update an entity.
        """
        self.entities[key] = value

    def remove_entity(
        self,
        key: str,
    ) -> None:
        """
        Remove an entity if present.
        """
        self.entities.pop(key, None)

    def clear_entities(self) -> None:
        """
        Remove all extracted entities.
        """
        self.entities.clear()

    def to_dict(self) -> dict[str, object]:
        """
        Convert the object into a serializable dictionary.
        """
        return {
            "intent": self.name.value,
            "confidence": self.confidence,
            "source": self.source.value,
            "entities": self.entities,
            "original_text": self.original_text,
            "metadata": self.metadata,
        }

    @classmethod
    def unknown(
        cls,
        text: str,
    ) -> "Intent":
        """
        Create an unknown intent.
        """
        return cls(
            name=IntentName.UNKNOWN,
            confidence=0.0,
            source=IntentSource.UNKNOWN,
            original_text=text,
        )

    def __str__(self) -> str:
        return (
            "Intent("
            f"name={self.name.value}, "
            f"confidence={self.confidence:.2f}, "
            f"source={self.source.value}, "
            f"entities={self.entities})"
        )

    def __repr__(self) -> str:
        return self.__str__()