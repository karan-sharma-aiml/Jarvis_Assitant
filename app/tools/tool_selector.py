"""
JARVIS Tool Selector

Selects the most appropriate tool
for a user query.

Responsibilities:
- Analyze query
- Score tools
- Return best matching tool

Contains NO execution logic.
"""

from __future__ import annotations

import re
from collections import defaultdict

from app.tools.registry import ToolRegistry


class ToolSelector:
    """
    Rule-based tool selector.

    Future:
    LLM based tool routing.
    """

    KEYWORDS = {

        "calculator": {
            "calculate",
            "math",
            "add",
            "subtract",
            "multiply",
            "divide",
            "+",
            "-",
            "*",
            "/",
            "%",
        },

        "datetime": {
            "date",
            "time",
            "today",
            "day",
            "month",
            "year",
            "clock",
        },

        "weather": {
            "weather",
            "temperature",
            "rain",
            "humidity",
            "wind",
            "forecast",
        },

        "search": {
            "search",
            "find",
            "google",
            "bing",
            "duckduckgo",
            "lookup",
        },

        "browser": {
            "open",
            "website",
            "url",
            "browser",
            "visit",
        },

        "filesystem": {
            "file",
            "folder",
            "directory",
            "read",
            "write",
            "delete",
            "create",
        },

        "terminal": {
            "terminal",
            "command",
            "shell",
            "cmd",
            "powershell",
            "python",
            "git",
            "pip",
        },

        "email": {
            "email",
            "mail",
            "send",
            "gmail",
            "outlook",
        },

        "calendar": {
            "calendar",
            "meeting",
            "event",
            "schedule",
            "appointment",
            "reminder",
        },
    }

    def __init__(
        self,
        registry: ToolRegistry,
    ) -> None:

        self._registry = registry

    def select(
        self,
        query: str,
    ) -> str | None:
        """
        Return best matching tool.
        """

        tokens = re.findall(
            r"\w+",
            query.lower(),
        )

        scores = defaultdict(int)

        for tool, keywords in self.KEYWORDS.items():

            if not self._registry.exists(tool):
                continue

            for token in tokens:

                if token in keywords:
                    scores[tool] += 1

        if not scores:
            return None

        return max(
            scores,
            key=scores.get,
        )

    def rank(
        self,
        query: str,
    ) -> list[tuple[str, int]]:
        """
        Return ranked tools.
        """

        tokens = re.findall(
            r"\w+",
            query.lower(),
        )

        scores = defaultdict(int)

        for tool, keywords in self.KEYWORDS.items():

            if not self._registry.exists(tool):
                continue

            for token in tokens:

                if token in keywords:
                    scores[tool] += 1

        return sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )