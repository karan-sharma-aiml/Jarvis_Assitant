"""
JARVIS Agent State

Central state object shared across the entire Agent Engine.

Responsibilities:
- Store user request
- Store planning information
- Store reasoning
- Store tool execution state
- Store memory context
- Store RAG context
- Store final response

Contains NO business logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class AgentState:
    """
    Shared mutable state for the JARVIS Agent.
    """

    # -----------------------------
    # User
    # -----------------------------

    user_input: str = ""

    # -----------------------------
    # Planning
    # -----------------------------

    goal: str = ""

    plan: list[str] = field(default_factory=list)

    current_step: int = 0

    # -----------------------------
    # Reasoning
    # -----------------------------

    thoughts: list[str] = field(default_factory=list)

    # -----------------------------
    # Tool Calling
    # -----------------------------

    selected_tool: str | None = None

    tool_arguments: dict[str, Any] = field(default_factory=dict)

    tool_result: Any = None

    # -----------------------------
    # Memory
    # -----------------------------

    conversation_context: str = ""

    semantic_context: str = ""

    episodic_context: str = ""

    preference_context: str = ""

    # -----------------------------
    # Knowledge (RAG)
    # -----------------------------

    retrieved_documents: list[str] = field(default_factory=list)

    # -----------------------------
    # LLM
    # -----------------------------

    prompt: str = ""

    llm_response: str = ""

    # -----------------------------
    # Final
    # -----------------------------

    final_response: str = ""

    success: bool = False

    error: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    def reset(self) -> None:
        """
        Reset the state for the next request.
        """

        self.user_input = ""

        self.goal = ""

        self.plan.clear()

        self.current_step = 0

        self.thoughts.clear()

        self.selected_tool = None

        self.tool_arguments.clear()

        self.tool_result = None

        self.conversation_context = ""

        self.semantic_context = ""

        self.episodic_context = ""

        self.preference_context = ""

        self.retrieved_documents.clear()

        self.prompt = ""

        self.llm_response = ""

        self.final_response = ""

        self.success = False

        self.error = None

        self.metadata.clear()