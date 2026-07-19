"""
JARVIS Knowledge Manager

Public interface for the Knowledge Engine.

Responsibilities:
- Index documents
- Index directories
- Search knowledge
- Clear knowledge base
- Health check

Acts as the single entry point for every
Knowledge Engine operation.
"""

from __future__ import annotations

import logging
from pathlib import Path

from app.rag.pipeline import KnowledgePipeline

logger = logging.getLogger(__name__)


class RAGManager:
    """
    Public manager for the Knowledge Engine.
    """

    def __init__(self) -> None:
        self._pipeline = KnowledgePipeline()

    @property
    def pipeline(self) -> KnowledgePipeline:
        """
        Expose pipeline (read-only).
        """
        return self._pipeline

    def index_document(
        self,
        file_path: str | Path,
    ) -> None:
        """
        Index a single document.
        """
        logger.info(
            "Indexing document: %s",
            file_path,
        )

        self._pipeline.index_document(
            file_path,
        )

    def index_directory(
        self,
        directory: str | Path,
        recursive: bool = True,
    ) -> None:
        """
        Index every supported document inside a directory.
        """

        documents = self._pipeline.loader.load_directory(
            directory,
            recursive=recursive,
        )

        logger.info(
            "Indexing %d documents.",
            len(documents),
        )

        for document in documents:

            self._pipeline.index_document(
                document.path,
            )

    def search(
        self,
        query: str,
    ):
        """
        Search indexed knowledge.
        """

        return self._pipeline.search(
            query,
        )

    def clear(
        self,
    ) -> None:
        """
        Remove every indexed document.
        """

        self._pipeline.vector_store.clear()

        logger.info(
            "Knowledge base cleared."
        )

    def document_count(
        self,
    ) -> int:
        """
        Number of indexed chunks.
        """

        return self._pipeline.vector_store.size

    def health_check(
        self,
    ) -> bool:
        """
        Verify Knowledge Engine health.
        """

        try:

            _ = self.document_count()

            return True

        except Exception:

            logger.exception(
                "Knowledge Engine health check failed."
            )

            return False

    def __repr__(
        self,
    ) -> str:

        return (
            f"RAGManager("
            f"documents={self.document_count()}"
            f")"
        )