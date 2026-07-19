"""
JARVIS Re-ranker

Re-ranks retrieved document chunks.

Current Version:
    Score-based ranking.

Future Versions:
    Cross Encoder
    Cohere Rerank
    Jina Reranker
    BGE Reranker
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from app.rag.models import RetrievalResult

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class RerankerConfig:
    """
    Configuration for result reranking.
    """

    top_k: int = 5

    minimum_score: float = 0.30


class Reranker:
    """
    Re-ranks retrieval results.
    """

    def __init__(
        self,
        config: RerankerConfig | None = None,
    ) -> None:

        self._config = config or RerankerConfig()

    def rerank(
        self,
        query: str,
        results: list[RetrievalResult],
    ) -> list[RetrievalResult]:
        """
        Re-rank retrieved results.

        Current implementation sorts by similarity score.

        Future versions will use semantic cross-encoders.
        """

        del query

        filtered = [
            result
            for result in results
            if result.score >= self._config.minimum_score
        ]

        filtered.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        ranked = filtered[: self._config.top_k]

        logger.info(
            "Reranked %d result(s).",
            len(ranked),
        )

        return ranked