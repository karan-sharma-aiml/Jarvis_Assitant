"""
Base Retrieval Interface

Defines the abstract interface for all retrieval backends used
by the JARVIS Knowledge Engine.

All vector stores and retrieval systems must implement this
interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseRetriever(ABC):
    """
    Abstract interface for retrieval systems.
    """

    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the retrieval backend.
        """

    @abstractmethod
    def add_documents(
        self,
        documents: list[Any],
    ) -> None:
        """
        Store processed documents.
        """

    @abstractmethod
    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[Any]:
        """
        Retrieve relevant documents.
        """

    @abstractmethod
    def delete(
        self,
        document_id: str,
    ) -> bool:
        """
        Delete a document.
        """

    @abstractmethod
    def clear(self) -> None:
        """
        Remove every stored document.
        """

    @abstractmethod
    def document_count(self) -> int:
        """
        Return total stored documents.
        """

    @abstractmethod
    def health_check(self) -> bool:
        """
        Verify backend health.
        """