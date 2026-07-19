"""
Preference Memory

Stores long-term user preferences.

These preferences persist across sessions and personalize
JARVIS without affecting conversation history.
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


class PreferenceMemory:
    """
    Persistent user preference storage.
    """

    def __init__(self, database: Database) -> None:
        self._database = database

    def set(
        self,
        key: str,
        value: str,
        importance: MemoryImportance = MemoryImportance.HIGH,
    ) -> None:
        """
        Save or update a preference.
        """

        now = datetime.now(UTC).isoformat()

        record = MemoryRecord(
            key=key,
            value=value,
            memory_type=MemoryType.PREFERENCE,
            importance=importance,
            metadata=MemoryMetadata(
                source="user_preference",
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
            VALUES
            (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.key,
                record.value,
                record.memory_type.value,
                record.importance.value,
                json.dumps(record.metadata.extra),
                now,
                now,
            ),
        )

        logger.info(
            "Preference saved: %s",
            key,
        )

    def get(
        self,
        key: str,
    ) -> str | None:
        """
        Retrieve a preference.
        """

        row = self._database.fetchone(
            """
            SELECT memory_value
            FROM memories
            WHERE memory_key = ?
            AND memory_type = ?
            """,
            (
                key,
                MemoryType.PREFERENCE.value,
            ),
        )

        if row is None:
            return None

        return row["memory_value"]

    def exists(
        self,
        key: str,
    ) -> bool:
        """
        Check whether a preference exists.
        """

        return self.get(key) is not None

    def delete(
        self,
        key: str,
    ) -> bool:
        """
        Delete a preference.
        """

        cursor = self._database.execute(
            """
            DELETE FROM memories
            WHERE memory_key = ?
            AND memory_type = ?
            """,
            (
                key,
                MemoryType.PREFERENCE.value,
            ),
        )

        deleted = cursor.rowcount > 0

        if deleted:
            logger.info(
                "Preference deleted: %s",
                key,
            )

        return deleted

    def list_preferences(self) -> dict[str, str]:
        """
        Return all stored preferences.
        """

        rows = self._database.fetchall(
            """
            SELECT memory_key, memory_value
            FROM memories
            WHERE memory_type = ?
            ORDER BY memory_key
            """,
            (
                MemoryType.PREFERENCE.value,
            ),
        )

        return {
            row["memory_key"]: row["memory_value"]
            for row in rows
        }

    def clear(self) -> None:
        """
        Remove every stored preference.
        """

        self._database.execute(
            """
            DELETE FROM memories
            WHERE memory_type = ?
            """,
            (
                MemoryType.PREFERENCE.value,
            ),
        )

        logger.info(
            "All preferences cleared."
        )