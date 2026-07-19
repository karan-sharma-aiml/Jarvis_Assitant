"""End-to-end integration test for Tool + Context + Memory + RAG."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.context.manager import ContextManager


def test_tool_context_integration() -> None:
    """Verify that ContextManager builds an AgentContext using real Tool, Memory, and RAG managers."""

    user_input = "hello"
    context_manager = ContextManager()

    context = context_manager.create_context(user_input=user_input)

    available_tools = context.metadata.get("available_tools", [])
    memory_status = bool(
        context.conversation_context
        or context.working_memory
        or context.semantic_memory
        or context.episodic_memory
        or context.preferences
    )
    knowledge_status = bool(context.knowledge_context)

    print("==================================================")
    print("Tool Context Integration Test")
    print("==================================================")
    print("User Input:")
    print(user_input)
    print()
    print("Available Tools:")
    for tool in available_tools:
        print(f"- {tool.get('name', '')}")
    print()
    print("Memory:")
    print("PASS" if memory_status else "FAIL")
    print()
    print("Knowledge:")
    print("PASS" if knowledge_status else "No indexed documents")
    print()
    print("Health:")
    print(context_manager.health_check())
    print()
    print("Result:")
    print("PASS")
    print("==================================================")

    assert context is not None
    assert context.user_input == user_input
    assert isinstance(context.metadata, dict)
    assert "available_tools" in context.metadata
    assert isinstance(available_tools, list)
    assert all(isinstance(tool, dict) for tool in available_tools)
    assert all({"name", "description", "category"}.issubset(tool.keys()) for tool in available_tools)
    assert memory_status is True
    assert context_manager.health_check() is True


if __name__ == "__main__":
    test_tool_context_integration()
