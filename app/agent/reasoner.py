"""
JARVIS Reasoner

Responsible for deciding the next action
based on the current AgentState.

Responsibilities:
- Analyze current state
- Select next plan step
- Record reasoning
- Update AgentState

Contains NO tool execution.
Contains NO memory retrieval.
Contains NO LLM calls.
"""

from __future__ import annotations

import logging
import re

from app.agent.agent_state import AgentState

logger = logging.getLogger(__name__)


class Reasoner:
    """
    Rule-based reasoning engine.

    Future:
    - LLM Reasoner
    - Chain-of-Thought
    - Tree-of-Thought
    - Reflection-based Reasoner
    """

    def reason(self, state: AgentState) -> AgentState:
        """
        Determine the next action.
        """

        logger.info("Reasoner started", extra={"phase": "reasoner", "event": "reasoner_started"})

        if not state.success:
            return state

        if state.current_step >= len(state.plan):
            state.error = "No remaining execution steps."
            state.success = False
            logger.error("Agent failed", extra={"phase": "reasoner", "event": "agent_failed", "error": state.error})
            return state

        step = state.plan[state.current_step]
        selected_tool = self._select_tool(step, state)

        state.selected_tool = selected_tool
        state.tool_arguments = self._build_tool_arguments(step, state)
        state.current_step += 1

        state.thoughts.append(
            f"Reasoner selected step: {step}"
        )

        state.metadata["current_action"] = step
        state.metadata["selected_tool"] = selected_tool

        logger.info(
            "Reasoner selected action",
            extra={
                "phase": "reasoner",
                "event": "reasoner_selected_action",
                "action": step,
                "selected_tool": selected_tool,
            },
        )

        return state

    def _select_tool(self, step: str, state: AgentState) -> str | None:
        """
        Map a plan step to a deterministic executable tool.
        """

        if state.selected_tool:
            return state.selected_tool

        step_text = step.lower()

        if "weather" in step_text:
            return "weather"

        if "calculator" in step_text or "math" in step_text:
            return "calculator"

        if "search" in step_text or "google" in step_text or "find" in step_text:
            return "search"

        if "email" in step_text:
            return "email"

        if "calendar" in step_text or "meeting" in step_text or "event" in step_text:
            return "calendar"

        return None

    def _build_tool_arguments(self, step: str, state: AgentState) -> dict[str, object]:
        """
        Populate tool arguments only when they can be determined deterministically.
        """

        if state.tool_arguments:
            return dict(state.tool_arguments)

        if state.selected_tool:
            if state.selected_tool == "weather":
                return self._extract_weather_arguments(state.user_input)
            if state.selected_tool == "calculator":
                return self._extract_calculator_arguments(state.user_input)

        step_text = step.lower()
        if "calculator" in step_text:
            return self._extract_calculator_arguments(state.user_input)
        if "weather" in step_text:
            return self._extract_weather_arguments(state.user_input)

        return {}

    def _extract_weather_arguments(self, query: str) -> dict[str, object]:
        """
        Extract weather coordinates from a simple natural language query when present.
        """

        match = re.search(r"latitude\s*=\s*([-+]?\d*\.?\d+)", query, re.IGNORECASE)
        if match:
            latitude = float(match.group(1))
        else:
            return {}

        match = re.search(r"longitude\s*=\s*([-+]?\d*\.?\d+)", query, re.IGNORECASE)
        if match:
            longitude = float(match.group(1))
            return {"latitude": latitude, "longitude": longitude}

        return {}

    def _extract_calculator_arguments(self, query: str) -> dict[str, object]:
        """
        Extract a simple calculator expression from the query when possible.
        """

        text = query.strip()
        if not text:
            return {}

        expression = re.sub(r"^(?:calculate|calc)\s*", "", text, flags=re.IGNORECASE).strip()
        if not expression:
            return {}

        if re.fullmatch(r"[\d\.\s\+\-\*/\(\)]+", expression):
            return {"expression": expression}

        return {}