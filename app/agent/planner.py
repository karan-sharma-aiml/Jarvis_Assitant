"""
JARVIS Planner

Responsible for creating an execution plan
from a user request.

Responsibilities:
- Extract goal
- Create execution plan
- Update AgentState

Contains NO reasoning.
Contains NO tool execution.
Contains NO memory retrieval.
"""

from __future__ import annotations

import logging
from typing import List

from app.agent.agent_state import AgentState

logger = logging.getLogger(__name__)


class Planner:
    """
    Rule-based planner.

    Future:
    - Hybrid Planner
    - LLM Planner
    - Tree-of-Thought Planner
    """

    def create_plan(self, state: AgentState) -> AgentState:
        """
        Generate an execution plan.
        """

        logger.info("Planner started", extra={"phase": "planner", "event": "planner_started"})

        query = state.user_input.strip()

        if not query:
            state.error = "User input is empty."
            state.success = False
            logger.error("Agent failed", extra={"phase": "planner", "event": "agent_failed", "error": state.error})
            return state

        state.goal = self._extract_goal(query)

        state.plan = self._generate_plan(query)

        state.current_step = 0

        state.success = True
        state.error = None

        logger.info("Planner finished", extra={"phase": "planner", "event": "planner_finished"})

        return state

    def _extract_goal(self, query: str) -> str:
        """
        Extract the high-level goal.
        """

        return query

    def _generate_plan(self, query: str) -> List[str]:
        """
        Generate ordered execution steps.
        """

        q = query.lower()

        steps: List[str] = []

        if any(word in q for word in ("weather", "temperature")):
            steps.append("Select Weather Tool")
            steps.append("Execute Weather Tool")
            steps.append("Generate Final Response")

        elif any(word in q for word in ("search", "google", "find")):
            steps.append("Select Search Tool")
            steps.append("Execute Search Tool")
            steps.append("Generate Final Response")

        elif any(word in q for word in ("calculate", "math", "+", "-", "*", "/")):
            steps.append("Select Calculator Tool")
            steps.append("Execute Calculator Tool")
            steps.append("Generate Final Response")

        elif any(word in q for word in ("email", "mail")):
            steps.append("Select Email Tool")
            steps.append("Execute Email Tool")
            steps.append("Generate Final Response")

        elif any(word in q for word in ("meeting", "calendar", "event")):
            steps.append("Select Calendar Tool")
            steps.append("Execute Calendar Tool")
            steps.append("Generate Final Response")

        else:
            steps.append("Retrieve Memory")
            steps.append("Retrieve Knowledge")
            steps.append("Generate Final Response")

        return steps