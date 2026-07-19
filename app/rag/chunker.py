"""
JARVIS Text Chunker

Splits cleaned documents into overlapping chunks suitable
for embedding and retrieval.

Responsibilities:
- Chunk text
- Preserve context using overlap
- Generate DocumentChunk models

No embedding or vector store logic belongs here.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

from app.rag.models import (
    DocumentChunk,
    ParsedDocument,
)


@dataclass(slots=True)
class ChunkConfig:
    """
    Configuration for text chunking.
    """

    chunk_size: int = 1000

    chunk_overlap: int = 200

    strip_chunks: bool = True


class TextChunker:
    """
    Creates overlapping text chunks.
    """

    def __init__(
        self,
        config: ChunkConfig | None = None,
    ) -> None:

        self._config = config or ChunkConfig()

        if (
            self._config.chunk_overlap
            >= self._config.chunk_size
        ):
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

    def chunk(
        self,
        document: ParsedDocument,
    ) -> list[DocumentChunk]:
        """
        Split a parsed document into chunks.
        """

        text = document.content

        chunks: list[DocumentChunk] = []

        start = 0

        chunk_index = 0

        step = (
            self._config.chunk_size
            - self._config.chunk_overlap
        )

        while start < len(text):

            end = start + self._config.chunk_size

            piece = text[start:end]

            if self._config.strip_chunks:
                piece = piece.strip()

            if piece:

                chunks.append(
                    DocumentChunk(
                        chunk_id=str(uuid.uuid4()),
                        document_id=document.document.document_id,
                        text=piece,
                        chunk_index=chunk_index,
                        metadata=document.document.metadata,
                    )
                )

                chunk_index += 1

            start += step

        return chunks