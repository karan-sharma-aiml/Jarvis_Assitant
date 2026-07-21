"""
Tool Router Models

Shared models used by the routing layer.

Responsibilities
----------------
- Represent one routing decision.
- Describe which manager and method should execute.
- Carry routing metadata.

Contains NO routing logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ToolRoute:
    """
    Represents one routing decision.
    """

    manager: str

    method: str

    required_entities: tuple[str, ...] = ()

    priority: int = 100

    requires_confirmation: bool = False

    metadata: dict[str, object] = field(
        default_factory=dict
    )

    @property
    def has_required_entities(self) -> bool:
        """
        True if the route requires entities.
        """
        return len(self.required_entities) > 0

    def requires(
        self,
        entity: str,
    ) -> bool:
        """
        Check whether an entity is required.
        """
        return entity in self.required_entities

    def to_dict(self) -> dict[str, object]:
        """
        Convert to serializable dictionary.
        """
        return {
            "manager": self.manager,
            "method": self.method,
            "required_entities": list(
                self.required_entities
            ),
            "priority": self.priority,
            "requires_confirmation":
                self.requires_confirmation,
            "metadata": self.metadata,
        }

    def __str__(self) -> str:
        return (
            "ToolRoute("
            f"manager={self.manager}, "
            f"method={self.method}, "
            f"priority={self.priority})"
        )

    def __repr__(self) -> str:
        return self.__str__()