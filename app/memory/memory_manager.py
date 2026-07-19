"""
Memory Manager

Central coordinator for the entire memory subsystem.

This class provides a single interface for interacting with
all memory modules.

Responsibilities:
- Initialize memory components
- Coordinate memory operations
- Retrieve prompt context
- Manage lifecycle

This module contains no SQLite queries.
"""

from __future__ import annotations

import logging

from app.memory.conversation import ConversationMemory
from app.memory.database import Database
from app.memory.episodic_memory import EpisodicMemory
from app.memory.preference_memory import PreferenceMemory
from app.memory.retrieval import MemoryRetriever
from app.memory.semantic_memory import SemanticMemory
from app.memory.summarizer import ConversationSummarizer
from app.memory.working_memory import WorkingMemory

logger = logging.getLogger(__name__)


class MemoryManager:
    """
    Central manager for the JARVIS memory system.
    """

    def __init__(self) -> None:
        self.database = Database()

        self.database.connect()
        self.database.initialize()

        self.working = WorkingMemory()

        self.preferences = PreferenceMemory(
            self.database
        )

        self.conversations = ConversationMemory(
            self.database
        )

        self.episodic = EpisodicMemory(
            self.database
        )

        self.semantic = SemanticMemory(
            self.database
        )

        self.retriever = MemoryRetriever(
            self.semantic
        )

        self.summarizer = ConversationSummarizer()

        logger.info(
            "Memory Manager initialized."
        )

    def retrieve_context(
        self,
        query: str,
        limit: int = 5,
    ) -> str:
        """
        Return prompt-ready context.
        """

        return self.retriever.retrieve_context(
            query=query,
            limit=limit,
        )

    def summarize(
        self,
        conversation: str,
    ):
        """
        Summarize conversation.
        """

        return self.summarizer.summarize(
            conversation
        )

    def health_check(
        self,
    ) -> bool:
        """
        Verify memory system.
        """

        try:

            self.database.execute(
                "SELECT 1"
            )

            return True

        except Exception as error:

            logger.exception(
                "Memory health check failed: %s",
                error,
            )

            return False

    def close(
        self,
    ) -> None:
        """
        Shutdown memory system.
        """

        self.database.close()

        logger.info(
            "Memory Manager closed."
        )

    def __enter__(
        self,
    ) -> "MemoryManager":
        return self

    def __exit__(
        self,
        exc_type,
        exc,
        traceback,
    ) -> None:
        self.close()