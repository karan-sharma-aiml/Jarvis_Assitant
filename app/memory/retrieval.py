"""
Memory Retrieval Engine

Responsible for retrieving the most relevant memories
for the current user request.

This module orchestrates all memory sources.

It does NOT interact with any LLM directly.
"""

from __future__ import annotations

import logging

from app.memory.models import MemorySearchResult
from app.memory.semantic_memory import SemanticMemory

logger = logging.getLogger(__name__)


class MemoryRetriever:
    """
    Retrieves and ranks memories for a query.
    """

    def __init__(
        self,
        semantic_memory: SemanticMemory,
    ) -> None:
        self._semantic_memory = semantic_memory

    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> list[MemorySearchResult]:
        """
        Retrieve relevant memories.

        Args:
            query:
                User query.

            limit:
                Maximum memories.

        Returns:
            Ranked memory results.
        """

        results = self._semantic_memory.search(
            query=query,
            limit=limit,
        )

        results.sort(
            key=lambda item: (
                item.record.importance.value,
                item.score,
            ),
            reverse=True,
        )

        logger.info(
            "Retrieved %d memories for query '%s'",
            len(results),
            query,
        )

        return results

    def retrieve_context(
        self,
        query: str,
        limit: int = 5,
    ) -> str:
        """
        Convert retrieved memories into prompt context.
        """

        memories = self.retrieve(
            query=query,
            limit=limit,
        )

        if not memories:
            return ""

        context: list[str] = []

        for item in memories:

            context.append(
                f"- {item.record.key}: {item.record.value}"
            )

        return "\n".join(context)