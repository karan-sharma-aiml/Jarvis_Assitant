"""
Tool Router

Routes an Intent to its corresponding ToolRoute.

Responsibilities
----------------
- Validate incoming Intent.
- Look up the route in ToolRegistry.
- Return ToolRoute.
- Return None if no route exists.

Contains NO execution logic.
"""

from __future__ import annotations

import logging

from app.intent.models import Intent, IntentName
from app.router.models import ToolRoute
from app.router.registry import ToolRegistry

logger = logging.getLogger(__name__)


class ToolRouter:
    """
    Converts Intent -> ToolRoute.
    """

    __slots__ = ("_registry",)

    def __init__(self) -> None:
        self._registry = ToolRegistry

    def route(
        self,
        intent: Intent | None,
    ) -> ToolRoute | None:
        """Return the ToolRoute for an Intent."""
        if not isinstance(intent, Intent):
            logger.debug("Received invalid intent object %r", intent)
            return None

        if intent.is_unknown:
            logger.debug("Received unknown intent; no route available")
            return None

        route = self._registry.get(intent.name)
        if route is None:
            logger.debug("No route found for intent %s", intent.name)
        return route

    def can_route(
        self,
        intent: Intent | None,
    ) -> bool:
        """Check whether an intent can be routed."""
        if not isinstance(intent, Intent):
            logger.debug("Received invalid intent object %r", intent)
            return False

        if intent.is_unknown:
            return False

        return self._registry.exists(intent.name)

    def available_routes(
        self,
    ) -> dict[IntentName, ToolRoute]:
        """Return all registered routes."""
        return self._registry.all()

    def route_count(
        self,
    ) -> int:
        """
        Return number of routes.
        """

        return self._registry.count()

    def health_check(
        self,
    ) -> bool:
        """
        Router health.
        """

        return self._registry.health_check()

    def __repr__(
        self,
    ) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(routes={self.route_count()})"
        )