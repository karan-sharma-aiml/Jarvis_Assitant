"""
Conversation Memory

Manages conversation history stored in SQLite.

Responsibilities:

- Store conversations
- Retrieve conversations
- Delete conversations
- Retrieve recent history

No LLM logic belongs here.
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


class ConversationMemory:
    """
    Handles conversation memory storage.
    """

    def __init__(self, database: Database) -> None:
        self._database = database

    def save(
        self,
        key: str,
        user_message: str,
        assistant_message: str,
        importance: MemoryImportance = MemoryImportance.NORMAL,
    ) -> None:
        """
        Save one conversation exchange.
        """

        timestamp = datetime.now(UTC).isoformat()

        record = MemoryRecord(
            key=key,
            value=json.dumps(
                {
                    "user": user_message,
                    "assistant": assistant_message,
                }
            ),
            memory_type=MemoryType.CONVERSATION,
            importance=importance,
            metadata=MemoryMetadata(
                source="conversation",
            ),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
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
                timestamp,
                timestamp,
            ),
        )

        logger.info(
            "Conversation saved: %s",
            key,
        )

    def load(
        self,
        key: str,
    ) -> dict[str, str] | None:
        """
        Load one conversation.
        """

        row = self._database.fetchone(
            """
            SELECT memory_value
            FROM memories
            WHERE memory_key = ?
            """,
            (key,),
        )

        if row is None:
            return None

        return json.loads(row["memory_value"])

    def delete(
        self,
        key: str,
    ) -> bool:
        """
        Delete one conversation.
        """

        cursor = self._database.execute(
            """
            DELETE FROM memories
            WHERE memory_key = ?
            """,
            (key,),
        )

        deleted = cursor.rowcount > 0

        if deleted:
            logger.info(
                "Conversation deleted: %s",
                key,
            )

        return deleted

    def recent(
        self,
        limit: int = 10,
    ) -> list[dict[str, str]]:
        """
        Return recent conversations.
        """

        rows = self._database.fetchall(
            """
            SELECT memory_value
            FROM memories
            WHERE memory_type = ?
            ORDER BY updated_at DESC
            LIMIT ?
            """,
            (
                MemoryType.CONVERSATION.value,
                limit,
            ),
        )

        return [
            json.loads(row["memory_value"])
            for row in rows
        ]