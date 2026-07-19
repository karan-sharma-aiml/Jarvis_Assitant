"""
JARVIS Workflow

Controls the execution flow of the AI Agent.

Responsibilities
----------------
- Define execution sequence
- Start agent execution
- Return final AgentState

Contains NO planning logic.
Contains NO reasoning logic.
Contains NO execution logic.
"""

from __future__ import annotations

import logging

from app.agent.agent import Agent
from app.agent.agent_state import AgentState

logger = logging.getLogger(__name__)


class Workflow:
    """
    Controls the execution workflow of the agent.
    """

    def __init__(self, agent: Agent) -> None:
        self._agent = agent

    def run(
        self,
        user_input: str,
        *,
        selected_tool: str | None = None,
        tool_arguments: dict | None = None,
    ) -> AgentState:
        """
        Execute one complete workflow.
        """

        state = self._agent.run(
            user_input=user_input,
            selected_tool=selected_tool,
            tool_arguments=tool_arguments,
        )

        logger.info("Workflow completed", extra={"phase": "workflow", "event": "workflow_completed"})
        return state