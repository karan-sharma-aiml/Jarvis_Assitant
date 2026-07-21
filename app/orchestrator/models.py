"""
Orchestrator Models

Shared models for the orchestration layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.executor.models import ExecutionResult
from app.planner.models import ExecutionPlan


@dataclass(slots=True)
class OrchestratorResult:
    """
    Final result returned by the AI Orchestrator.
    """

    plan: ExecutionPlan

    results: list[ExecutionResult] = field(
        default_factory=list
    )

    success: bool = False

    def add_result(
        self,
        result: ExecutionResult,
    ) -> None:

        self.results.append(result)

    @property
    def total_steps(
        self,
    ) -> int:

        return len(self.results)

    def __repr__(
        self,
    ) -> str:

        return (
            f"OrchestratorResult("
            f"steps={self.total_steps}, "
            f"success={self.success})"
        )