"""
Base Memory Interface

Defines the abstract interface for all memory implementations
used by JARVIS.

Every memory backend must implement this interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseMemory(ABC):
    """
    Abstract base class for all memory backends.
    """

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the memory backend."""

    @abstractmethod
    def save(
        self,
        key: str,
        value: Any,
    ) -> None:
        """Store a value."""

    @abstractmethod
    def load(
        self,
        key: str,
    ) -> Any | None:
        """Load a value."""

    @abstractmethod
    def delete(
        self,
        key: str,
    ) -> bool:
        """Delete a value."""

    @abstractmethod
    def exists(
        self,
        key: str,
    ) -> bool:
        """Return True if the key exists."""

    @abstractmethod
    def clear(self) -> None:
        """Remove all stored data."""

    @abstractmethod
    def close(self) -> None:
        """Release resources."""

    @abstractmethod
    def health_check(self) -> bool:
        """Return True if the memory backend is operational."""