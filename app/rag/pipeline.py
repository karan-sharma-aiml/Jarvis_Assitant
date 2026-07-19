"""
JARVIS Knowledge Pipeline

Coordinates the complete RAG workflow.

Responsibilities:
- Index documents
- Search documents
- Coordinate every Knowledge Engine component

Contains NO prompt-building logic.
Contains NO LLM calls.
"""

from __future__ import annotations

import logging
from pathlib import Path

from app.rag.chunker import TextChunker
from app.rag.document_loader import DocumentLoader
from app.rag.document_parser import DocumentParser
from app.rag.embeddings import EmbeddingEngine
from app.rag.reranker import Reranker
from app.rag.retriever import Retriever
from app.rag.text_cleaner import TextCleaner
from app.rag.vector_store import VectorStore

logger = logging.getLogger(__name__)


class KnowledgePipeline:
    """
    End-to-end Knowledge Engine pipeline.
    """

    def __init__(self) -> None:

        self.loader = DocumentLoader()

        self.parser = DocumentParser()

        self.cleaner = TextCleaner()

        self.chunker = TextChunker()

        self.embedding = EmbeddingEngine()

        self.vector_store = VectorStore(
            self.embedding.dimension
        )

        self.retriever = Retriever(
            self.embedding,
            self.vector_store,
        )

        self.reranker = Reranker()

    def index_document(
        self,
        file_path: str | Path,
    ) -> None:
        """
        Index a document.
        """

        document = self.loader.load(
            file_path
        )

        parsed = self.parser.parse(
            document
        )

        parsed.content = self.cleaner.clean(
            parsed.content
        )

        chunks = self.chunker.chunk(
            parsed
        )

        embeddings = self.embedding.embed_many(
            chunks
        )

        self.vector_store.add(
            embeddings
        )

        logger.info(
            "Indexed document: %s",
            document.path.name,
        )

    def search(
        self,
        query: str,
    ):
        """
        Search indexed documents.
        """

        retrieved = self.retriever.retrieve(
            query
        )

        return self.reranker.rerank(
            query,
            retrieved,
        )