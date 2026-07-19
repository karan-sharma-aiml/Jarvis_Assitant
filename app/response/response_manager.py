"""Lightweight response normalization for JARVIS."""

from __future__ import annotations

import re


class ResponseManager:
    """Normalize raw LLM output into a clean string response."""

    @staticmethod
    def format_response(response: str) -> str:
        """Normalize whitespace and trim surrounding whitespace."""
        if not response:
            return ""

        normalized = response.replace("\r\n", "\n").replace("\r", "\n")
        normalized = re.sub(r"\n{3,}", "\n\n", normalized)
        normalized = normalized.strip()
        return normalized
