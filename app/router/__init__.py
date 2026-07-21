"""
JARVIS Tool Router

Routes detected intents to the correct system manager.
"""

from app.router.models import ToolRoute

try:
    from app.router.registry import ToolRegistry
except ImportError:  # pragma: no cover - allows incremental development
    ToolRegistry = None

try:
    from app.router.tool_router import ToolRouter
except ImportError:  # pragma: no cover - allows incremental development
    ToolRouter = None

__all__ = [
    "ToolRoute",
    "ToolRegistry",
    "ToolRouter",
]