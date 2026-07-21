"""
Intent Detection Package

Provides:

- Intent models
- Intent detector
- Intent registry
- Pattern matching
"""

from app.intent.detector import IntentDetector
from app.intent.models import (
    Intent,
    IntentName,
    IntentSource,
)

__all__ = [
    "Intent",
    "IntentName",
    "IntentSource",
    "IntentDetector",
]