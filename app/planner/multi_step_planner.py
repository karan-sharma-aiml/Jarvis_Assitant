"""
Multi-Step Planner

Builds an execution plan containing multiple sequential steps.

Responsibilities
----------------
- Convert multiple intents into one ExecutionPlan.
- Preserve execution order.
- Skip unknown intents.
- Does NOT execute anything.
"""

from __future__ import annotations

from collections.abc import Iterable

from app.intent.models import Intent
from app.planner.models import ExecutionPlan, PlanStatus, PlanStep
from app.router.tool_router import ToolRouter


class MultiStepPlanner:
    """Builds execution plans containing multiple steps."""

    def __init__(self, router: ToolRouter | None = None) -> None:
        self._router = router if router is not None else ToolRouter()

    def create_plan(self, intents: Iterable[Intent] | None) -> ExecutionPlan:
        """Convert multiple intents into one execution plan."""
        plan = ExecutionPlan()
        if not intents:
            plan.status = PlanStatus.FAILED
            return plan

        step_number = 1
        for intent in intents:
            if not isinstance(intent, Intent):
                continue

            if intent.is_unknown:
                continue

            route = self._router.route(intent)
            if route is None:
                continue

            plan.add_step(
                PlanStep(
                    step_number=step_number,
                    intent=intent,
                    route=route,
                    description=f"Execute {intent.name.value}",
                )
            )
            step_number += 1

        if plan.is_empty:
            plan.status = PlanStatus.FAILED

        return plan

    def health_check(self) -> bool:
        """Return True when the planner is healthy."""
        return self._router.health_check()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(routes={self._router.route_count()})"