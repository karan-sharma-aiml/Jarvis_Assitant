"""
Semantic Memory

Provides semantic search capabilities over stored memories.

This implementation is backend-independent.

The current version performs metadata-based retrieval.

Future versions will integrate vector databases
(FAISS / ChromaDB) without changing the public API.
"""

from __future__ import annotations

import json
import logging

from app.memory.database import Database
from app.memory.models import MemorySearchResult

logger = logging.getLogger(__name__)


class SemanticMemory:
    """
    Semantic memory retrieval interface.

    Current implementation:
        Keyword matching.

    Future implementation:
        Embedding similarity search.
    """

    def __init__(self, database: Database) -> None:
        self._database = database

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[MemorySearchResult]:
        """
        Search memories related to the given query.

        Returns:
            Ranked list of MemorySearchResult objects.
        """

        query = query.lower()

        rows = self._database.fetchall(
            """
            SELECT *
            FROM memories
            ORDER BY updated_at DESC
            """
        )

        results: list[MemorySearchResult] = []

        for row in rows:

            searchable = (
                row["memory_key"]
                + " "
                + row["memory_value"]
            ).lower()

            if query not in searchable:
                continue

            from app.memory.models import (
                MemoryImportance,
                MemoryMetadata,
                MemoryRecord,
                MemoryType,
            )

            metadata = MemoryMetadata()

            if row["metadata"]:

                try:
                    raw = json.loads(row["metadata"])

                    metadata.source = raw.get(
                        "source",
                        metadata.source,
                    )

                    metadata.tags = raw.get(
                        "tags",
                        [],
                    )

                    metadata.confidence = raw.get(
                        "confidence",
                        1.0,
                    )

                    metadata.extra = raw.get(
                        "extra",
                        {},
                    )

                except Exception:
                    pass

            record = MemoryRecord(
                key=row["memory_key"],
                value=row["memory_value"],
                memory_type=MemoryType(
                    row["memory_type"]
                ),
                importance=MemoryImportance(
                    row["importance"]
                ),
                metadata=metadata,
            )

            score = 1.0

            if query == row["memory_key"].lower():
                score = 2.0

            elif query in row["memory_value"].lower():
                score = 1.5

            results.append(
                MemorySearchResult(
                    record=record,
                    score=score,
                )
            )

        results.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        logger.info(
            "Semantic search '%s' returned %d result(s).",
            query,
            len(results),
        )

        return results[:limit]