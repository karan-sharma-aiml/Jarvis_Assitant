"""
JARVIS Document Loader

Discovers and loads supported documents from the local
filesystem.

Responsibilities:
- Validate file existence
- Detect supported document type
- Create Document models

This module performs NO parsing.
"""

from __future__ import annotations

import logging
import uuid
from pathlib import Path

from app.rag.models import (
    Document,
    DocumentMetadata,
    DocumentType,
)

logger = logging.getLogger(__name__)


class DocumentLoader:
    """
    Loads supported documents from disk.
    """

    _SUPPORTED_TYPES: dict[str, DocumentType] = {
        ".pdf": DocumentType.PDF,
        ".docx": DocumentType.DOCX,
        ".txt": DocumentType.TXT,
        ".md": DocumentType.MARKDOWN,
        ".html": DocumentType.HTML,
        ".csv": DocumentType.CSV,
        ".json": DocumentType.JSON,
    }

    def load(
        self,
        file_path: str | Path,
    ) -> Document:
        """
        Load one document.

        Args:
            file_path:
                File to load.

        Returns:
            Document
        """

        path = Path(file_path).expanduser().resolve()

        if not path.exists():
            raise FileNotFoundError(path)

        document = Document(
            document_id=str(uuid.uuid4()),
            path=path,
            document_type=self._detect_type(path),
            metadata=DocumentMetadata(
                source="local",
            ),
        )

        logger.info(
            "Loaded document: %s",
            path.name,
        )

        return document

    def load_directory(
        self,
        directory: str | Path,
        recursive: bool = True,
    ) -> list[Document]:
        """
        Load every supported document inside a directory.
        """

        directory = Path(directory).expanduser().resolve()

        if not directory.exists():
            raise FileNotFoundError(directory)

        iterator = (
            directory.rglob("*")
            if recursive
            else directory.glob("*")
        )

        documents: list[Document] = []

        for file in iterator:

            if not file.is_file():
                continue

            if file.suffix.lower() not in self._SUPPORTED_TYPES:
                continue

            documents.append(
                self.load(file)
            )

        logger.info(
            "Loaded %d documents.",
            len(documents),
        )

        return documents

    def supported_extensions(
        self,
    ) -> tuple[str, ...]:
        """
        Return supported file extensions.
        """

        return tuple(
            sorted(
                self._SUPPORTED_TYPES.keys()
            )
        )

    def _detect_type(
        self,
        path: Path,
    ) -> DocumentType:
        """
        Detect document type.
        """

        return self._SUPPORTED_TYPES.get(
            path.suffix.lower(),
            DocumentType.UNKNOWN,
        )