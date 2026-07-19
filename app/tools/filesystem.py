"""
JARVIS File System Tool

Provides safe file system operations.

Supported operations:
- list_directory
- read_file
- write_file
- create_directory
- delete_file
- file_exists

All operations are restricted to the configured working directory.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from app.tools.base import BaseTool
from app.tools.exceptions import (
    ToolExecutionError,
    ToolValidationError,
)
from app.tools.models import ToolCategory


class FileSystemTool(BaseTool):
    """
    Safe file system tool.
    """

    def __init__(self, root_directory: str | Path = ".") -> None:
        self._root = Path(root_directory).resolve()

    @property
    def name(self) -> str:
        return "filesystem"

    @property
    def description(self) -> str:
        return "Performs safe file system operations."

    @property
    def category(self) -> ToolCategory:
        return ToolCategory.FILESYSTEM

    def validate(self, **kwargs: Any) -> None:
        operation = kwargs.get("operation")

        allowed = {
            "list_directory",
            "read_file",
            "write_file",
            "create_directory",
            "delete_file",
            "file_exists",
        }

        if operation not in allowed:
            raise ToolValidationError(
                f"Unsupported operation: {operation}"
            )

    def execute(self, **kwargs: Any) -> Any:
        self.validate(**kwargs)

        operation = kwargs["operation"]

        if operation == "list_directory":
            return self._list_directory(kwargs["path"])

        if operation == "read_file":
            return self._read_file(kwargs["path"])

        if operation == "write_file":
            return self._write_file(
                kwargs["path"],
                kwargs["content"],
            )

        if operation == "create_directory":
            return self._create_directory(kwargs["path"])

        if operation == "delete_file":
            return self._delete_file(kwargs["path"])

        if operation == "file_exists":
            return self._file_exists(kwargs["path"])

        raise ToolValidationError(
            f"Unsupported operation: {operation}"
        )

    def _resolve(self, path: str | Path) -> Path:
        """
        Prevent directory traversal.
        """
        resolved = (self._root / path).resolve()

        if self._root not in resolved.parents and resolved != self._root:
            raise ToolExecutionError(
                "Access outside root directory is not allowed."
            )

        return resolved

    def _list_directory(self, path: str | Path) -> list[str]:
        directory = self._resolve(path)

        if not directory.exists():
            raise ToolExecutionError("Directory does not exist.")

        if not directory.is_dir():
            raise ToolExecutionError("Path is not a directory.")

        return sorted(item.name for item in directory.iterdir())

    def _read_file(self, path: str | Path) -> str:
        file = self._resolve(path)

        if not file.exists():
            raise ToolExecutionError("File does not exist.")

        return file.read_text(encoding="utf-8")

    def _write_file(
        self,
        path: str | Path,
        content: str,
    ) -> str:
        file = self._resolve(path)

        file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file.write_text(
            content,
            encoding="utf-8",
        )

        return "File written successfully."

    def _create_directory(
        self,
        path: str | Path,
    ) -> str:
        directory = self._resolve(path)

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        return "Directory created successfully."

    def _delete_file(
        self,
        path: str | Path,
    ) -> str:
        file = self._resolve(path)

        if not file.exists():
            raise ToolExecutionError("File does not exist.")

        file.unlink()

        return "File deleted successfully."

    def _file_exists(
        self,
        path: str | Path,
    ) -> bool:
        return self._resolve(path).exists()