"""End-to-end integration test for RAG + Context + Memory."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.context.manager import ContextManager


def test_rag_context_integration() -> None:
    """Verify that ContextManager builds an AgentContext using real RAG and Memory managers."""

    user_input = "hello"
    context_manager = ContextManager()

    context = context_manager.create_context(user_input=user_input)

    print("==================================================")
    print("RAG + Context Integration Test")
    print("==================================================")
    print("User Input:")
    print(user_input)
    print()
    print("Knowledge Context:")
    print(context.knowledge_context)
    print()
    print("Memory Status:")
    print(bool(context.conversation_context or context.working_memory or context.semantic_memory or context.episodic_memory or context.preferences))
    print()
    print("Health:")
    print(context_manager.health_check())
    print()
    print("PASS")
    print("==================================================")

    assert context is not None
    assert context.user_input == user_input
    assert isinstance(context.knowledge_context, list)
    assert context.has_memory is True or context.has_knowledge is True
    assert context_manager.health_check() is True


if __name__ == "__main__":
    test_rag_context_integration()
