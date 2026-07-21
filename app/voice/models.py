"""Voice models for the speech subsystem."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TranscriptionResult:
    """Result returned by SpeechToText."""

    text: str = ""
    language: str = ""
    duration: float = 0.0