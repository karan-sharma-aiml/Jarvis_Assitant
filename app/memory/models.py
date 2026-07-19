"""
JARVIS Memory Models

Defines the data models used throughout the memory system.

This module is intentionally storage-independent.

It contains only data structures shared by all memory backends.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class MemoryType(StrEnum):
    """
    Supported memory categories.
    """

    CONVERSATION = "conversation"
    WORKING = "working"
    PREFERENCE = "preference"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"


class MemoryImportance(StrEnum):
    """
    Importance level of a memory.
    """

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(slots=True)
class MemoryMetadata:
    """
    Additional metadata attached to a memory.
    """

    source: str = "user"

    tags: list[str] = field(default_factory=list)

    confidence: float = 1.0

    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class MemoryRecord:
    """
    Represents one stored memory.
    """

    key: str

    value: str

    memory_type: MemoryType

    importance: MemoryImportance = MemoryImportance.NORMAL

    metadata: MemoryMetadata = field(default_factory=MemoryMetadata)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )


@dataclass(slots=True)
class MemorySearchResult:
    """
    Result returned from a memory search.
    """

    record: MemoryRecord

    score: float