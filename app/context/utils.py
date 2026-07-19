"""
JARVIS Context Utilities

Utility functions for the Context Engine.

Responsibilities
----------------
- Normalize context values.
- Merge context safely.
- Validate context data.

Contains NO business logic.
Contains NO memory retrieval.
Contains NO RAG retrieval.
"""

from __future__ import annotations

from typing import Any


def normalize_text(text: str | None) -> str:
    """
    Normalize text by stripping whitespace.

    Returns an empty string for None.
    """

    if text is None:
        return ""

    return " ".join(text.strip().split())


def normalize_list(values: list[str] | None) -> list[str]:
    """
    Normalize a list of strings.

    - Removes empty strings.
    - Strips whitespace.
    """

    if values is None:
        return []

    normalized: list[str] = []

    for value in values:
        value = normalize_text(value)

        if value:
            normalized.append(value)

    return normalized


def merge_metadata(
    *sources: dict[str, Any] | None,
) -> dict[str, Any]:
    """
    Merge multiple metadata dictionaries.

    Later dictionaries override earlier ones.
    """

    merged: dict[str, Any] = {}

    for source in sources:
        if source:
            merged.update(source)

    return merged


def is_context_empty(
    *,
    conversation_context: list[str],
    working_memory: dict[str, Any],
    semantic_memory: list[str],
    episodic_memory: list[str],
    preferences: dict[str, Any],
    knowledge_context: list[str],
) -> bool:
    """
    Determine whether the context contains useful information.
    """

    return not any(
        (
            conversation_context,
            working_memory,
            semantic_memory,
            episodic_memory,
            preferences,
            knowledge_context,
        )
    )