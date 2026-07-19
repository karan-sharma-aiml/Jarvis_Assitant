"""
JARVIS Tool Manager

Central manager for all JARVIS tools.

Responsibilities:
- Register tools
- Execute tools
- Check availability
- List available tools

Contains NO tool-specific business logic.
"""

from __future__ import annotations

import logging
from typing import Any

from app.tools.base import BaseTool
from app.tools.exceptions import (
    ToolExecutionError,
    ToolNotFoundError,
)
from app.tools.models import (
    ToolExecutionStatus,
    ToolResponse,
)
from app.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)


class ToolManager:
    """
    Central manager for all JARVIS tools.
    """

    def __init__(self, registry: ToolRegistry | None = None) -> None:
        self._registry = registry or ToolRegistry()

    @property
    def registry(self) -> ToolRegistry:
        """
        Read-only access to the registry.
        """
        return self._registry

    def register_tool(self, tool: BaseTool) -> None:
        """
        Register a tool.
        """
        self._registry.register(tool)

    def unregister_tool(self, tool_name: str) -> None:
        """
        Remove a registered tool.
        """
        self._registry.unregister(tool_name)

    def list_tools(self) -> list[str]:
        """
        Return all registered tool names.
        """
        return self._registry.list_tools()

    def execute(
        self,
        tool_name: str,
        **kwargs: Any,
    ) -> ToolResponse:
        """
        Execute a registered tool.

        Returns:
            ToolResponse
        """

        tool = self._registry.get(tool_name)

        available, reason = tool.availability()

        if not available:
            return ToolResponse(
                tool_name=tool.name,
                status=ToolExecutionStatus.UNAVAILABLE,
                error=reason,
            )

        try:
            tool.validate(**kwargs)

            result = tool.execute(**kwargs)

            logger.info(
                "Tool executed successfully: %s",
                tool.name,
            )

            return ToolResponse(
                tool_name=tool.name,
                status=ToolExecutionStatus.SUCCESS,
                output=result,
            )

        except Exception as error:
            logger.exception(
                "Tool execution failed: %s",
                tool.name,
            )

            return ToolResponse(
                tool_name=tool.name,
                status=ToolExecutionStatus.FAILED,
                error=str(error),
            )

    def exists(
        self,
        tool_name: str,
    ) -> bool:
        """
        Check whether a tool exists.
        """
        return self._registry.exists(tool_name)

    def get_tool(
        self,
        tool_name: str,
    ) -> BaseTool:
        """
        Return a registered tool.
        """
        return self._registry.get(tool_name)

    def clear(self) -> None:
        """
        Remove every registered tool.
        """
        self._registry.clear()

    def health_check(self) -> bool:
        """
        Verify Tool Manager health.
        """
        try:
            _ = len(self._registry)
            return True
        except Exception:
            logger.exception(
                "Tool Manager health check failed."
            )
            return False

    def __len__(self) -> int:
        return len(self._registry)

    def __repr__(self) -> str:
        return (
            f"ToolManager("
            f"tools={self.list_tools()}"
            f")"
        )