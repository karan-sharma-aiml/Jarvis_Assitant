"""
JARVIS Context Builder

Builds a unified AgentContext from multiple sources.

Responsibilities
----------------
- Aggregate context data.
- Create AgentContext.
- Keep context creation centralized.

Contains NO memory retrieval.
Contains NO RAG retrieval.
Contains NO LLM calls.
"""

from __future__ import annotations

from typing import Any

from app.context.models import AgentContext
from app.context.utils import merge_metadata, normalize_list, normalize_text


class ContextBuilder:
    """
    Builds AgentContext objects.
    """

    def build(
        self,
        *,
        user_input: str,
        conversation_context: list[str] | None = None,
        working_memory: dict[str, Any] | None = None,
        semantic_memory: list[str] | None = None,
        episodic_memory: list[str] | None = None,
        preferences: dict[str, Any] | None = None,
        knowledge_context: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AgentContext:
        """
        Create a fully populated AgentContext.
        """

        return AgentContext(
            user_input=normalize_text(user_input),
            conversation_context=normalize_list(conversation_context),
            working_memory=working_memory or {},
            semantic_memory=normalize_list(semantic_memory),
            episodic_memory=normalize_list(episodic_memory),
            preferences=preferences or {},
            knowledge_context=normalize_list(knowledge_context),
            metadata=merge_metadata(metadata),
        )