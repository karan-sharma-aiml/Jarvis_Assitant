"""
Conversation Manager

Manages conversation history and context.

Responsibilities
----------------
- Store conversation messages.
- Retrieve recent history.
- Clear conversation.

Contains NO LLM logic.
"""

from __future__ import annotations

from app.conversation.models import (
    ConversationContext,
    ConversationMessage,
    MessageRole,
)


class ConversationManager:
    """
    Manages conversation state.
    """

    def __init__(self) -> None:

        self._context = ConversationContext()

    @property
    def context(self) -> ConversationContext:
        return self._context

    def add_user_message(
        self,
        content: str,
    ) -> None:

        self._context.add_message(
            ConversationMessage(
                role=MessageRole.USER,
                content=content,
            )
        )

    def add_assistant_message(
        self,
        content: str,
    ) -> None:

        self._context.add_message(
            ConversationMessage(
                role=MessageRole.ASSISTANT,
                content=content,
            )
        )

    def get_history(
        self,
        limit: int | None = None,
    ) -> list[ConversationMessage]:

        if limit is None:
            return list(self._context.messages)

        return self._context.messages[-limit:]

    def clear(self) -> None:
        self._context.clear()

    def health_check(self) -> bool:
        return True

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(messages={self._context.total_messages})"
        )