"""
JARVIS Executor

Executes the action selected by the Reasoner.

Responsibilities:
- Execute tool calls
- Store execution results
- Update AgentState

Contains NO planning.
Contains NO reasoning.
Contains NO LLM calls.
Contains NO memory retrieval.
"""

from __future__ import annotations

import logging

from app.agent.agent_state import AgentState
from app.tools.manager import ToolManager

logger = logging.getLogger(__name__)


class Executor:
    """
    Executes the current action.
    """

    def __init__(self, tool_manager: ToolManager) -> None:
        self._tool_manager = tool_manager

    def execute(self, state: AgentState) -> AgentState:
        """
        Execute the selected tool.
        """

        logger.info("Executor started", extra={"phase": "executor", "event": "executor_started"})

        if not state.success:
            return state

        tool_name = state.selected_tool

        if tool_name is None:
            state.error = "No tool selected."
            state.success = False
            logger.error("Agent failed", extra={"phase": "executor", "event": "agent_failed", "error": state.error})
            return state

        try:
            result = self._tool_manager.execute(
                tool_name,
                **state.tool_arguments,
            )

            state.tool_result = result
            state.metadata["execution_status"] = "success"

        except Exception as error:
            state.tool_result = None
            state.error = str(error)
            state.success = False
            state.metadata["execution_status"] = "failed"
            logger.error("Agent failed", extra={"phase": "executor", "event": "agent_failed", "error": str(error)})

        logger.info(
            "Executor finished",
            extra={
                "phase": "executor",
                "event": "executor_finished",
                "status": state.metadata.get("execution_status"),
            },
        )

        return state