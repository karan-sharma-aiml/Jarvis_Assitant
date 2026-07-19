"""Tool exceptions used by the tool-calling engine.

This module provides a small, stable exception hierarchy for tools. All
exceptions inherit from :class:`ToolError`, which itself subclasses
``app.core.exceptions.JarvisError`` to integrate with the application's
top-level error handling.

Design goals:
- Keep the hierarchy simple and flat so callers can catch broad or fine-
  grained errors as needed.
- Preserve backward compatibility for existing raise sites.
- Add lightweight, optional ``details`` storage to improve diagnostics
  without introducing business logic.
"""

from __future__ import annotations

from typing import Any, Optional

from app.core.exceptions import JarvisError

__all__ = [
    "ToolError",
    "ToolValidationError",
    "ToolExecutionError",
    "ToolUnavailableError",
    "ToolNotFoundError",
    "ToolRegistrationError",
    "ToolPermissionError",
]


class ToolError(JarvisError):
    """Base exception for the Tool Engine.

    Parameters
    - ``message``: optional human-readable message (kept positional for
      backward compatibility)
    - ``details``: optional mapping with additional diagnostic data (keyword-only)

    The class purposefully does not implement business logic. It provides a
    small extension point (``details``) so callers and logging can include
    structured context alongside the exception message.
    """

    __slots__ = ("details",)

    def __init__(self, message: Optional[str] = None, *, details: Optional[dict[str, Any]] = None) -> None:
        super().__init__(message)
        # Store extra diagnostic context; may be None.
        self.details = details

    def __repr__(self) -> str:  # pragma: no cover - trivial
        msg = super().__str__() or self.__class__.__name__
        return f"{self.__class__.__name__}({msg!r}, details={self.details!r})"


class ToolValidationError(ToolError):
    """Raised when tool input validation fails.

    Examples: missing required argument, wrong argument type, or format errors.
    """


class ToolExecutionError(ToolError):
    """Raised when a tool fails during execution.

    Use this for runtime failures inside the tool implementation; the
    exception may include ``details`` describing internal state useful for
    debugging.
    """


class ToolUnavailableError(ToolError):
    """Raised when a tool exists but is currently unavailable.

    Typical causes (examples, not exhaustive): missing API key, transient
    network problems, or missing optional dependency.
    """


class ToolNotFoundError(ToolError):
    """Raised when the requested tool is not registered or cannot be found."""


class ToolRegistrationError(ToolError):
    """Raised when tool registration or discovery fails."""


class ToolPermissionError(ToolError):
    """Raised when a tool cannot be executed due to insufficient permissions.

    This can be used by policy checks or OS-level permission checks. The
    exception is security-related; handlers may treat it differently from
    other operational errors.
    """