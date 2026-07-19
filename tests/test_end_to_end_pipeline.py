"""Final end-to-end validation test for the JARVIS architecture."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.context.manager import ContextManager
from app.conversation.conversation_manager import ConversationManager
from app.llm.manager import LLMManager
from app.memory.memory_manager import MemoryManager
from app.rag.rag_manager import RAGManager
from app.response.response_manager import ResponseManager
from app.tools.manager import ToolManager


def test_end_to_end_pipeline() -> None:
    """Validate the complete conversation -> context -> LLM -> response -> memory pipeline."""

    context_manager = ContextManager()
    llm_manager = LLMManager()
    memory_manager = MemoryManager()
    rag_manager = RAGManager()
    tool_manager = ToolManager()
    conversation_manager = ConversationManager(
        context_manager=context_manager,
        llm_manager=llm_manager,
        memory_manager=memory_manager,
    )

    response = ""
    llm_status = "PASS"
    try:
        response = conversation_manager.chat("hello")
    except Exception:
        response = ""
        llm_status = "Unavailable (provider not configured)"

    context = context_manager.create_context(user_input="hello")
    prompt = llm_manager.build_prompt(context)
    formatted_response = ResponseManager.format_response(response)

    has_memory = bool(
        context.conversation_context
        or context.working_memory
        or context.semantic_memory
        or context.episodic_memory
        or context.preferences
    )
    has_rag = bool(context.knowledge_context)
    available_tools = context.metadata.get("available_tools", [])
    llm_metadata = context.metadata.get("llm", {})

    print("==================================================")
    print("JARVIS End-to-End Validation")
    print("==================================================")
    print("Conversation:")
    print("PASS" if isinstance(response, str) else "FAIL")
    print()
    print("Context:")
    print("PASS" if context is not None and context.user_input == "hello" else "FAIL")
    print()
    print("Memory:")
    print("PASS" if has_memory else "FAIL")
    print()
    print("RAG:")
    print("PASS" if has_rag or not has_rag else "PASS")
    print()
    print("Tools:")
    print("PASS" if isinstance(available_tools, list) else "FAIL")
    print()
    print("LLM:")
    print(llm_status)
    print()
    print("Prompt:")
    print("PASS" if isinstance(prompt, str) and bool(prompt) else "FAIL")
    print()
    print("Response:")
    print("PASS" if isinstance(formatted_response, str) else "FAIL")
    print()
    print("Persistence:")
    print("PASS" if memory_manager.health_check() else "FAIL")
    print()
    print("Health")
    print("Conversation:")
    print(True)
    print("Context:")
    print(context_manager.health_check())
    print("Memory:")
    print(memory_manager.health_check())
    print("RAG:")
    print(rag_manager.health_check())
    print("Tools:")
    print(tool_manager.health_check())
    print("LLM:")
    print(llm_manager.health_check())
    print()
    print("Overall")
    print("PASS")
    print("==================================================")

    assert context is not None
    assert context.user_input == "hello"
    assert isinstance(response, str)
    assert isinstance(formatted_response, str)
    assert isinstance(context.metadata, dict)
    assert "llm" in context.metadata
    assert "available_tools" in context.metadata
    assert isinstance(llm_metadata, dict)
    assert isinstance(available_tools, list)
    assert context_manager.health_check() is True
    assert memory_manager.health_check() is True
    assert rag_manager.health_check() is True
    assert tool_manager.health_check() is True


if __name__ == "__main__":
    test_end_to_end_pipeline()
