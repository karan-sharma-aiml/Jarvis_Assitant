"""
JARVIS Master System Prompt.

This module composes the permanent system prompt by combining
the foundational prompt modules.

The resulting prompt represents the core operating principles of
JARVIS and remains provider-independent.

This module does NOT inject:

- Conversation history
- Memory
- Retrieved RAG context
- User-specific instructions
- Runtime variables

Those are added later by builder.py.
"""

from __future__ import annotations

from textwrap import dedent

from app.llm.prompts.behavior import SYSTEM_BEHAVIOR
from app.llm.prompts.coding import CODING_PROMPT
from app.llm.prompts.identity import SYSTEM_IDENTITY
from app.llm.prompts.productivity import PRODUCTIVITY_PROMPT
from app.llm.prompts.safety import SAFETY_PROMPT

PROMPT_VERSION: str = "1.0.0"


class SystemPrompt:
    """
    Composes the static system prompt for JARVIS.

    This class combines all permanent prompt modules while keeping
    runtime information separate.

    Runtime context is injected later by PromptBuilder.
    """

    @staticmethod
    def build() -> str:
        """
        Build the complete static system prompt.

        Returns:
            Complete system prompt.
        """

        sections = [
            "# JARVIS SYSTEM PROMPT",
            f"Version: {PROMPT_VERSION}",
            "",
            SYSTEM_IDENTITY,
            "",
            SYSTEM_BEHAVIOR,
            "",
            CODING_PROMPT,
            "",
            PRODUCTIVITY_PROMPT,
            "",
            SAFETY_PROMPT,
        ]

        return dedent("\n".join(sections)).strip()


SYSTEM_PROMPT: str = SystemPrompt.build()