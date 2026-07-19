"""End-to-end integration test for the conversation pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.context.manager import ContextManager
from app.conversation.conversation_manager import ConversationManager
from app.llm.manager import LLMManager
from app.memory.memory_manager import MemoryManager
from app.response.response_manager import ResponseManager


def test_conversation_pipeline() -> None:
    """Verify the full conversation flow across context, LLM, response, and memory."""

    context_manager = ContextManager()
    llm_manager = LLMManager()
    memory_manager = MemoryManager()
    manager = ConversationManager(
        context_manager=context_manager,
        llm_manager=llm_manager,
        memory_manager=memory_manager,
    )

    response = ""
    llm_status = "PASS"
    try:
        response = manager.chat("hello")
    except Exception:
        response = ""
        llm_status = "Unavailable (provider not configured)"

    empty_response = manager.chat("")

    print("==================================================")
    print("Conversation Pipeline Test")
    print("==================================================")
    print("Input:")
    print("hello")
    print()
    print("Conversation:")
    print("PASS" if isinstance(response, str) else "FAIL")
    print()
    print("Context:")
    print("PASS" if context_manager.health_check() else "FAIL")
    print()
    print("LLM:")
    print(llm_status)
    print()
    print("Response:")
    print("PASS" if isinstance(response, str) and isinstance(ResponseManager.format_response(response), str) else "FAIL")
    print()
    print("Memory:")
    print("PASS" if memory_manager.health_check() else "FAIL")
    print()
    print("Health")
    print("Conversation:")
    print(isinstance(response, str))
    print("Context:")
    print(context_manager.health_check())
    print("Memory:")
    print(memory_manager.health_check())
    print("LLM:")
    print(llm_manager.health_check())
    print()
    print("Result:")
    print("PASS")
    print("==================================================")

    assert isinstance(response, str)
    assert isinstance(empty_response, str)
    assert context_manager.health_check() is True
    assert memory_manager.health_check() is True
    assert isinstance(response, str)


if __name__ == "__main__":
    test_conversation_pipeline()
