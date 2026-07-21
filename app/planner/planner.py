"""
Planner

Converts an Intent into an ExecutionPlan.

Responsibilities
----------------
- Validate intent.
- Route intent.
- Build execution plan.

Contains NO execution logic.
"""

from __future__ import annotations

from app.intent.models import Intent
from app.planner.models import ExecutionPlan, PlanStatus, PlanStep
from app.router.tool_router import ToolRouter


class Planner:
    """Creates execution plans from a single intent."""

    def __init__(self, router: ToolRouter | None = None) -> None:
        self._router = router if router is not None else ToolRouter()

    def create_plan(self, intent: Intent | None) -> ExecutionPlan:
        """Convert an Intent into an ExecutionPlan."""
        plan = ExecutionPlan()

        if not isinstance(intent, Intent):
            plan.status = PlanStatus.FAILED
            return plan

        if intent.is_unknown:
            plan.status = PlanStatus.FAILED
            return plan

        route = self._router.route(intent)
        if route is None:
            plan.status = PlanStatus.FAILED
            return plan

        step = PlanStep(
            step_number=1,
            intent=intent,
            route=route,
            description=f"Execute {intent.name.value}",
        )
        plan.add_step(step)
        return plan

    def can_plan(self, intent: Intent | None) -> bool:
        """Return True when the planner can build a plan for the provided intent."""
        if not isinstance(intent, Intent):
            return False

        if intent.is_unknown:
            return False

        return self._router.can_route(intent)

    def health_check(self) -> bool:
        """Return True when the planner is healthy."""
        return self._router.health_check()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(routes={self._router.route_count()})"