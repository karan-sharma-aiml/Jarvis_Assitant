"""
Executor

Executes a ToolRoute using the appropriate manager.

Responsibilities
----------------
- Resolve manager instances.
- Validate routes.
- Invoke manager methods.
- Return ExecutionResult.

Contains NO intent detection logic.
"""

from __future__ import annotations

import logging

from app.executor.models import (
    ExecutionRequest,
    ExecutionResult,
    ExecutionStatus,
)
from app.executor.registry import ManagerRegistry

logger = logging.getLogger(__name__)


class Executor:
    """Executes routed actions."""

    def __init__(self, registry: ManagerRegistry | None = None) -> None:
        self._registry = registry if registry is not None else ManagerRegistry()

    def execute(self, request: ExecutionRequest | None) -> ExecutionResult:
        """Execute one request and return a structured execution result."""
        if not isinstance(request, ExecutionRequest):
            logger.warning("Received invalid execution request %r", request)
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message="Invalid execution request.",
                manager="",
                method="",
            )

        route = request.route
        if route is None:
            logger.warning("Execution request %r is missing a route", request)
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message="Execution request is missing a route.",
                manager="",
                method="",
            )

        manager_name = getattr(route, "manager", None)
        if not isinstance(manager_name, str) or not manager_name.strip():
            logger.warning("Execution request %r has an invalid manager name", request)
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message="Execution request has an invalid manager name.",
                manager="",
                method=getattr(route, "method", ""),
            )

        method_name = getattr(route, "method", None)
        if not isinstance(method_name, str) or not method_name.strip():
            logger.warning("Execution request %r has an invalid method name", request)
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message="Execution request has an invalid method name.",
                manager=manager_name,
                method="",
            )

        manager = self._registry.get(manager_name)
        if manager is None:
            logger.warning("Unknown manager '%s' for route %r", manager_name, route)
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message=f"Unknown manager: {manager_name}",
                manager=manager_name,
                method=method_name,
            )

        method = getattr(manager, method_name, None)
        if not callable(method):
            logger.warning(
                "Manager '%s' does not expose a callable method '%s'",
                manager_name,
                method_name,
            )
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message=f"Method '{method_name}' not found.",
                manager=manager_name,
                method=method_name,
            )

        try:
            result = method(**request.arguments)
            logger.debug(
                "Execution succeeded for manager='%s' method='%s'",
                manager_name,
                method_name,
            )
            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                message="Execution successful.",
                manager=manager_name,
                method=method_name,
                data={"result": result},
            )
        except TypeError as exc:
            logger.warning(
                "Execution argument mismatch for manager='%s' method='%s': %s",
                manager_name,
                method_name,
                exc,
            )
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message=f"Invalid arguments for method '{method_name}': {exc}",
                manager=manager_name,
                method=method_name,
            )
        except Exception as exc:  # pragma: no cover - defensive logging path
            logger.exception(
                "Execution failed for manager='%s' method='%s'",
                manager_name,
                method_name,
            )
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message=str(exc),
                manager=manager_name,
                method=method_name,
            )

    def health_check(self) -> bool:
        """Return True when the executor has a healthy registry."""
        return self._registry.health_check()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(registry={self._registry.count()})"
