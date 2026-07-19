"""
JARVIS Observer

Observes the result produced by the Executor.

Responsibilities:
- Inspect execution result
- Determine success/failure
- Record observations
- Update AgentState

Contains NO planning.
Contains NO reasoning.
Contains NO execution.
"""

from __future__ import annotations

import logging

from app.agent.agent_state import AgentState
from app.tools.models import ToolExecutionStatus, ToolResponse

logger = logging.getLogger(__name__)


class Observer:
    """
    Observes execution results.
    """

    def observe(self, state: AgentState) -> AgentState:

        result = state.tool_result

        if result is None:
            state.success = False
            state.error = "No execution result available."
            state.metadata["observation"] = "missing_result"
            logger.info("Observer finished", extra={"phase": "observer", "event": "observer_finished", "observation": "missing_result"})
            return state

        if not isinstance(result, ToolResponse):
            state.success = False
            state.error = "Invalid execution result."
            state.metadata["observation"] = "invalid_result"
            logger.info("Observer finished", extra={"phase": "observer", "event": "observer_finished", "observation": "invalid_result"})
            return state

        if result.status == ToolExecutionStatus.SUCCESS:
            state.success = True
            state.error = None
            state.metadata["observation"] = "success"
            state.thoughts.append(
                f"Tool '{result.tool_name}' executed successfully."
            )

        elif result.status == ToolExecutionStatus.UNAVAILABLE:
            state.success = False
            state.error = result.error
            state.metadata["observation"] = "tool_unavailable"
            state.thoughts.append(
                f"Tool '{result.tool_name}' is unavailable."
            )

        else:
            state.success = False
            state.error = result.error
            state.metadata["observation"] = "execution_failed"
            state.thoughts.append(
                f"Tool '{result.tool_name}' execution failed."
            )

        logger.info("Observer finished", extra={"phase": "observer", "event": "observer_finished", "observation": state.metadata.get("observation")})
        return state