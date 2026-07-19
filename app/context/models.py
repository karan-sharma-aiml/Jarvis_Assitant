"""
JARVIS Context Models

Defines the normalized context object used by the Agent Engine.

Responsibilities
----------------
- Store all contextual information for one agent cycle.
- Provide a unified interface between Memory, RAG, Agent and LLM.

Contains NO business logic.
Contains NO retrieval logic.
Contains NO LLM logic.
Contains NO tool execution logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Any


@dataclass(slots=True)
class AgentContext:
    """
    Unified context passed through the complete agent pipeline.

    This object aggregates information collected from
    different subsystems before reasoning begins.

    It is intentionally a pure data model.
    """

    # ------------------------------------------------------------------
    # User
    # ------------------------------------------------------------------

    user_input: str = ""

    # ------------------------------------------------------------------
    # Memory
    # ------------------------------------------------------------------

    conversation_context: list[str] = field(default_factory=list)

    working_memory: dict[str, Any] = field(default_factory=dict)

    semantic_memory: list[str] = field(default_factory=list)

    episodic_memory: list[str] = field(default_factory=list)

    preferences: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Knowledge (RAG)
    # ------------------------------------------------------------------

    knowledge_context: list[str] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    metadata: dict[str, Any] = field(default_factory=dict)

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    @property
    def has_memory(self) -> bool:
        """
        Returns True if any memory source contains data.
        """

        return any(
            (
                self.conversation_context,
                self.working_memory,
                self.semantic_memory,
                self.episodic_memory,
                self.preferences,
            )
        )

    @property
    def has_knowledge(self) -> bool:
        """
        Returns True if retrieved knowledge exists.
        """

        return bool(self.knowledge_context)

    @property
    def is_empty(self) -> bool:
        """
        Returns True if no contextual information exists.
        """

        return not (
            self.has_memory
            or self.has_knowledge
            or self.metadata
        )