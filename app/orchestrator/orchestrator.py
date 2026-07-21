"""
AI Orchestrator

Coordinates the complete JARVIS execution pipeline.

Pipeline
--------
User Command
      ↓
CommandParser
      ↓
IntentDetector
      ↓
MultiStepPlanner
      ↓
Executor
      ↓
Execution Results
"""

from __future__ import annotations

from app.intent.detector import IntentDetector
from app.executor.executor import Executor
from app.executor.models import ExecutionRequest
from app.orchestrator.models import OrchestratorResult
from app.planner.models import ExecutionPlan
from app.planner.multi_step_planner import MultiStepPlanner
from app.planner.parser import CommandParser


class AIOrchestrator:
    """
    Coordinates the complete AI pipeline.
    """

    def __init__(self) -> None:

        self._parser = CommandParser()
        self._detector = IntentDetector()
        self._planner = MultiStepPlanner()
        self._executor = Executor()

    def run(
        self,
        command: str,
    ) -> OrchestratorResult:
        """
        Execute a complete user command.
        """

        commands = self._parser.parse(command)

        intents = []

        for text in commands:

            intent = self._detector.detect(text)

            intents.append(intent)

        plan: ExecutionPlan = self._planner.create_plan(intents)

        result = OrchestratorResult(
            plan=plan,
        )

        if plan.is_empty:

            return result

        success = True

        for step in plan.steps:

            execution = self._executor.execute(
                ExecutionRequest(
                    intent=step.intent,
                    route=step.route,
                    arguments=step.intent.entities,
                )
            )

            result.add_result(execution)

            if not execution.success:
                success = False

        result.success = success

        return result

    def health_check(
        self,
    ) -> bool:

        return (
            self._parser.health_check()
            and self._detector.health_check()
            and self._planner.health_check()
            and self._executor.health_check()
        )

    def __repr__(
        self,
    ) -> str:

        return "AIOrchestrator()"
