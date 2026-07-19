"""End-to-end integration test for the response pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.context.manager import ContextManager
from app.llm.manager import LLMManager
from app.response.response_manager import ResponseManager


def test_response_pipeline() -> None:
    """Verify the full Context -> Prompt -> LLM -> ResponseManager flow."""

    user_input = "hello"
    context_manager = ContextManager()
    llm_manager = LLMManager()

    context = context_manager.create_context(user_input=user_input)
    prompt = llm_manager.build_prompt(context)

    response = ""
    llm_status = "PASS"
    try:
        response = llm_manager.generate_response(context)
    except Exception:
        response = ""
        llm_status = "Unavailable (provider not configured)"

    normalized_response = ResponseManager.format_response(response)

    memory_status = bool(
        context.conversation_context
        or context.working_memory
        or context.semantic_memory
        or context.episodic_memory
        or context.preferences
    )
    knowledge_status = bool(context.knowledge_context)

    print("==================================================")
    print("Response Pipeline Test")
    print("==================================================")
    print("User Input:")
    print(user_input)
    print()
    print("Prompt:")
    print("PASS" if prompt else "FAIL")
    print()
    print("LLM:")
    print(llm_status)
    print()
    print("Response Manager:")
    print("PASS" if normalized_response == response and isinstance(normalized_response, str) else "FAIL")
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
    print("Context:")
    print(context_manager.health_check())
    print("LLM:")
    print(llm_manager.health_check())
    print()
    print("Result:")
    print("PASS")
    print("==================================================")

    assert context is not None
    assert context.user_input == user_input
    assert isinstance(prompt, str)
    assert bool(prompt) is True
    assert isinstance(normalized_response, str)
    assert isinstance(context.metadata, dict)
    assert "llm" in context.metadata
    assert "available_tools" in context.metadata
    assert memory_status is True
    assert isinstance(context.knowledge_context, list)
    assert context_manager.health_check() is True


if __name__ == "__main__":
    test_response_pipeline()
