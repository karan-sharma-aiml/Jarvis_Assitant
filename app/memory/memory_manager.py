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
from datetime import UTC, datetime

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

    def get_context_payload(
        self,
        query: str,
        limit: int = 5,
    ) -> dict[str, object]:
        """
        Return a structured memory payload for AgentContext creation.
        """

        conversation_context = [
            (
                f"User: {entry.get('user', '')}\n"
                f"Assistant: {entry.get('assistant', '')}"
            ).strip()
            for entry in self.conversations.recent(limit=limit)
            if isinstance(entry, dict)
        ]

        working_memory = {
            "current_project": self.working.state.current_project,
            "current_task": self.working.state.current_task,
            "current_file": self.working.state.current_file,
            "current_goal": self.working.state.current_goal,
            "active_roles": list(self.working.state.active_roles),
            "variables": dict(self.working.state.variables),
        }

        semantic_memory = [
            f"- {item.record.key}: {item.record.value}"
            for item in self.retriever.retrieve(
                query=query,
                limit=limit,
            )
        ]

        episodic_memory = [
            (
                f"{entry.get('title', '')}: {entry.get('description', '')}"
            ).strip()
            for entry in self.episodic.list_events()
            if isinstance(entry, dict)
        ]

        preferences = self.preferences.list_preferences()

        return {
            "conversation_context": conversation_context,
            "working_memory": working_memory,
            "semantic_memory": semantic_memory,
            "episodic_memory": episodic_memory,
            "preferences": preferences,
        }

    def save_conversation(
        self,
        user_message: str,
        assistant_message: str,
    ) -> None:
        """Persist one user/assistant exchange through the memory subsystem."""
        timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S%f")
        self.conversations.save(
            key=f"conversation-{timestamp}",
            user_message=user_message,
            assistant_message=assistant_message,
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