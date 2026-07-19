"""
JARVIS Prompt Builder

This module builds the final prompt sent to the LLM.

It combines:

- Static system prompt
- Selected expert roles
- Conversation memory
- Retrieved RAG context
- Runtime instructions

This module intentionally does NOT depend on any
specific LLM provider.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from textwrap import dedent

from app.llm.prompts.roles import ROLES
from app.llm.prompts.system import SYSTEM_PROMPT


@dataclass(slots=True)
class PromptContext:
    """
    Runtime prompt context.

    Every field is optional.
    Empty values are ignored by PromptBuilder.
    """

    roles: list[str] = field(default_factory=list)

    memory: str = ""

    rag_context: str = ""

    conversation_history: str = ""

    user_instruction: str = ""

    additional_context: str = ""


class PromptBuilder:
    """
    Builds the final prompt for every LLM request.
    """

    @staticmethod
    def _build_roles(role_names: list[str]) -> str:
        """
        Build the selected role prompts.
        """

        if not role_names:
            return ""

        sections: list[str] = []

        for role in role_names:

            prompt = ROLES.get(role)

            if prompt:
                sections.append(prompt)

        return "\n\n".join(sections)

    @classmethod
    def build(
        cls,
        context: PromptContext,
    ) -> str:
        """
        Build the complete prompt.
        """

        parts: list[str] = [SYSTEM_PROMPT]

        role_prompt = cls._build_roles(context.roles)

        if role_prompt:

            parts.extend(
                [
                    "",
                    "# Active Expert Roles",
                    role_prompt,
                ]
            )

        if context.memory:

            parts.extend(
                [
                    "",
                    "# Long-Term Memory",
                    context.memory,
                ]
            )

        if context.rag_context:

            parts.extend(
                [
                    "",
                    "# Retrieved Knowledge",
                    context.rag_context,
                ]
            )

        if context.conversation_history:

            parts.extend(
                [
                    "",
                    "# Conversation History",
                    context.conversation_history,
                ]
            )

        if context.additional_context:

            parts.extend(
                [
                    "",
                    "# Additional Context",
                    context.additional_context,
                ]
            )

        if context.user_instruction:

            parts.extend(
                [
                    "",
                    "# Current User Request",
                    context.user_instruction,
                ]
            )

        return dedent("\n".join(parts)).strip()