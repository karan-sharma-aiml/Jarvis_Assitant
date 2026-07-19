"""app.tools.base
===================

Base abstractions for executable tools used by JARVIS.

This module exposes `BaseTool`, the minimal, stable, and beginner-friendly
abstract base class every concrete tool must inherit from. The public API
(`name`, `description`, `is_available`, `validate`, `execute`) is preserved
to maintain backward compatibility.

Design goals:
- Keep the surface area small and explicit.
- Provide clear extension hooks for validation and availability checks.
- Fail fast with a dedicated `ValidationError` when inputs are invalid.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping, Optional, Tuple


class ValidationError(ValueError):
    """Raised when a tool's inputs fail validation.

    Using a distinct exception type (subclassing ``ValueError``) makes it
    straightforward for callers to catch validation failures specifically
    while keeping compatibility with existing code that may catch
    ``Exception`` or ``ValueError``.
    """


class BaseTool(ABC):
    """Abstract base class for JARVIS tools.

    Public API (kept for backward compatibility):
    - ``name``: unique identifier for the tool (property)
    - ``description``: human-friendly description (property)
    - ``is_available() -> bool``: whether the tool can execute now
    - ``validate(**kwargs)``: validate inputs (raise ``ValidationError`` on failure)
    - ``execute(**kwargs) -> Any``: perform the tool action

    Extension hooks (optional):
    - ``availability() -> tuple[bool, Optional[str]]``: returns (available, reason)

    Notes for implementers:
    - Keep ``name`` and ``description`` inexpensive to compute.
    - ``validate`` should raise ``ValidationError`` on invalid input.
    - ``is_available`` remains the simple compatibility method; prefer
      ``availability`` when a diagnostic message is useful.
    """

    # -- Metadata -------------------------------------------------
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the tool's unique name.

        Must be a short identifier (no spaces) suitable for logging and lookups.
        """

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a concise, human-readable description of the tool."""

    # -- Enablement / availability --------------------------------
    @property
    def enabled(self) -> bool:
        """Whether the tool is enabled.

        Override to provide dynamic enable/disable behavior. Default is ``True``
        for backward compatibility with existing implementations.
        """

        return True

    def availability(self) -> Tuple[bool, Optional[str]]:
        """Return a tuple ``(available, reason)`` describing availability.

        The default implementation simply reflects ``enabled``. Subclasses can
        override this method to perform lightweight checks (network, API key,
        configuration) and provide an explanatory reason for unavailability.
        """

        if not self.enabled:
            return False, "tool is disabled"
        return True, None

    def is_available(self) -> bool:
        """Backward-compatible availability check.

        Calls :meth:`availability` and returns only the boolean part. Keep using
        this method when callers only need a boolean.
        """

        return self.availability()[0]

    # -- Validation -------------------------------------------------
    def validate(self, **kwargs: Any) -> None:
        """Validate inputs for :meth:`execute`.

        Raise ``ValidationError`` when inputs are invalid. The default
        implementation performs no validation which keeps behavior compatible
        with existing tools. Prefer raising over returning error values so
        callers fail fast and error handling is explicit.

        Example override::

            def validate(self, **kwargs):
                if "path" not in kwargs:
                    raise ValidationError("'path' is required")
        """

        return None

    def validate_with_messages(self, **kwargs: Any) -> list[str]:
        """Optional helper: return a list of validation error messages.

        The default implementation returns an empty list. Implementers may
        override this to provide non-exception-based validation diagnostics.
        This method is additive and not required for simple tools.
        """

        return []

    # -- Execution --------------------------------------------------
    @abstractmethod
    def execute(self, **kwargs: Any) -> Any:
        """Execute the tool.

        Subclasses must implement this method. Callers should validate inputs
        first (``tool.validate(...)``) and may call ``is_available`` or
        ``availability`` to check preconditions.
        """

    # -- Representation ---------------------------------------------
    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"{self.__class__.__name__}(name='{self.name}')"
