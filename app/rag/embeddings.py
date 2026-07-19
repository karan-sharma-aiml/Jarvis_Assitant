"""
JARVIS Embedding Engine

Generates dense vector embeddings for document chunks.

This implementation uses Sentence Transformers.

Future versions can support:

- Ollama
- OpenAI
- Gemini
- Jina AI
- Voyage AI
- NVIDIA

without changing the public API.
"""

from __future__ import annotations

import logging
from functools import cached_property

from sentence_transformers import SentenceTransformer

from app.config.settings import settings
from app.rag.models import (
    DocumentChunk,
    EmbeddingRecord,
)

logger = logging.getLogger(__name__)


class EmbeddingEngine:
    """
    Generates embeddings for document chunks.

    Configuration Priority (highest to lowest):
    1. Explicit model_name parameter: EmbeddingEngine(model_name="custom-model")
    2. Settings: settings.EMBEDDING_MODEL from app.config.settings
    3. Default fallback: "sentence-transformers/all-MiniLM-L6-v2"

    The model is loaded lazily on first use and cached via @cached_property
    to avoid unnecessary I/O overhead.
    """

    DEFAULT_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    def __init__(
        self,
        model_name: str | None = None,
    ) -> None:
        """
        Initialize EmbeddingEngine with optional model override.

        Args:
            model_name: Explicit model identifier to use. If provided, takes
                priority over settings.EMBEDDING_MODEL and DEFAULT_MODEL.
                If None, uses settings.EMBEDDING_MODEL.

        Maintains backward compatibility: calling EmbeddingEngine() without
        arguments uses the configured settings model or default.
        """

        # Priority: explicit parameter → settings → safe default
        self._model_name: str = (
            model_name
            or settings.EMBEDDING_MODEL
            or self.DEFAULT_MODEL
        )

    @cached_property
    def model(self) -> SentenceTransformer:
        """
        Lazily load and cache the embedding model.

        Model selection follows priority order:
        1. Explicit model_name passed to __init__
        2. EMBEDDING_MODEL from centralized settings
        3. DEFAULT_MODEL ("sentence-transformers/all-MiniLM-L6-v2")

        Returns:
            SentenceTransformer: Loaded model instance cached for lifetime
                of this EmbeddingEngine instance.

        Raises:
            OSError: If model cannot be downloaded from Hugging Face Hub.
            ImportError: If required dependencies are missing.
        """

        logger.info(
            "Loading embedding model: %s",
            self._model_name,
        )

        return SentenceTransformer(
            self._model_name
        )

    def embed_query(
        self,
        query: str,
    ) -> list[float]:
        """
        Generate embedding for a search query.

        Public interface for query embedding. Used by Retriever to avoid
        direct coupling to the embedding library (SentenceTransformer, etc).

        This method normalizes the query and returns a plain list of floats,
        which is the public contract for embedding queries.

        Args:
            query: Text query to embed.

        Returns:
            list[float]: Normalized embedding vector as list of floats.

        Raises:
            RuntimeError: If model loading failed.
            ValueError: If query text is invalid or empty.

        Example:
            >>> engine = EmbeddingEngine()
            >>> vector = engine.embed_query("What is Python?")
            >>> len(vector)  # Depends on model, e.g., 384 for all-MiniLM-L6-v2
            384
        """

        if not query or not isinstance(query, str):
            raise ValueError("Query must be a non-empty string")

        vector = self.model.encode(
            query,
            normalize_embeddings=True,
        )

        return vector.tolist()

    def embed_queries(
        self,
        queries: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple search queries (batch).

        More efficient than calling embed_query() multiple times because
        the model encodes all queries in a single batch operation.

        Public interface for batch query embedding used by advanced
        retrieval systems that process multiple queries simultaneously.

        Args:
            queries: List of text queries to embed.

        Returns:
            list[list[float]]: List of normalized embedding vectors.
                Order matches input queries exactly.

        Raises:
            RuntimeError: If model loading failed.
            ValueError: If queries list is empty or contains invalid text.

        Example:
            >>> engine = EmbeddingEngine()
            >>> queries = ["What is Python?", "How to learn Rust?"]
            >>> vectors = engine.embed_queries(queries)
            >>> len(vectors)
            2
            >>> len(vectors[0])
            384
        """

        if not queries or not isinstance(queries, list):
            raise ValueError("Queries must be a non-empty list")

        if not all(isinstance(q, str) and q for q in queries):
            raise ValueError("All queries must be non-empty strings")

        vectors = self.model.encode(
            queries,
            normalize_embeddings=True,
        )

        # Convert numpy arrays to lists
        return [v.tolist() for v in vectors]

    def embed(
        self,
        chunk: DocumentChunk,
    ) -> EmbeddingRecord:
        """
        Generate embedding for a single document chunk.

        Uses the configured model (respecting priority order) to create
        a normalized dense vector representation of the chunk's text.

        Args:
            chunk: DocumentChunk object containing text to embed.

        Returns:
            EmbeddingRecord: Contains original chunk and its embedding vector.

        Raises:
            RuntimeError: If model loading failed.
            ValueError: If chunk text is invalid.
        """

        vector = self.model.encode(
            chunk.text,
            normalize_embeddings=True,
        )

        return EmbeddingRecord(
            chunk=chunk,
            vector=vector.tolist(),
        )

    def embed_many(
        self,
        chunks: list[DocumentChunk],
    ) -> list[EmbeddingRecord]:
        """
        Batch embedding for multiple document chunks.

        Efficiently encodes multiple chunks in a single model call,
        which is more performant than sequential embed() calls.

        Args:
            chunks: List of DocumentChunk objects to embed.

        Returns:
            list[EmbeddingRecord]: Parallel list of embedding records
                matching input chunks in the same order.

        Raises:
            RuntimeError: If model loading failed.
            ValueError: If chunks list is empty or contains invalid text.
        """

        vectors = self.model.encode(
            [c.text for c in chunks],
            normalize_embeddings=True,
        )

        results: list[EmbeddingRecord] = []

        for chunk, vector in zip(
            chunks,
            vectors,
            strict=True,
        ):

            results.append(
                EmbeddingRecord(
                    chunk=chunk,
                    vector=vector.tolist(),
                )
            )

        logger.info(
            "Generated embeddings for %d chunks.",
            len(results),
        )

        return results

    @property
    def dimension(
        self,
    ) -> int:
        """
        Get the embedding dimensionality for the configured model.

        Returns the vector dimension size of the loaded embedding model.
        This is useful for vector database initialization and verification.

        Returns:
            int: Dimension size (e.g., 384 for all-MiniLM-L6-v2).

        Raises:
            RuntimeError: If model loading failed.
        """

        return self.model.get_embedding_dimension()