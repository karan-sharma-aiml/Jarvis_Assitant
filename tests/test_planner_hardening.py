from app.planner.models import ExecutionPlan, PlanStatus, PlanStep
from app.planner.multi_step_planner import MultiStepPlanner
from app.planner.parser import CommandParser
from app.planner.planner import Planner
from app.planner.registry import PlannerRegistry
from app.intent.models import Intent, IntentName, IntentSource
from app.router.models import ToolRoute


def test_command_parser_handles_invalid_input() -> None:
    parser = CommandParser()
    assert parser.parse(None) == []  # type: ignore[arg-type]
    assert parser.parse("") == []
    assert parser.parse("   ") == []


def test_planner_registry_rejects_invalid_names() -> None:
    registry = PlannerRegistry()
    try:
        registry.register("", Planner())
    except ValueError as exc:
        assert "empty" in str(exc).lower()
    else:
        raise AssertionError("Expected ValueError")


def test_multi_step_planner_handles_unknown_intents() -> None:
    planner = MultiStepPlanner()
    plan = planner.create_plan([Intent.unknown("hi")])
    assert plan.status is PlanStatus.FAILED
    assert plan.is_empty


def test_planner_handles_invalid_intent() -> None:
    planner = Planner()
    result = planner.create_plan(None)  # type: ignore[arg-type]
    assert isinstance(result, ExecutionPlan)
    assert result.status is PlanStatus.FAILED
