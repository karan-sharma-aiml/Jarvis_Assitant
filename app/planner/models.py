"""
Planner Models

Defines the models used by the planning layer.

Responsibilities
----------------
- Represent a single plan step.
- Represent a complete execution plan.
- Represent planning status.

Contains NO planning logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from app.intent.models import Intent
from app.router.models import ToolRoute


class PlanStatus(str, Enum):
    """Status of a generated execution plan."""

    READY = "ready"
    FAILED = "failed"
    PARTIAL = "partial"


@dataclass(slots=True)
class PlanStep:
    """Represents one executable step."""

    step_number: int

    intent: Intent | None = None

    route: ToolRoute | None = None

    description: str = ""

    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Normalize optional values so the step remains safe to serialize."""
        if self.intent is None:
            self.intent = Intent.unknown("")

        if self.route is None:
            self.route = ToolRoute(manager="", method="")

        if self.description is None:
            self.description = ""

        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> dict[str, object]:
        """Convert the plan step into a serializable dictionary."""
        return {
            "step_number": self.step_number,
            "intent": self.intent.to_dict() if self.intent is not None else {},
            "route": self.route.to_dict() if self.route is not None else {},
            "description": self.description,
            "metadata": self.metadata,
        }

    def __repr__(self) -> str:
        intent_name = self.intent.name.value if self.intent is not None else "unknown"
        manager_name = self.route.manager if self.route is not None else ""
        return f"PlanStep(step={self.step_number}, intent={intent_name}, manager={manager_name})"


@dataclass(slots=True)
class ExecutionPlan:
    """Represents the complete execution plan."""

    status: PlanStatus = PlanStatus.READY

    steps: list[PlanStep] = field(default_factory=list)

    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Normalize optional values so the plan remains safe to use."""
        if self.metadata is None:
            self.metadata = {}

        if self.steps is None:
            self.steps = []

    @property
    def total_steps(self) -> int:
        """Return the number of steps in the plan."""
        return len(self.steps)

    @property
    def is_empty(self) -> bool:
        """Return True when no steps are present."""
        return not self.steps

    def add_step(self, step: PlanStep) -> None:
        """Append one step to the plan."""
        self.steps.append(step)

    def clear(self) -> None:
        """Remove all steps from the plan."""
        self.steps.clear()

    def to_dict(self) -> dict[str, object]:
        """Convert the plan into a serializable dictionary."""
        return {
            "status": self.status.value,
            "steps": [step.to_dict() for step in self.steps],
            "metadata": self.metadata,
        }

    def __repr__(self) -> str:
        return f"ExecutionPlan(status={self.status.value}, steps={self.total_steps})"