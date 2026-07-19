"""
JARVIS Knowledge Engine Models.

Defines storage-independent data models shared by every
component of the Knowledge Engine.

This module intentionally contains no business logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any


class DocumentType(StrEnum):
    """
    Supported document types.
    """

    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    MARKDOWN = "markdown"
    HTML = "html"
    CSV = "csv"
    JSON = "json"
    UNKNOWN = "unknown"


@dataclass(slots=True)
class DocumentMetadata:
    """
    Metadata associated with a document.
    """

    source: str = "local"

    author: str | None = None

    tags: list[str] = field(default_factory=list)

    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Document:
    """
    Raw document before parsing.
    """

    document_id: str

    path: Path

    document_type: DocumentType

    metadata: DocumentMetadata = field(
        default_factory=DocumentMetadata
    )


@dataclass(slots=True)
class ParsedDocument:
    """
    Parsed document text.
    """

    document: Document

    content: str

    parsed_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )


@dataclass(slots=True)
class DocumentChunk:
    """
    One chunk generated from a parsed document.
    """

    chunk_id: str

    document_id: str

    text: str

    chunk_index: int

    metadata: DocumentMetadata = field(
        default_factory=DocumentMetadata
    )


@dataclass(slots=True)
class EmbeddingRecord:
    """
    Embedding associated with one chunk.
    """

    chunk: DocumentChunk

    vector: list[float]


@dataclass(slots=True)
class RetrievalResult:
    """
    Result returned from vector search.
    """

    chunk: DocumentChunk

    score: float