"""
JARVIS Calendar Tool

Simple local calendar tool.

Responsibilities:
- Create event
- List events
- Get event
- Update event
- Delete event

Stores events in memory.

Future:
- Google Calendar
- Outlook Calendar
- Apple Calendar
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

from app.tools.base import BaseTool
from app.tools.exceptions import (
    ToolExecutionError,
    ToolValidationError,
)
from app.tools.models import ToolCategory


class CalendarTool(BaseTool):
    """
    Calendar Tool.
    """

    def __init__(self) -> None:
        self._events: dict[str, dict[str, Any]] = {}

    @property
    def name(self) -> str:
        return "calendar"

    @property
    def description(self) -> str:
        return "Manage calendar events."

    @property
    def category(self) -> ToolCategory:
        return ToolCategory.PRODUCTIVITY

    def validate(self, **kwargs: Any) -> None:

        operation = kwargs.get("operation")

        allowed = {
            "create",
            "list",
            "get",
            "update",
            "delete",
        }

        if operation not in allowed:
            raise ToolValidationError(
                f"Unsupported operation: {operation}"
            )

    def execute(self, **kwargs: Any):

        self.validate(**kwargs)

        operation = kwargs["operation"]

        if operation == "create":

            title = kwargs.get("title")

            event_time = kwargs.get("time")

            if not title:
                raise ToolValidationError(
                    "Missing title."
                )

            if not event_time:
                raise ToolValidationError(
                    "Missing time."
                )

            event_id = str(uuid4())

            self._events[event_id] = {
                "id": event_id,
                "title": title,
                "time": event_time,
                "created": datetime.now().isoformat(),
            }

            return event_id

        if operation == "list":

            return list(self._events.values())

        if operation == "get":

            event_id = kwargs["id"]

            if event_id not in self._events:
                raise ToolExecutionError(
                    "Event not found."
                )

            return self._events[event_id]

        if operation == "update":

            event_id = kwargs["id"]

            if event_id not in self._events:
                raise ToolExecutionError(
                    "Event not found."
                )

            if "title" in kwargs:
                self._events[event_id]["title"] = kwargs["title"]

            if "time" in kwargs:
                self._events[event_id]["time"] = kwargs["time"]

            return self._events[event_id]

        if operation == "delete":

            event_id = kwargs["id"]

            if event_id not in self._events:
                raise ToolExecutionError(
                    "Event not found."
                )

            del self._events[event_id]

            return "Event deleted."

        raise ToolValidationError(
            "Unknown operation."
        )