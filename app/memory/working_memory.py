"""
Working Memory

Stores short-term runtime context for the current session.

Working memory is temporary and represents the active task,
current project, and runtime state.

It is intentionally lightweight and independent from
persistent long-term memory.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class WorkingMemoryState:
    """
    Represents the active working memory for the current session.
    """

    current_project: str = ""

    current_task: str = ""

    current_file: str = ""

    current_goal: str = ""

    active_roles: list[str] = field(default_factory=list)

    variables: dict[str, Any] = field(default_factory=dict)


class WorkingMemory:
    """
    Stores temporary runtime information.

    Data exists only during the current execution.
    """

    def __init__(self) -> None:
        self._state = WorkingMemoryState()

    @property
    def state(self) -> WorkingMemoryState:
        """
        Return current working memory.
        """
        return self._state

    def update(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Update one or more working memory fields.
        """

        for key, value in kwargs.items():

            if hasattr(self._state, key):

                setattr(self._state, key, value)

                logger.debug(
                    "Working memory updated: %s",
                    key,
                )

    def set_variable(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store a runtime variable.
        """

        self._state.variables[key] = value

    def get_variable(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve a runtime variable.
        """

        return self._state.variables.get(
            key,
            default,
        )

    def remove_variable(
        self,
        key: str,
    ) -> bool:
        """
        Remove a runtime variable.
        """

        if key not in self._state.variables:
            return False

        del self._state.variables[key]

        return True

    def clear(self) -> None:
        """
        Reset working memory.
        """

        self._state = WorkingMemoryState()

        logger.info(
            "Working memory cleared."
        )