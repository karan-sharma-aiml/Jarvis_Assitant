"""
JARVIS Screenshot Manager

Responsibilities
----------------
- Capture full screen
- Save screenshot
- Open screenshot
- Health check
"""

from __future__ import annotations

import logging
import subprocess
from datetime import datetime
from pathlib import Path

import mss
from PIL import Image

from app.system.models import SystemResponse, SystemStatus

logger = logging.getLogger(__name__)


class ScreenshotManager:
    """Windows screenshot controller."""

    def __init__(self) -> None:
        self._default_directory = Path.home() / "Pictures" / "Jarvis"
        self._default_directory.mkdir(parents=True, exist_ok=True)

    def _resolve_directory(self, save_directory: str | Path | None) -> Path:
        if save_directory is None:
            return self._default_directory

        directory = Path(str(save_directory)).expanduser()
        if not directory.is_absolute():
            directory = Path.cwd() / directory
        return directory

    def _build_output_path(self, directory: Path) -> Path:
        for _ in range(5):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            output = directory / f"{timestamp}.png"
            if not output.exists():
                return output

        return directory / f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"

    def take_screenshot(self, save_directory: str | Path | None = None) -> SystemResponse:
        """Capture the primary monitor."""

        directory = self._resolve_directory(save_directory)
        try:
            directory.mkdir(parents=True, exist_ok=True)
            output = self._build_output_path(directory)

            with mss.mss() as sct:
                monitor = sct.monitors[1]
                image = sct.grab(monitor)
                Image.frombytes("RGB", image.size, image.rgb).save(output)
        except (OSError, ValueError, RuntimeError) as exc:
            logger.exception("Unable to capture screenshot: %s", exc)
            return SystemResponse(SystemStatus.FAILED, f"Unable to save screenshot: {exc}")

        logger.info("Screenshot saved: %s", output)
        return SystemResponse(SystemStatus.SUCCESS, f"Screenshot saved: {output}")

    def open_last(self) -> SystemResponse:
        """Open the newest screenshot."""

        try:
            files = sorted(
                self._default_directory.glob("*.png"),
                key=lambda path: path.stat().st_mtime,
                reverse=True,
            )
        except (OSError, ValueError) as exc:
            logger.exception("Unable to inspect screenshots: %s", exc)
            return SystemResponse(SystemStatus.FAILED, "Unable to inspect screenshots.")

        if not files:
            logger.warning("No screenshots found.")
            return SystemResponse(SystemStatus.FAILED, "No screenshots found.")

        try:
            subprocess.Popen(["explorer", str(files[0])])
        except (OSError, ValueError) as exc:
            logger.exception("Unable to open screenshot %s: %s", files[0], exc)
            return SystemResponse(SystemStatus.FAILED, f"Unable to open screenshot: {files[0]}")

        logger.info("Opened screenshot: %s", files[0].name)
        return SystemResponse(SystemStatus.SUCCESS, f"Opened: {files[0].name}")

    def health_check(self) -> bool:
        try:
            self._default_directory.mkdir(parents=True, exist_ok=True)
            return self._default_directory.exists()
        except (OSError, ValueError) as exc:
            logger.exception("Screenshot Manager health check failed: %s", exc)
            return False