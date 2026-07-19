"""
JARVIS Tool Registry

Maintains a registry of all available tools.

Responsibilities:
- Register tools
- Unregister tools
- Retrieve tools
- List registered tools

Contains NO execution logic.
"""

from __future__ import annotations

import logging

from app.tools.base import BaseTool
from app.tools.exceptions import (
    ToolNotFoundError,
    ToolRegistrationError,
)

logger = logging.getLogger(__name__)


class ToolRegistry:
    """
    Registry for JARVIS tools.
    """

    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """
        Register a tool.

        Raises:
            ToolRegistrationError:
                If a tool with the same name already exists.
        """
        if tool.name in self._tools:
            raise ToolRegistrationError(
                f"Tool '{tool.name}' is already registered."
            )

        self._tools[tool.name] = tool

        logger.info("Registered tool: %s", tool.name)

    def unregister(self, tool_name: str) -> None:
        """
        Remove a tool from the registry.
        """
        if tool_name not in self._tools:
            raise ToolNotFoundError(
                f"Tool '{tool_name}' is not registered."
            )

        del self._tools[tool_name]

        logger.info("Unregistered tool: %s", tool_name)

    def get(self, tool_name: str) -> BaseTool:
        """
        Return a registered tool.
        """
        tool = self._tools.get(tool_name)

        if tool is None:
            raise ToolNotFoundError(
                f"Tool '{tool_name}' is not registered."
            )

        return tool

    def exists(self, tool_name: str) -> bool:
        """
        Check whether a tool exists.
        """
        return tool_name in self._tools

    def list_tools(self) -> list[str]:
        """
        Return all registered tool names.
        """
        return sorted(self._tools.keys())

    def clear(self) -> None:
        """
        Remove every registered tool.
        """
        self._tools.clear()

        logger.info("Tool registry cleared.")

    def __len__(self) -> int:
        return len(self._tools)

    def __contains__(self, tool_name: str) -> bool:
        return tool_name in self._tools

    def __repr__(self) -> str:
        return (
            f"ToolRegistry("
            f"tools={self.list_tools()}"
            f")"
        )