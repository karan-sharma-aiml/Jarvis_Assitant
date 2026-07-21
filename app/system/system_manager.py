"""
JARVIS System Manager

Public entry point for Windows automation.

Responsibilities
----------------
- Coordinate Windows automation managers.
- Expose a stable public API.
- Perform health checks.

Contains NO Windows-specific implementation.
Contains NO business logic.
"""

from __future__ import annotations

import logging

from app.system.application_manager import ApplicationManager
from app.system.brightness_manager import BrightnessManager
from app.system.clipboard_manager import ClipboardManager
from app.system.file_manager import FileManager
from app.system.models import SystemResponse
from app.system.screenshot_manager import ScreenshotManager
from app.system.power_manager import PowerManager
from app.system.volume_manager import VolumeManager

logger = logging.getLogger(__name__)


class SystemManager:
    """
    Central coordinator for Windows automation.
    """

    def __init__(
        self,
        application_manager: ApplicationManager | None = None,
        file_manager: FileManager | None = None,
        volume_manager: VolumeManager | None = None,
        brightness_manager: BrightnessManager | None = None,
        clipboard_manager: ClipboardManager | None = None,
        power_manager: PowerManager | None = None,
        screenshot_manager: ScreenshotManager | None = None,
    ) -> None:

        self._applications = (
            application_manager or ApplicationManager()
        )

        self._files = (
            file_manager or FileManager()
        )

        self._volume = (
            volume_manager or VolumeManager()
        )

        self._brightness = (
            brightness_manager or BrightnessManager()
        )

        self._clipboard = (
            clipboard_manager or ClipboardManager()
        )

        self._screenshot = (
            screenshot_manager or ScreenshotManager()
        )

        self._power = (
            power_manager or PowerManager()
        )

        logger.info("System Manager initialized.")

    # ==================================================
    # Properties
    # ==================================================

    @property
    def applications(self) -> ApplicationManager:
        return self._applications

    @property
    def files(self) -> FileManager:
        return self._files

    @property
    def volume(self) -> VolumeManager:
        return self._volume

    @property
    def brightness(self) -> BrightnessManager:
        return self._brightness

    @property
    def clipboard(self) -> ClipboardManager:
        return self._clipboard

    @property
    def screenshot(self) -> ScreenshotManager:
        return self._screenshot
    
    @property
    def power(self) -> PowerManager:
        return self._power
    

    # ==================================================
    # Application Management
    # ==================================================

    def open_application(
        self,
        application: str,
    ) -> SystemResponse:
        return self._applications.open(application)

    def close_application(
        self,
        application: str,
    ) -> SystemResponse:
        return self._applications.close(application)

    def application_running(
        self,
        application: str,
    ) -> bool:
        return self._applications.is_running(application)

    def running_applications(
        self,
    ) -> list[str]:
        return self._applications.list_running()

    # ==================================================
    # File Management
    # ==================================================

    def open_folder(
        self,
        path: str,
    ) -> SystemResponse:
        return self._files.open_folder(path)

    def create_folder(
        self,
        path: str,
    ) -> SystemResponse:
        return self._files.create_folder(path)

    def create_file(
        self,
        path: str,
    ) -> SystemResponse:
        return self._files.create_file(path)

    def delete_path(
        self,
        path: str,
    ) -> SystemResponse:
        return self._files.delete(path)

    def rename_path(
        self,
        source: str,
        destination: str,
    ) -> SystemResponse:
        return self._files.rename(
            source,
            destination,
        )

    def copy_path(
        self,
        source: str,
        destination: str,
    ) -> SystemResponse:
        return self._files.copy(
            source,
            destination,
        )

    def move_path(
        self,
        source: str,
        destination: str,
    ) -> SystemResponse:
        return self._files.move(
            source,
            destination,
        )

    def path_exists(
        self,
        path: str,
    ) -> bool:
        return self._files.exists(path)

    def list_directory(
        self,
        path: str,
    ) -> list[str]:
        return self._files.list_directory(path)

    # ==================================================
    # Volume Management
    # ==================================================

    def get_volume(
        self,
    ) -> int:
        return self._volume.get_volume()

    def set_volume(
        self,
        percent: int,
    ) -> SystemResponse:
        return self._volume.set_volume(percent)

    def increase_volume(
        self,
        step: int = 10,
    ) -> SystemResponse:
        return self._volume.increase(step)

    def decrease_volume(
        self,
        step: int = 10,
    ) -> SystemResponse:
        return self._volume.decrease(step)

    def mute(
        self,
    ) -> SystemResponse:
        return self._volume.mute()

    def unmute(
        self,
    ) -> SystemResponse:
        return self._volume.unmute()

    def is_muted(
        self,
    ) -> bool:
        return self._volume.is_muted()

    # ==================================================
    # Brightness Management
    # ==================================================

    def get_brightness(
        self,
    ) -> int:
        return self._brightness.get_brightness()

    def set_brightness(
        self,
        percent: int,
    ) -> SystemResponse:
        return self._brightness.set_brightness(percent)

    def increase_brightness(
        self,
        step: int = 10,
    ) -> SystemResponse:
        return self._brightness.increase(step)

    def decrease_brightness(
        self,
        step: int = 10,
    ) -> SystemResponse:
        return self._brightness.decrease(step)

    # ==================================================
    # Clipboard Management
    # ==================================================

    def copy_text(
        self,
        text: str,
    ) -> SystemResponse:
        return self._clipboard.copy(text)

    def paste_text(
        self,
    ) -> str:
        return self._clipboard.paste()

    def clear_clipboard(
        self,
    ) -> SystemResponse:
        return self._clipboard.clear()

    def clipboard_has_text(
        self,
    ) -> bool:
        return self._clipboard.has_text()

    # ==================================================
    # Screenshot Management
    # ==================================================

    def take_screenshot(
        self,
        save_directory: str | None = None,
    ) -> SystemResponse:
        return self._screenshot.take_screenshot(
            save_directory
        )

    def open_last_screenshot(
        self,
    ) -> SystemResponse:
        return self._screenshot.open_last()

    # ==================================================
     
    # ==================================================
    # Power Management
    # ==================================================
    
    def shutdown(
        self,
        delay: int = 0,
        dry_run: bool = False,
    ) -> SystemResponse:
        return self._power.shutdown(delay, dry_run)

    def restart(
        self,
        delay: int = 0,
        dry_run: bool = False,
    ) -> SystemResponse:
        return self._power.restart(delay, dry_run)

    def sleep(
        self,
        dry_run: bool = False,
    ) -> SystemResponse:
        return self._power.sleep(dry_run)

    def hibernate(
        self,
        dry_run: bool = False,
    ) -> SystemResponse:
        return self._power.hibernate(dry_run)

    def lock(
        self,
        dry_run: bool = False,
    ) -> SystemResponse:
        return self._power.lock(dry_run)

    def logoff(
        self,
        dry_run: bool = False,
    ) -> SystemResponse:
        return self._power.logoff(dry_run)

    def cancel_shutdown(
        self,
    ) -> SystemResponse:
        return self._power.cancel_shutdown()

     


    # ==================================================
    # Health
    # ==================================================

    def health_check(
        self,
    ) -> bool:

        try:

            return (
                self._applications.health_check()
                and self._files.health_check()
                and self._volume.health_check()
                and self._brightness.health_check()
                and self._clipboard.health_check()
                and self._screenshot.health_check()
                and self._power.health_check()
            )

        except Exception as error:

            logger.exception(
                "System Manager health check failed: %s",
                error,
            )

            return False

    # ==================================================
    # Representation
    # ==================================================

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}("
            f"applications={self._applications.__class__.__name__}, "
            f"files={self._files.__class__.__name__}, "
            f"volume={self._volume.__class__.__name__}, "
            f"brightness={self._brightness.__class__.__name__}, "
            f"clipboard={self._clipboard.__class__.__name__}, "
            f"screenshot={self._screenshot.__class__.__name__}, "
            f"power={self._power.__class__.__name__})"
        )