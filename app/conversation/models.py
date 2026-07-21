"""
Conversation Models

Shared models for the conversation layer.

Responsibilities
----------------
- Represent conversation messages.
- Store conversation context.
- Represent conversation state.

Contains NO business logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class MessageRole(str, Enum):
    """
    Role of a conversation message.
    """

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass(slots=True)
class ConversationMessage:
    """
    Represents a single message in a conversation.
    """

    role: MessageRole
    content: str

    metadata: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "role": self.role.value,
            "content": self.content,
            "metadata": self.metadata,
        }

    def __repr__(self) -> str:
        return (
            f"ConversationMessage("
            f"role={self.role.value}, "
            f"content={self.content!r})"
        )


@dataclass(slots=True)
class ConversationContext:
    """
    Stores conversation history.
    """

    messages: list[ConversationMessage] = field(default_factory=list)

    metadata: dict[str, object] = field(default_factory=dict)

    def add_message(
        self,
        message: ConversationMessage,
    ) -> None:
        self.messages.append(message)

    def clear(self) -> None:
        self.messages.clear()

    @property
    def total_messages(self) -> int:
        return len(self.messages)

    @property
    def is_empty(self) -> bool:
        return len(self.messages) == 0

    def to_dict(self) -> dict[str, object]:
        return {
            "messages": [
                message.to_dict()
                for message in self.messages
            ],
            "metadata": self.metadata,
        }

    def __repr__(self) -> str:
        return (
            f"ConversationContext("
            f"messages={self.total_messages})"
        )