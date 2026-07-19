"""Integration test for the Memory-to-Context flow."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.context.manager import ContextManager


def test_memory_context_integration() -> None:
    """Verify that ContextManager builds an AgentContext from MemoryManager data."""

    user_input = "Hello there"
    context_manager = ContextManager()

    context = context_manager.create_context(user_input=user_input)

    print("==================================================")
    print("Memory Integration Test")
    print("==================================================")
    print("User Input:")
    print(user_input)
    print()
    print("Conversation:")
    print(context.conversation_context)
    print()
    print("Working Memory:")
    print(context.working_memory)
    print()
    print("Semantic Memory:")
    print(context.semantic_memory)
    print()
    print("Episodic Memory:")
    print(context.episodic_memory)
    print()
    print("Preferences:")
    print(context.preferences)
    print()
    print("Health:")
    print(context_manager.health_check())
    print()
    print("Result:")
    print("PASS")
    print("==================================================")

    assert context is not None
    assert context.user_input == user_input
    assert isinstance(context.conversation_context, list)
    assert isinstance(context.working_memory, dict)
    assert isinstance(context.semantic_memory, list)
    assert isinstance(context.episodic_memory, list)
    assert isinstance(context.preferences, dict)
    assert context.has_memory is True
    assert isinstance(context.has_knowledge, bool)
    assert context_manager.health_check() is True


if __name__ == "__main__":
    test_memory_context_integration()
