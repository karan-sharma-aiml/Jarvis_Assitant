"""
JARVIS Action

Represents a single executable action.

Responsibilities
----------------
- Represent a tool invocation
- Store tool arguments
- Store execution metadata

Contains NO execution logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Action:
    """
    Represents one executable action.
    """

    tool_name: str

    arguments: dict[str, Any] = field(default_factory=dict)

    description: str = ""

    priority: int = 0

    retry_count: int = 0

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def has_arguments(self) -> bool:
        """
        Return True if arguments exist.
        """
        return bool(self.arguments)

    def increment_retry(self) -> None:
        """
        Increase retry count.
        """
        self.retry_count += 1

    def reset_retry(self) -> None:
        """
        Reset retry counter.
        """
        self.retry_count = 0