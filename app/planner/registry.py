"""
Planner Registry

Stores and provides planner implementations.

Responsibilities
----------------
- Register planners.
- Retrieve planners.
- Health checks.

Contains NO planning logic.
"""

from __future__ import annotations

from typing import Protocol


class Planner(Protocol):
    """Planner interface used by the registry."""

    def create_plan(self, text: str) -> object:
        ...


class PlannerRegistry:
    """Registry for planner implementations."""

    def __init__(self) -> None:
        self._planners: dict[str, Planner] = {}

    def register(self, name: str, planner: Planner) -> None:
        """Register a planner instance under the provided name."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Planner name cannot be empty.")

        self._planners[name.strip()] = planner

    def get(self, name: str) -> Planner | None:
        """Return a registered planner by name."""
        if not isinstance(name, str) or not name.strip():
            return None
        return self._planners.get(name.strip())

    def exists(self, name: str) -> bool:
        """Return True when a planner with the given name exists."""
        if not isinstance(name, str) or not name.strip():
            return False
        return name.strip() in self._planners

    def names(self) -> tuple[str, ...]:
        """Return the registered planner names."""
        return tuple(self._planners.keys())

    def count(self) -> int:
        """Return the number of registered planners."""
        return len(self._planners)

    def clear(self) -> None:
        """Remove all registered planners."""
        self._planners.clear()

    def health_check(self) -> bool:
        """Return True when the registry is usable."""
        return True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(planners={self.count()})"