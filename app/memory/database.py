"""
JARVIS SQLite Database

Provides a reusable SQLite database layer for the memory subsystem.

Responsibilities:

- Database connection
- Schema initialization
- Transaction handling
- Query execution
- Resource cleanup

This module contains NO memory business logic.
"""

from __future__ import annotations

import logging
import sqlite3
from pathlib import Path
from sqlite3 import Connection, Cursor
from typing import Any

from app.config.settings import settings

logger = logging.getLogger(__name__)


class Database:
    """
    SQLite database wrapper.
    """

    def __init__(self, database_path: str | None = None) -> None:
        self._database_path = Path(
            database_path or settings.DATABASE_PATH
        )

        self._connection: Connection | None = None

    @property
    def connection(self) -> Connection:
        """
        Returns an active SQLite connection.
        """

        if self._connection is None:

            self.connect()

        return self._connection

    def connect(self) -> None:
        """
        Open the SQLite connection.
        """

        if self._connection is not None:
            return

        self._database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._connection = sqlite3.connect(
            self._database_path,
            check_same_thread=False,
        )

        self._connection.row_factory = sqlite3.Row

        logger.info(
            "SQLite connected: %s",
            self._database_path,
        )

    def initialize(self) -> None:
        """
        Create required database tables.
        """

        query = """
        CREATE TABLE IF NOT EXISTS memories (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            memory_key TEXT UNIQUE NOT NULL,

            memory_value TEXT NOT NULL,

            memory_type TEXT NOT NULL,

            importance TEXT NOT NULL,

            metadata TEXT,

            created_at TEXT NOT NULL,

            updated_at TEXT NOT NULL
        );
        """

        self.execute(query)

        logger.info("Memory tables initialized.")

    def execute(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> Cursor:
        """
        Execute a query and commit automatically.
        """

        cursor = self.connection.cursor()

        cursor.execute(query, parameters)

        self.connection.commit()

        return cursor

    def executemany(
        self,
        query: str,
        parameters: list[tuple[Any, ...]],
    ) -> None:
        """
        Execute multiple statements.
        """

        cursor = self.connection.cursor()

        cursor.executemany(query, parameters)

        self.connection.commit()

    def fetchone(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> sqlite3.Row | None:
        """
        Return one row.
        """

        return self.execute(
            query,
            parameters,
        ).fetchone()

    def fetchall(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> list[sqlite3.Row]:
        """
        Return all rows.
        """

        return self.execute(
            query,
            parameters,
        ).fetchall()

    def close(self) -> None:
        """
        Close database connection.
        """

        if self._connection is None:
            return

        self._connection.close()

        self._connection = None

        logger.info("SQLite connection closed.")

    def __enter__(self) -> "Database":
        self.connect()
        return self

    def __exit__(
        self,
        exc_type,
        exc,
        traceback,
    ) -> None:
        self.close()