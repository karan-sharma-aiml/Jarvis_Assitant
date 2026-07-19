"""
Conversation Summarizer

Provides lightweight conversation summarization.

Current Version:
    Rule-based summarization.

Future Version:
    Uses PromptBuilder + LLMManager to create AI-generated summaries.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(slots=True)
class ConversationSummary:
    """
    Represents a summarized conversation.
    """

    summary: str

    message_count: int

    original_length: int

    summary_length: int


class ConversationSummarizer:
    """
    Compresses conversation history.

    This implementation intentionally avoids any LLM dependency.
    """

    def summarize(
        self,
        conversation: str,
        max_sentences: int = 5,
    ) -> ConversationSummary:
        """
        Generate a lightweight summary.

        Args:
            conversation:
                Full conversation text.

            max_sentences:
                Maximum number of sentences to keep.

        Returns:
            ConversationSummary
        """

        cleaned = re.sub(
            r"\s+",
            " ",
            conversation,
        ).strip()

        sentences = re.split(
            r"(?<=[.!?])\s+",
            cleaned,
        )

        selected = sentences[:max_sentences]

        summary = " ".join(selected)

        return ConversationSummary(
            summary=summary,
            message_count=len(sentences),
            original_length=len(cleaned),
            summary_length=len(summary),
        )