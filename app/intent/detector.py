"""
Intent Detector

Converts natural language into a structured Intent object.

Responsibilities
----------------
- Normalize user input.
- Match against registered regex patterns.
- Extract entities.
- Produce an Intent object.
- Return UNKNOWN intent if nothing matches.

This module contains NO execution logic.
"""

from __future__ import annotations

import logging

from app.intent.models import (
    Intent,
    IntentName,
    IntentSource,
)
from app.intent.patterns import IntentPatterns

logger = logging.getLogger(__name__)


class IntentDetector:
    """
    Rule-based intent detector.

    Future:
    -------
    Low-confidence or unknown intents can be
    forwarded to an LLM without changing this API.
    """

    __slots__ = ("_patterns",)

    def __init__(self) -> None:
        self._patterns = IntentPatterns.all()

    @staticmethod
    def normalize(text: str | None) -> str:
        """Normalize incoming user text."""
        if not isinstance(text, str):
            return ""
        return " ".join(text.strip().split())

    @staticmethod
    def _coerce_source(source: IntentSource | str | None) -> IntentSource:
        """Normalize the source value to an IntentSource enum."""
        if isinstance(source, IntentSource):
            return source

        if isinstance(source, str):
            normalized = source.strip().lower()
            for candidate in IntentSource:
                if candidate.value == normalized:
                    return candidate

        logger.debug("Unsupported intent source %r; using TEXT", source)
        return IntentSource.TEXT

    def detect(
        self,
        text: str | None,
        *,
        source: IntentSource | str | None = IntentSource.TEXT,
    ) -> Intent:
        """Detect one intent from text."""
        normalized_text = self.normalize(text)
        resolved_source = self._coerce_source(source)

        if not normalized_text:
            logger.debug("Empty intent text received; returning unknown intent")
            return Intent.unknown(text or "")

        for pattern in self._patterns:
            match = pattern.regex.fullmatch(normalized_text)
            if not match:
                continue

            entities: dict[str, object] = {}
            for key, value in match.groupdict().items():
                if value is None:
                    continue

                cleaned_value = value.strip()
                if cleaned_value.isdigit():
                    entities[key] = int(cleaned_value)
                else:
                    entities[key] = cleaned_value

            logger.debug("Matched intent %s from text %r", pattern.intent.value, normalized_text)
            return Intent(
                name=pattern.intent,
                confidence=1.0,
                source=resolved_source,
                entities=entities,
                original_text=text or "",
            )

        logger.debug("No intent pattern matched for text %r", normalized_text)
        return Intent(
            name=IntentName.UNKNOWN,
            confidence=0.0,
            source=resolved_source,
            original_text=text or "",
        )

    def health_check(self) -> bool:
        """Return True when the detector has registered patterns."""
        return bool(self._patterns)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(patterns={len(self._patterns)})"
        )