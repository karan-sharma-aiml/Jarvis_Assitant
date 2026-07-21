"""
JARVIS File Manager

Responsibilities
----------------
- Open folders
- Create folders
- Create files
- Delete files/folders
- Rename
- Copy
- Move
- List directory contents

Uses only Python standard library.
"""

from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path

from app.system.models import SystemResponse, SystemStatus

logger = logging.getLogger(__name__)


SPECIAL_FOLDERS = {
    "desktop": Path.home() / "Desktop",
    "downloads": Path.home() / "Downloads",
    "documents": Path.home() / "Documents",
    "pictures": Path.home() / "Pictures",
    "videos": Path.home() / "Videos",
    "music": Path.home() / "Music",
}


class FileManager:
    """Manage files and folders."""

    def _resolve(self, path: str | Path) -> Path:
        if isinstance(path, Path):
            return path.expanduser().resolve()

        raw_path = str(path).strip()

        if not raw_path:
            return Path.cwd().resolve()

        key = raw_path.lower()
        if key in SPECIAL_FOLDERS:
            return SPECIAL_FOLDERS[key].expanduser().resolve()

        return Path(raw_path).expanduser().resolve()

    def open_folder(self, path: str) -> SystemResponse:
        folder = self._resolve(path)

        if not folder.exists():
            logger.warning("Folder not found: %s", folder)
            return SystemResponse(SystemStatus.FAILED, f"Folder not found: {folder}")

        try:
            subprocess.Popen(["explorer", str(folder)])
        except (OSError, ValueError) as exc:
            logger.exception("Unable to open folder %s: %s", folder, exc)
            return SystemResponse(SystemStatus.FAILED, f"Unable to open folder: {folder}")

        logger.info("Opened folder: %s", folder)
        return SystemResponse(SystemStatus.SUCCESS, f"Opened folder: {folder}")

    def create_folder(self, path: str) -> SystemResponse:
        folder = self._resolve(path)

        try:
            folder.mkdir(parents=True, exist_ok=True)
        except (OSError, ValueError) as exc:
            logger.exception("Unable to create folder %s: %s", folder, exc)
            return SystemResponse(SystemStatus.FAILED, f"Unable to create folder: {folder}")

        logger.info("Folder created: %s", folder)
        return SystemResponse(SystemStatus.SUCCESS, f"Folder created: {folder}")

    def create_file(self, path: str) -> SystemResponse:
        file_path = self._resolve(path)

        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch(exist_ok=True)
        except (OSError, ValueError) as exc:
            logger.exception("Unable to create file %s: %s", file_path, exc)
            return SystemResponse(SystemStatus.FAILED, f"Unable to create file: {file_path}")

        logger.info("File created: %s", file_path)
        return SystemResponse(SystemStatus.SUCCESS, f"File created: {file_path}")

    def delete(self, path: str) -> SystemResponse:
        target = self._resolve(path)

        if not target.exists():
            logger.warning("Path does not exist: %s", target)
            return SystemResponse(SystemStatus.FAILED, "Path does not exist.")

        try:
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
        except (OSError, shutil.Error, ValueError) as exc:
            logger.exception("Unable to delete path %s: %s", target, exc)
            return SystemResponse(SystemStatus.FAILED, f"Unable to delete path: {target}")

        logger.info("Path deleted: %s", target)
        return SystemResponse(SystemStatus.SUCCESS, f"Deleted: {target}")

    def rename(self, source: str, destination: str) -> SystemResponse:
        src = self._resolve(source)
        dst = self._resolve(destination)

        if dst.exists():
            logger.warning("Destination already exists: %s", dst)
            return SystemResponse(SystemStatus.FAILED, "Destination already exists.")

        try:
            src.rename(dst)
        except (FileNotFoundError, OSError, ValueError) as exc:
            logger.exception("Unable to rename %s to %s: %s", src, dst, exc)
            return SystemResponse(SystemStatus.FAILED, f"Unable to rename {src} to {dst}")

        logger.info("Path renamed to: %s", dst)
        return SystemResponse(SystemStatus.SUCCESS, f"Renamed to {dst.name}")

    def copy(self, source: str, destination: str) -> SystemResponse:
        src = self._resolve(source)
        dst = self._resolve(destination)

        try:
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
        except (FileNotFoundError, OSError, shutil.Error, ValueError) as exc:
            logger.exception("Unable to copy %s to %s: %s", src, dst, exc)
            return SystemResponse(SystemStatus.FAILED, f"Unable to copy {src} to {dst}")

        logger.info("Path copied to: %s", dst)
        return SystemResponse(SystemStatus.SUCCESS, f"Copied to {dst}")

    def move(self, source: str, destination: str) -> SystemResponse:
        src = self._resolve(source)
        dst = self._resolve(destination)

        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
        except (FileNotFoundError, OSError, shutil.Error, ValueError) as exc:
            logger.exception("Unable to move %s to %s: %s", src, dst, exc)
            return SystemResponse(SystemStatus.FAILED, f"Unable to move {src} to {dst}")

        logger.info("Path moved to: %s", dst)
        return SystemResponse(SystemStatus.SUCCESS, f"Moved to {dst}")

    def exists(self, path: str) -> bool:
        try:
            return self._resolve(path).exists()
        except (OSError, ValueError) as exc:
            logger.warning("Unable to check path existence for %s: %s", path, exc)
            return False

    def list_directory(self, path: str) -> list[str]:
        folder = self._resolve(path)

        if not folder.exists():
            return []

        try:
            return sorted(item.name for item in folder.iterdir())
        except (OSError, ValueError) as exc:
            logger.warning("Unable to list directory %s: %s", folder, exc)
            return []

    def health_check(self) -> bool:
        try:
            return self._resolve("~").exists()
        except (OSError, ValueError) as exc:
            logger.exception("File Manager health check failed: %s", exc)
            return False