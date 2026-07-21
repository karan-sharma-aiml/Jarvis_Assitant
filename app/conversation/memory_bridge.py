"""
Memory Bridge

Bridges the Conversation layer with the existing Memory system.

Responsibilities
----------------
- Save conversation messages.
- Load recent conversation.
- Keep Conversation independent from Memory implementation.
"""

from __future__ import annotations

from app.conversation.models import (
    ConversationContext,
    ConversationMessage,
)


class MemoryBridge:
    """
    Bridge between ConversationManager and MemoryManager.
    """

    def __init__(self, memory_manager) -> None:
        self._memory = memory_manager

    def save_context(
        self,
        context: ConversationContext,
    ) -> None:
        """
        Save all conversation messages.
        """

        for message in context.messages:
            self._memory.save(
                role=message.role.value,
                content=message.content,
            )

    def load_recent(
        self,
        limit: int = 10,
    ) -> list[ConversationMessage]:
        """
        Load recent conversation from memory.
        """

        records = self._memory.load(limit=limit)

        messages: list[ConversationMessage] = []

        for record in records:

            messages.append(
                ConversationMessage(
                    role=record.role,
                    content=record.content,
                )
            )

        return messages

    def health_check(self) -> bool:
        return self._memory is not None

    def __repr__(self) -> str:
        return "MemoryBridge()"