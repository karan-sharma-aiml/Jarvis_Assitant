"""
JARVIS Context Manager

Public interface for the Context Engine.

Responsibilities
----------------
- Build AgentContext objects.
- Expose a stable API to the Agent Engine.
- Hide ContextBuilder implementation details.

Contains NO memory retrieval.
Contains NO RAG retrieval.
Contains NO LLM logic.
Contains NO tool execution.
"""

from __future__ import annotations

from typing import Any

from app.context.builder import ContextBuilder
from app.context.models import AgentContext
from app.llm.manager import LLMManager
from app.memory.memory_manager import MemoryManager
from app.rag.rag_manager import RAGManager
from app.tools.manager import ToolManager


class ContextManager:
    """
    Public interface for the Context Engine.
    """

    def __init__(
        self,
        builder: ContextBuilder | None = None,
        memory_manager: MemoryManager | None = None,
        rag_manager: RAGManager | None = None,
        tool_manager: ToolManager | None = None,
        llm_manager: LLMManager | None = None,
    ) -> None:
        self._builder = builder or ContextBuilder()
        self._memory_manager = memory_manager or MemoryManager()
        self._rag_manager = rag_manager or RAGManager()
        self._tool_manager = tool_manager or ToolManager()
        self._llm_manager = llm_manager or LLMManager()

    @property
    def builder(self) -> ContextBuilder:
        """
        Read-only access to the ContextBuilder.
        """
        return self._builder

    @property
    def memory_manager(self) -> MemoryManager:
        """
        Read-only access to the MemoryManager.
        """
        return self._memory_manager

    @property
    def rag_manager(self) -> RAGManager:
        """
        Read-only access to the RAGManager.
        """
        return self._rag_manager

    @property
    def tool_manager(self) -> ToolManager:
        """
        Read-only access to the ToolManager.
        """
        return self._tool_manager

    @property
    def llm_manager(self) -> LLMManager:
        """
        Read-only access to the LLMManager.
        """
        return self._llm_manager

    def create_context(
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
        Create a new AgentContext.
        """

        memory_payload = self._memory_manager.get_context_payload(
            query=user_input,
            limit=5,
        )

        knowledge_context = (
            knowledge_context
            if knowledge_context is not None
            else self._rag_manager.get_context_knowledge(
                user_input,
            )
        )

        merged_metadata: dict[str, Any] = {}

        if metadata is not None:
            merged_metadata.update(metadata)

        merged_metadata["available_tools"] = (
            self._tool_manager.get_context_tools()
        )
        merged_metadata["llm"] = self._llm_manager.get_context_llm()

        return self._builder.build(
            user_input=user_input,
            conversation_context=(
                conversation_context
                if conversation_context is not None
                else memory_payload.get("conversation_context")
            ),
            working_memory=(
                working_memory
                if working_memory is not None
                else memory_payload.get("working_memory")
            ),
            semantic_memory=(
                semantic_memory
                if semantic_memory is not None
                else memory_payload.get("semantic_memory")
            ),
            episodic_memory=(
                episodic_memory
                if episodic_memory is not None
                else memory_payload.get("episodic_memory")
            ),
            preferences=(
                preferences
                if preferences is not None
                else memory_payload.get("preferences")
            ),
            knowledge_context=knowledge_context,
            metadata=merged_metadata,
        )

    def health_check(self) -> bool:
        """
        Verify Context Engine health.
        """
        return isinstance(self._builder, ContextBuilder) and isinstance(
            self._memory_manager,
            MemoryManager,
        ) and isinstance(self._rag_manager, RAGManager) and isinstance(
            self._tool_manager,
            ToolManager,
        ) and isinstance(self._llm_manager, LLMManager)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(builder={self._builder.__class__.__name__}, "
            f"memory_manager={self._memory_manager.__class__.__name__}, "
            f"rag_manager={self._rag_manager.__class__.__name__}, "
            f"tool_manager={self._tool_manager.__class__.__name__}, "
            f"llm_manager={self._llm_manager.__class__.__name__})"
        )