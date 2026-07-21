"""
Intent Patterns

Maps regular expression patterns to supported intents.

Responsibilities
----------------
- Store regex patterns.
- Keep aliases in one place.
- Support future multilingual extensions.

This module contains NO detection logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from re import Pattern
import re

from app.intent.models import IntentName


@dataclass(slots=True, frozen=True)
class IntentPattern:
    """
    One intent pattern.
    """

    intent: IntentName

    regex: Pattern[str]

    description: str


class IntentPatterns:
    """
    Registry of all supported regex patterns.
    """

    _PATTERNS: tuple[IntentPattern, ...] = (

        # -------------------------------------------------
        # Applications
        # -------------------------------------------------

        IntentPattern(
            IntentName.OPEN_APPLICATION,
            re.compile(
                r"^(open|launch|start|run)\s+(?P<application>.+)$",
                re.IGNORECASE,
            ),
            "Open an application.",
        ),

        IntentPattern(
            IntentName.CLOSE_APPLICATION,
            re.compile(
                r"^(close|stop|exit|quit)\s+(?P<application>.+)$",
                re.IGNORECASE,
            ),
            "Close an application.",
        ),

        # -------------------------------------------------
        # Volume
        # -------------------------------------------------

        IntentPattern(
            IntentName.SET_VOLUME,
            re.compile(
                r"^(set volume to)\s+(?P<value>\d+)",
                re.IGNORECASE,
            ),
            "Set system volume.",
        ),

        IntentPattern(
            IntentName.INCREASE_VOLUME,
            re.compile(
                r"^(increase volume|volume up)",
                re.IGNORECASE,
            ),
            "Increase volume.",
        ),

        IntentPattern(
            IntentName.DECREASE_VOLUME,
            re.compile(
                r"^(decrease volume|volume down)",
                re.IGNORECASE,
            ),
            "Decrease volume.",
        ),

        # -------------------------------------------------
        # Brightness
        # -------------------------------------------------

        IntentPattern(
            IntentName.SET_BRIGHTNESS,
            re.compile(
                r"^(set brightness to)\s+(?P<value>\d+)",
                re.IGNORECASE,
            ),
            "Set brightness.",
        ),

        # -------------------------------------------------
        # Screenshot
        # -------------------------------------------------

        IntentPattern(
            IntentName.TAKE_SCREENSHOT,
            re.compile(
                r"^(take screenshot|capture screen)$",
                re.IGNORECASE,
            ),
            "Take screenshot.",
        ),

        # -------------------------------------------------
        # Clipboard
        # -------------------------------------------------

        IntentPattern(
            IntentName.COPY_TEXT,
            re.compile(
                r"^copy\s+(?P<text>.+)$",
                re.IGNORECASE,
            ),
            "Copy text.",
        ),

        IntentPattern(
            IntentName.PASTE_TEXT,
            re.compile(
                r"^paste$",
                re.IGNORECASE,
            ),
            "Paste text.",
        ),

        # -------------------------------------------------
        # Power
        # -------------------------------------------------

        IntentPattern(
            IntentName.SHUTDOWN,
            re.compile(
                r"^shutdown$",
                re.IGNORECASE,
            ),
            "Shutdown computer.",
        ),

        IntentPattern(
            IntentName.RESTART,
            re.compile(
                r"^restart$",
                re.IGNORECASE,
            ),
            "Restart computer.",
        ),
    )

    @classmethod
    def all(cls) -> tuple[IntentPattern, ...]:
        """
        Return every registered pattern.
        """
        return cls._PATTERNS

    @classmethod
    def count(cls) -> int:
        """
        Number of registered patterns.
        """
        return len(cls._PATTERNS)

    @classmethod
    def health_check(cls) -> bool:
        """
        Registry health.
        """
        return cls.count() > 0

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(patterns={self.count()})"
        )