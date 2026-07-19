"""
JARVIS Vector Store

Stores and retrieves embedding vectors.

Current backend:
    FAISS

Future backends:
    ChromaDB
    Milvus
    Pinecone
    Qdrant
"""

from __future__ import annotations

import logging
from pathlib import Path

import faiss
import numpy as np

from app.rag.models import EmbeddingRecord

logger = logging.getLogger(__name__)


class VectorStore:
    """
    FAISS vector database wrapper.
    """

    def __init__(
        self,
        dimension: int,
    ) -> None:

        self._dimension = dimension

        self._index = faiss.IndexFlatIP(
            dimension
        )

        self._records: list[EmbeddingRecord] = []

    @property
    def size(
        self,
    ) -> int:
        """
        Number of indexed chunks.
        """

        return len(
            self._records
        )

    def add(
        self,
        records: list[EmbeddingRecord],
    ) -> None:
        """
        Store embeddings.
        """

        if not records:
            return

        vectors = np.array(
            [
                record.vector
                for record in records
            ],
            dtype="float32",
        )

        self._index.add(
            vectors
        )

        self._records.extend(
            records
        )

        logger.info(
            "Indexed %d chunks.",
            len(records),
        )

    def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
    ) -> list[tuple[EmbeddingRecord, float]]:
        """
        Similarity search.
        """

        if self.size == 0:
            return []

        distances, indices = self._index.search(
            np.array(
                [query_vector],
                dtype="float32",
            ),
            top_k,
        )

        results: list[
            tuple[
                EmbeddingRecord,
                float,
            ]
        ] = []

        for score, idx in zip(
            distances[0],
            indices[0],
            strict=True,
        ):

            if idx == -1:
                continue

            results.append(
                (
                    self._records[idx],
                    float(score),
                )
            )

        return results

    def clear(
        self,
    ) -> None:
        """
        Reset vector index.
        """

        self._index.reset()

        self._records.clear()

    def save(
        self,
        path: str | Path,
    ) -> None:
        """
        Persist FAISS index.
        """

        faiss.write_index(
            self._index,
            str(path),
        )

    def load(
        self,
        path: str | Path,
    ) -> None:
        """
        Load FAISS index.
        """

        self._index = faiss.read_index(
            str(path),
        )