"""
Episodic Memory

Stores important long-term events.

Unlike conversation memory, episodic memory captures
significant milestones, achievements, and events that
should remain available across future conversations.
"""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime

from app.memory.database import Database
from app.memory.models import (
    MemoryImportance,
    MemoryMetadata,
    MemoryRecord,
    MemoryType,
)

logger = logging.getLogger(__name__)


class EpisodicMemory:
    """
    Persistent storage for important life or project events.
    """

    def __init__(self, database: Database) -> None:
        self._database = database

    def add_event(
        self,
        event_id: str,
        title: str,
        description: str,
        importance: MemoryImportance = MemoryImportance.HIGH,
        tags: list[str] | None = None,
    ) -> None:
        """
        Store a new episodic memory.
        """

        now = datetime.now(UTC).isoformat()

        payload = {
            "title": title,
            "description": description,
        }

        record = MemoryRecord(
            key=event_id,
            value=json.dumps(payload),
            memory_type=MemoryType.EPISODIC,
            importance=importance,
            metadata=MemoryMetadata(
                source="episodic_memory",
                tags=tags or [],
            ),
        )

        self._database.execute(
            """
            INSERT OR REPLACE INTO memories
            (
                memory_key,
                memory_value,
                memory_type,
                importance,
                metadata,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.key,
                record.value,
                record.memory_type.value,
                record.importance.value,
                json.dumps(
                    {
                        "source": record.metadata.source,
                        "tags": record.metadata.tags,
                        "confidence": record.metadata.confidence,
                        "extra": record.metadata.extra,
                    }
                ),
                now,
                now,
            ),
        )

        logger.info(
            "Episodic memory stored: %s",
            title,
        )

    def get_event(
        self,
        event_id: str,
    ) -> dict[str, str] | None:
        """
        Retrieve one episodic memory.
        """

        row = self._database.fetchone(
            """
            SELECT memory_value
            FROM memories
            WHERE memory_key = ?
            AND memory_type = ?
            """,
            (
                event_id,
                MemoryType.EPISODIC.value,
            ),
        )

        if row is None:
            return None

        return json.loads(row["memory_value"])

    def list_events(
        self,
    ) -> list[dict[str, str]]:
        """
        Return all episodic memories.
        """

        rows = self._database.fetchall(
            """
            SELECT memory_value
            FROM memories
            WHERE memory_type = ?
            ORDER BY created_at DESC
            """,
            (
                MemoryType.EPISODIC.value,
            ),
        )

        return [
            json.loads(row["memory_value"])
            for row in rows
        ]

    def delete_event(
        self,
        event_id: str,
    ) -> bool:
        """
        Delete an episodic memory.
        """

        cursor = self._database.execute(
            """
            DELETE FROM memories
            WHERE memory_key = ?
            AND memory_type = ?
            """,
            (
                event_id,
                MemoryType.EPISODIC.value,
            ),
        )

        deleted = cursor.rowcount > 0

        if deleted:
            logger.info(
                "Deleted episodic memory: %s",
                event_id,
            )

        return deleted