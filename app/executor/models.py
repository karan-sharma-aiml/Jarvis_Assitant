"""
Executor Models

Shared models for the execution layer.

Responsibilities
----------------
- Represent an execution request.
- Represent an execution result.

Contains NO execution logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from app.intent.models import Intent
from app.router.models import ToolRoute


class ExecutionStatus(str, Enum):
    """Execution status for a routed action."""

    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass(slots=True)
class ExecutionRequest:
    """Represents one execution request."""

    intent: Intent | None = None

    route: ToolRoute | None = None

    arguments: dict[str, object] = field(default_factory=dict)

    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Normalize optional values so downstream execution remains safe."""
        if self.intent is None:
            self.intent = Intent.unknown("")

        if self.route is None:
            self.route = ToolRoute(manager="", method="")

        if self.arguments is None:
            self.arguments = {}

        if self.metadata is None:
            self.metadata = {}

    def has_argument(self, key: str) -> bool:
        """Return True when the request carries the requested argument."""
        return key in self.arguments

    def get_argument(
        self,
        key: str,
        default: object | None = None,
    ) -> object | None:
        """Return one argument value or a default."""
        return self.arguments.get(key, default)

    def to_dict(self) -> dict[str, object]:
        """Convert the request into a serializable dictionary."""
        return {
            "intent": self.intent.to_dict() if self.intent is not None else {},
            "route": self.route.to_dict() if self.route is not None else {},
            "arguments": self.arguments,
            "metadata": self.metadata,
        }


@dataclass(slots=True)
class ExecutionResult:
    """Result returned by the Executor."""

    status: ExecutionStatus | None = None

    message: str = ""

    manager: str = ""

    method: str = ""

    data: dict[str, object] = field(default_factory=dict)

    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Normalize values so the result always remains usable."""
        if self.status is None:
            self.status = ExecutionStatus.FAILED

        if self.message is None:
            self.message = ""

        if self.manager is None:
            self.manager = ""

        if self.method is None:
            self.method = ""

        if self.data is None:
            self.data = {}

        if self.metadata is None:
            self.metadata = {}

        self.message = str(self.message)
        self.manager = str(self.manager)
        self.method = str(self.method)

    @property
    def success(self) -> bool:
        """Return True when the execution succeeded."""
        return self.status is ExecutionStatus.SUCCESS

    @property
    def failed(self) -> bool:
        """Return True when the execution failed."""
        return self.status is ExecutionStatus.FAILED

    def to_dict(self) -> dict[str, object]:
        """Convert the result into a serializable dictionary."""
        return {
            "status": self.status.value if self.status is not None else ExecutionStatus.FAILED.value,
            "message": self.message,
            "manager": self.manager,
            "method": self.method,
            "data": self.data,
            "metadata": self.metadata,
        }

    def __str__(self) -> str:
        """Return a compact string representation."""
        return (
            "ExecutionResult("
            f"status={self.status.value if self.status is not None else ExecutionStatus.FAILED.value}, "
            f"manager={self.manager}, "
            f"method={self.method})"
        )

    def __repr__(self) -> str:
        return self.__str__()
