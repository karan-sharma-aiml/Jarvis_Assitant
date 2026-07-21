"""
Planner Parser

Parses a user command into smaller command segments.

Responsibilities
----------------
- Split compound commands.
- Normalize whitespace.
- Preserve execution order.

Contains NO planning or execution logic.
"""

from __future__ import annotations

import re


class CommandParser:
    """Splits compound commands into individual commands."""

    _PATTERN = re.compile(r"\s*(?:,| and | then | after that )\s*", flags=re.IGNORECASE)

    def parse(self, command: str | None) -> list[str]:
        """Parse a command into individual command strings."""
        if not isinstance(command, str):
            return []

        normalized_command = command.strip()
        if not normalized_command:
            return []

        parts = self._PATTERN.split(normalized_command)
        return [part.strip() for part in parts if part.strip()]

    def health_check(self) -> bool:
        """Return True when the parser is usable."""
        return True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"