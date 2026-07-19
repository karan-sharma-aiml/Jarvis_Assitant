"""
JARVIS Agent Manager

Public entry point for the Agent Engine.

Responsibilities
----------------
- Own the Workflow
- Execute agent requests
- Return AgentState

Contains NO planning.
Contains NO reasoning.
Contains NO execution logic.
"""

from __future__ import annotations

from app.agent.agent import Agent
from app.agent.agent_state import AgentState
from app.agent.workflow import Workflow


class AgentManager:
    """
    Public interface for the Agent Engine.
    """

    def __init__(
        self,
        agent: Agent,
    ) -> None:

        self._workflow = Workflow(agent)

    def execute(
        self,
        user_input: str,
        *,
        selected_tool: str | None = None,
        tool_arguments: dict | None = None,
    ) -> AgentState:
        """
        Execute a complete agent request.
        """

        return self._workflow.run(
            user_input=user_input,
            selected_tool=selected_tool,
            tool_arguments=tool_arguments,
        )

    @property
    def workflow(self) -> Workflow:
        """
        Read-only access to the workflow.
        """
        return self._workflow