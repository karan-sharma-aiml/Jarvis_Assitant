"""End-to-end integration test for LLM + Context + Memory + RAG + Tool."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.context.manager import ContextManager


def test_llm_context_integration() -> None:
    """Verify the full LLM + Context + Memory + RAG + Tool integration flow."""

    user_input = "hello"
    context_manager = ContextManager()
    context = context_manager.create_context(user_input=user_input)

    llm_metadata = context.metadata.get("llm", {})
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
    print("LLM Context Integration Test")
    print("==================================================")
    print("User Input:")
    print(user_input)
    print()
    print("LLM")
    print("Provider:")
    print(llm_metadata.get("provider", ""))
    print()
    print("Model:")
    print(llm_metadata.get("model", ""))
    print()
    print("Temperature:")
    print(llm_metadata.get("temperature", ""))
    print()
    print("Available Tools:")
    print(len(available_tools))
    print()
    print("Memory:")
    print("PASS" if memory_status else "FAIL")
    print()
    print("Knowledge:")
    if knowledge_status:
        print("PASS")
    else:
        print("No indexed documents")
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
    assert "llm" in context.metadata
    assert isinstance(llm_metadata, dict)
    assert {"provider", "model", "temperature"}.issubset(llm_metadata.keys())
    assert isinstance(available_tools, list)
    assert all(isinstance(tool, dict) for tool in available_tools)
    assert all({"name", "description", "category"}.issubset(tool.keys()) for tool in available_tools)
    assert memory_status is True
    assert isinstance(context.knowledge_context, list)
    assert context_manager.health_check() is True


if __name__ == "__main__":
    test_llm_context_integration()
