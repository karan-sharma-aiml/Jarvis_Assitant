"""Lightweight conversation orchestration for JARVIS."""

from __future__ import annotations

from app.context.manager import ContextManager
from app.llm.manager import LLMManager
from app.memory.memory_manager import MemoryManager


class ConversationManager:
    """Coordinate context creation, response generation, and memory persistence."""

    def __init__(
        self,
        context_manager: ContextManager | None = None,
        llm_manager: LLMManager | None = None,
        memory_manager: MemoryManager | None = None,
    ) -> None:
        self._context_manager = context_manager or ContextManager()
        self._llm_manager = llm_manager or LLMManager()
        self._memory_manager = memory_manager or MemoryManager()

    def chat(self, message: str) -> str:
        """Create context, generate a response, and save the exchange."""
        if not message or not message.strip():
            return ""

        normalized_message = message.strip()
        context = self._context_manager.create_context(
            user_input=normalized_message,
        )
        response = self._llm_manager.generate_response(context)

        self._memory_manager.save_conversation(
            user_message=normalized_message,
            assistant_message=response,
        )

        return response
