from app.tools.manager import ToolManager
from app.tools.registry import ToolRegistry


def test_tool_manager_accepts_injected_registry() -> None:
    registry = ToolRegistry()

    manager = ToolManager(registry)

    assert manager.registry is registry


def test_tool_manager_uses_default_registry_when_none_is_provided() -> None:
    manager = ToolManager()

    assert isinstance(manager.registry, ToolRegistry)
