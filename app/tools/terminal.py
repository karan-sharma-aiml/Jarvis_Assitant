"""
JARVIS Terminal Tool

Provides safe terminal command execution.

Only approved commands are allowed.
"""

from __future__ import annotations

import logging
import os
import platform
import shlex
import shutil
import subprocess
from typing import Any, Iterable, List, Optional, Sequence, Union

from app.tools.base import BaseTool
from app.tools.exceptions import ToolExecutionError, ToolValidationError
from app.tools.models import ToolCategory

logger = logging.getLogger(__name__)


class TerminalTool(BaseTool):
    """
    Safe terminal execution tool.
    """

    # Default allowlist of safe executables. Keep short and explicit.
    # Note: "dir" is a Windows shell builtin; we implement it using Python
    # to avoid shell=True. "which/where" are mapped to shutil.which when
    # available.
    _ALLOWED_COMMANDS: set[str] = {
        "python",
        "py",
        "pip",
        "git",
        "which" if platform.system() != "Windows" else "where",
        "ls" if platform.system() != "Windows" else "dir",
        "echo",
    }

    # Execution timeout in seconds (can be overridden via kwargs, but capped)
    DEFAULT_TIMEOUT: int = 30
    MAX_TIMEOUT: int = 300

    @property
    def name(self) -> str:
        return "terminal"

    @property
    def description(self) -> str:
        return "Execute safe terminal commands."

    @property
    def category(self) -> ToolCategory:
        return ToolCategory.SYSTEM

    def validate(self, **kwargs: Any) -> None:
        """Validate the incoming command arguments.

        Accepted input formats (backwards compatible):
        - ``command``: a single string command (original API)
        - ``args``: a sequence/list of arguments (executable + args)

        Validation performed:
        - Ensure a command is provided and not empty.
        - Parse the command safely (no shell evaluation).
        - Ensure the executable is a simple basename and is allowlisted.
        - Ensure the executable is discoverable on PATH when applicable.
        """

        raw_command = kwargs.get("command")
        raw_args = kwargs.get("args")

        # Use the centralized parser/validator to perform checks without
        # mutating kwargs. We ignore the returned parts here because
        # validate() must not change inputs; execute() will re-parse.
        self._parse_and_validate(raw_command, raw_args)

    def _parse_and_validate(self, raw_command: Any, raw_args: Any) -> list[str]:
        """Parse and validate a command and return a list of parts.

        This helper centralizes parsing and validation so callers can use it
        without relying on mutated kwargs. It raises ``ToolValidationError``
        for invalid input and returns the parsed ``parts`` suitable for
        execution with ``subprocess.run(shell=False)``.
        """

        if raw_args is None and raw_command is None:
            raise ToolValidationError("Either 'command' or 'args' must be provided.")

        parts: list[str]

        if raw_args is not None:
            if not isinstance(raw_args, (list, tuple)) or not raw_args:
                raise ToolValidationError("'args' must be a non-empty list of strings")
            parts = [str(p) for p in raw_args]
            raw_command_str: Optional[str] = None
        else:
            if not isinstance(raw_command, str):
                raise ToolValidationError("'command' must be a string")
            command_str = raw_command.strip()
            if not command_str:
                raise ToolValidationError("Command cannot be empty.")

            posix = platform.system() != "Windows"
            try:
                parts = shlex.split(command_str, posix=posix)
            except ValueError as exc:
                raise ToolValidationError("Failed to parse command string") from exc
            raw_command_str = command_str

        executable = parts[0]

        if os.path.basename(executable) != executable:
            raise ToolValidationError("Executable must be a bare program name, not a path")

        forbidden = {";", "&&", "||", "|", "$(`", "`"}
        if raw_command is not None and raw_command_str and any(tok in raw_command_str for tok in forbidden):
            raise ToolValidationError("Potentially unsafe shell characters in command")

        if executable not in self._ALLOWED_COMMANDS:
            raise ToolValidationError(f"Command '{executable}' is not allowed.")

        if executable not in {"dir", "echo"}:
            found = shutil.which(executable)
            if not found:
                raise ToolValidationError(f"Executable '{executable}' not found on PATH")

        return parts

    def execute(self, **kwargs: Any) -> str:
        """
        Execute a safe terminal command.
        """
        # Validate inputs (no mutation) and parse the command safely.
        raw_command = kwargs.get("command")
        raw_args = kwargs.get("args")
        # Re-parse/validate and obtain parts for execution.
        parts: list[str] = self._parse_and_validate(raw_command, raw_args)

        # Allow caller to override timeout (respect caps)
        timeout: int = kwargs.get("timeout", self.DEFAULT_TIMEOUT)
        try:
            timeout = int(timeout)
        except (TypeError, ValueError):
            raise ToolValidationError("'timeout' must be an integer number of seconds")

        if timeout <= 0 or timeout > self.MAX_TIMEOUT:
            raise ToolValidationError(f"'timeout' must be between 1 and {self.MAX_TIMEOUT} seconds")

        executable = parts[0]
        args = parts[1:]

        logger.debug("TerminalTool executing: %s (args count: %d)", executable, len(args))

        # Handle small builtins via Python implementations to avoid shell.
        if executable == "echo":
            # echo simply joins arguments with spaces
            result = " ".join(args)
            logger.info("Echo command executed")
            return result or ""

        if executable == "dir":
            # Provide a safe directory listing. Only allow relative paths
            # without parent traversal to avoid exposing arbitrary files.
            path = args[0] if args else "."
            if os.path.isabs(path) or ".." in path.split(os.path.sep):
                raise ToolValidationError("Directory listing path not allowed")
            try:
                entries = os.listdir(path)
                return "\n".join(sorted(entries))
            except OSError as exc:
                raise ToolExecutionError("Failed to list directory", details={"error": str(exc)}) from exc

        # External execution using subprocess with shell=False for safety
        cmd: list[str] = [executable] + args

        try:
            completed = subprocess.run(
                cmd,
                shell=False,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            logger.warning("Command timed out: %s", executable)
            raise ToolExecutionError("Command timed out", details={"timeout": timeout}) from exc
        except OSError as exc:
            # e.g., executable not found or permission denied
            logger.exception("OS error when executing command: %s", executable)
            raise ToolExecutionError("Execution failed", details={"error": str(exc)}) from exc

        stdout = (completed.stdout or "").strip()
        stderr = (completed.stderr or "").strip()

        if completed.returncode != 0:
            # Avoid leaking large amounts of stderr; provide a truncated snippet
            snippet = (stderr[:500] + "...") if len(stderr) > 500 else stderr
            logger.warning("Command %s failed (rc=%d): %s", executable, completed.returncode, snippet)
            raise ToolExecutionError(
                f"Command failed (exit code {completed.returncode})",
                details={"stderr": snippet, "returncode": completed.returncode},
            )

        logger.info("Command %s completed successfully", executable)
        return stdout or ""