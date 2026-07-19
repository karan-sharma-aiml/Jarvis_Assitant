"""
JARVIS Agent

Main orchestrator for the Agent Engine.

Responsibilities
----------------
- Coordinate all agent components
- Execute one reasoning cycle
- Return final AgentState

Contains NO planning logic.
Contains NO reasoning logic.
Contains NO tool logic.
"""

from __future__ import annotations

import logging

from app.agent.agent_state import AgentState
from app.agent.executor import Executor
from app.agent.observer import Observer
from app.agent.planner import Planner
from app.agent.reasoner import Reasoner
from app.agent.reflection import Reflection

logger = logging.getLogger(__name__)


class Agent:
    """
    Main AI Agent.
    """

    def __init__(
        self,
        planner: Planner,
        reasoner: Reasoner,
        executor: Executor,
        observer: Observer,
        reflection: Reflection,
    ) -> None:

        self._planner = planner
        self._reasoner = reasoner
        self._executor = executor
        self._observer = observer
        self._reflection = reflection

    def run(
        self,
        user_input: str,
        *,
        selected_tool: str | None = None,
        tool_arguments: dict | None = None,
    ) -> AgentState:
        """
        Execute one complete agent cycle.
        """

        state = AgentState()

        state.user_input = user_input
        state.selected_tool = selected_tool
        state.tool_arguments = tool_arguments or {}

        if not self._run_phase(state, "planner", self._planner.create_plan):
            return state

        if not self._run_phase(state, "reasoner", self._reasoner.reason):
            return state

        if not self._run_phase(state, "executor", self._executor.execute):
            return state

        if not self._run_phase(state, "observer", self._observer.observe):
            return state

        if not self._run_phase(state, "reflection", self._reflection.reflect):
            return state

        logger.info("Workflow completed", extra={"phase": "workflow", "event": "workflow_completed"})
        return state

    def _run_phase(
        self,
        state: AgentState,
        phase_name: str,
        phase_handler,
    ) -> bool:
        """
        Execute one pipeline phase while preserving state on failure.
        """

        logger.info(f"{phase_name.capitalize()} started", extra={"phase": phase_name, "event": f"{phase_name}_started"})

        try:
            phase_handler(state)
        except Exception as error:
            state.success = False
            state.error = f"{phase_name.capitalize()} failed: {error}"
            state.metadata["phase_error"] = phase_name
            state.metadata["phase_error_message"] = str(error)
            logger.error("Agent failed", extra={"phase": phase_name, "event": "agent_failed", "error": str(error)})
            return False

        if not state.success:
            state.metadata["phase_error"] = phase_name
            logger.error("Agent failed", extra={"phase": phase_name, "event": "agent_failed", "error": state.error or "phase failed"})
            return False

        logger.info(f"{phase_name.capitalize()} finished", extra={"phase": phase_name, "event": f"{phase_name}_finished"})
        return True