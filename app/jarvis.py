"""
JARVIS AI Assistant

Main application entry point.

Pipeline
--------
User Input
    ↓
Command Parser
    ↓
Intent Detection
    ↓
Multi-Step Planner
    ↓
Executor
    ↓
Conversation
    ↓
Memory
"""

from __future__ import annotations

from app.conversation.conversation_manager import ConversationManager
from app.orchestrator.orchestrator import AIOrchestrator


class Jarvis:
    """
    Main JARVIS application.

    Coordinates the complete AI assistant pipeline.
    """

    def __init__(self) -> None:

        self._conversation = ConversationManager()
        self._orchestrator = AIOrchestrator()

    def process(
        self,
        command: str,
    ):
        """
        Process one user command.
        """

        self._conversation.add_user_message(
            command
        )

        result = self._orchestrator.run(
            command
        )

        if result.success:

            reply = (
                f"Successfully executed "
                f"{result.total_steps} step(s)."
            )

        else:

            reply = (
                "Unable to execute the request."
            )

        self._conversation.add_assistant_message(
            reply
        )

        return result

    def conversation(self):

        return self._conversation.context

    def health_check(self) -> bool:

        return (
            self._conversation.health_check()
            and self._orchestrator.health_check()
        )

    def __repr__(self) -> str:

        return (
            "Jarvis()"
        )