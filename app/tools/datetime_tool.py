"""
JARVIS DateTime Tool

Provides current date and time information.

Responsibilities:
- Current date
- Current time
- Current datetime
- Current weekday
- Current month
- Current year

Contains NO business logic.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.tools.base import BaseTool
from app.tools.exceptions import ToolValidationError
from app.tools.models import ToolCategory


class DateTimeTool(BaseTool):
    """
    Tool for retrieving current date and time information.
    """

    @property
    def name(self) -> str:
        return "datetime"

    @property
    def description(self) -> str:
        return "Returns current date and time."

    @property
    def category(self) -> ToolCategory:
        return ToolCategory.UTILITY

    def validate(self, **kwargs: Any) -> None:
        operation = kwargs.get("operation", "datetime")

        allowed = {
            "datetime",
            "date",
            "time",
            "day",
            "month",
            "year",
        }

        if operation not in allowed:
            raise ToolValidationError(
                f"Unsupported operation: {operation}"
            )

    def execute(self, **kwargs: Any) -> str:
        """
        Execute the requested date/time operation.
        """

        self.validate(**kwargs)

        operation = kwargs.get(
            "operation",
            "datetime",
        )

        now = datetime.now()

        if operation == "datetime":
            return now.strftime("%Y-%m-%d %H:%M:%S")

        if operation == "date":
            return now.strftime("%Y-%m-%d")

        if operation == "time":
            return now.strftime("%H:%M:%S")

        if operation == "day":
            return now.strftime("%A")

        if operation == "month":
            return now.strftime("%B")

        if operation == "year":
            return str(now.year)

        raise ToolValidationError(
            f"Unsupported operation: {operation}"
        )