"""
JARVIS Retriever

Responsible for retrieving the most relevant document chunks
from the vector store.

Responsibilities:
- Convert query to embedding
- Perform similarity search
- Filter low-quality results
- Return RetrievalResult models

No prompt building or LLM interaction belongs here.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from app.rag.embeddings import EmbeddingEngine
from app.rag.models import RetrievalResult
from app.rag.vector_store import VectorStore

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class RetrieverConfig:
    """
    Configuration for retrieval.
    """

    top_k: int = 5

    score_threshold: float = 0.30


class Retriever:
    """
    Semantic Retriever.

    Retrieves relevant chunks using vector similarity.
    """

    def __init__(
        self,
        embedding_engine: EmbeddingEngine,
        vector_store: VectorStore,
        config: RetrieverConfig | None = None,
    ) -> None:

        self._embedding_engine = embedding_engine

        self._vector_store = vector_store

        self._config = config or RetrieverConfig()

    def retrieve(
        self,
        query: str,
    ) -> list[RetrievalResult]:
        """
        Retrieve relevant document chunks.

        Converts query to embedding using the public interface,
        then searches the vector store for similar chunks.

        Args:
            query: Search query string.

        Returns:
            list[RetrievalResult]: Ranked list of relevant chunks
                filtered by score threshold.
        """

        # Use public interface - do not access .model directly
        query_vector = self._embedding_engine.embed_query(query)

        results = self._vector_store.search(
            query_vector=query_vector,
            top_k=self._config.top_k,
        )

        retrieved: list[RetrievalResult] = []

        for record, score in results:

            if score < self._config.score_threshold:
                continue

            retrieved.append(
                RetrievalResult(
                    chunk=record.chunk,
                    score=score,
                )
            )

        logger.info(
            "Retriever returned %d result(s) for query '%s'.",
            len(retrieved),
            query,
        )

        return retrieved