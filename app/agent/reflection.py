"""
JARVIS Reflection Engine

Evaluates the outcome of an executed action.

Responsibilities
---------------
- Evaluate execution outcome
- Decide next action
- Record reflection
- Update AgentState

Contains NO planning.
Contains NO execution.
Contains NO tool selection.
Contains NO LLM calls.
"""

from __future__ import annotations

import logging

from app.agent.agent_state import AgentState

logger = logging.getLogger(__name__)


class Reflection:
    """
    Reflection engine for the agent.
    """

    def reflect(self, state: AgentState) -> AgentState:
        """
        Reflect on the execution result.
        """

        observation = state.metadata.get("observation")

        if observation == "success":
            state.metadata["reflection"] = "continue"
            state.thoughts.append(
                "Reflection: execution succeeded. Continue workflow."
            )
            logger.info("Reflection finished", extra={"phase": "reflection", "event": "reflection_finished", "reflection": "continue"})
            return state

        if observation == "tool_unavailable":
            state.metadata["reflection"] = "retry"
            state.thoughts.append(
                "Reflection: tool unavailable. Retry may be required."
            )
            logger.info("Reflection finished", extra={"phase": "reflection", "event": "reflection_finished", "reflection": "retry"})
            return state

        if observation == "missing_result":
            state.metadata["reflection"] = "retry"
            state.thoughts.append(
                "Reflection: execution returned no result."
            )
            logger.info("Reflection finished", extra={"phase": "reflection", "event": "reflection_finished", "reflection": "retry"})
            return state

        if observation == "invalid_result":
            state.metadata["reflection"] = "investigate"
            state.thoughts.append(
                "Reflection: invalid tool response detected."
            )
            logger.info("Reflection finished", extra={"phase": "reflection", "event": "reflection_finished", "reflection": "investigate"})
            return state

        if observation == "execution_failed":
            state.metadata["reflection"] = "ask_user"
            state.thoughts.append(
                "Reflection: execution failed. User clarification may be required."
            )
            logger.info("Reflection finished", extra={"phase": "reflection", "event": "reflection_finished", "reflection": "ask_user"})
            return state

        state.metadata["reflection"] = "unknown"
        state.thoughts.append(
            "Reflection: unable to determine next action."
        )
        logger.info("Reflection finished", extra={"phase": "reflection", "event": "reflection_finished", "reflection": "unknown"})
        return state