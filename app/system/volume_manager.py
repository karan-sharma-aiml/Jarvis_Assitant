"""
JARVIS Volume Manager

Responsibilities
----------------
- Set system volume
- Increase volume
- Decrease volume
- Mute
- Unmute
- Query current volume

Windows only.
"""

from __future__ import annotations

import logging

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from app.system.models import SystemResponse, SystemStatus

logger = logging.getLogger(__name__)


class VolumeManager:
    """Control Windows master volume."""

    def __init__(self) -> None:
        self._volume = None
        self._available = False

        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_,
                CLSCTX_ALL,
                None,
            )
            self._volume = interface.QueryInterface(IAudioEndpointVolume)
            self._available = True
        except (AttributeError, OSError, ValueError) as exc:
            logger.exception("Volume Manager initialization failed: %s", exc)

    def get_volume(self) -> int:
        if self._volume is None:
            logger.warning("Volume control is unavailable.")
            return 0

        try:
            level = self._volume.GetMasterVolumeLevelScalar()
            return round(level * 100)
        except (AttributeError, OSError, ValueError) as exc:
            logger.warning("Unable to read volume: %s", exc)
            return 0

    def set_volume(self, percent: int) -> SystemResponse:
        percent = max(0, min(100, percent))

        if self._volume is None:
            logger.warning("Volume control is unavailable.")
            return SystemResponse(SystemStatus.FAILED, "Volume control is unavailable.")

        try:
            self._volume.SetMasterVolumeLevelScalar(percent / 100, None)
        except (AttributeError, OSError, ValueError) as exc:
            logger.exception("Unable to set volume to %s%%: %s", percent, exc)
            return SystemResponse(SystemStatus.FAILED, f"Unable to set volume to {percent}%")

        logger.info("Volume changed to %s%%", percent)
        return SystemResponse(SystemStatus.SUCCESS, f"Volume set to {percent}%")

    def increase(self, step: int = 10) -> SystemResponse:
        current = self.get_volume()
        return self.set_volume(current + step)

    def decrease(self, step: int = 10) -> SystemResponse:
        current = self.get_volume()
        return self.set_volume(current - step)

    def mute(self) -> SystemResponse:
        if self._volume is None:
            logger.warning("Volume control is unavailable.")
            return SystemResponse(SystemStatus.FAILED, "Volume control is unavailable.")

        try:
            self._volume.SetMute(1, None)
        except (AttributeError, OSError, ValueError) as exc:
            logger.exception("Unable to mute volume: %s", exc)
            return SystemResponse(SystemStatus.FAILED, "Unable to mute volume.")

        logger.info("Volume muted.")
        return SystemResponse(SystemStatus.SUCCESS, "Volume muted.")

    def unmute(self) -> SystemResponse:
        if self._volume is None:
            logger.warning("Volume control is unavailable.")
            return SystemResponse(SystemStatus.FAILED, "Volume control is unavailable.")

        try:
            self._volume.SetMute(0, None)
        except (AttributeError, OSError, ValueError) as exc:
            logger.exception("Unable to unmute volume: %s", exc)
            return SystemResponse(SystemStatus.FAILED, "Unable to unmute volume.")

        logger.info("Volume unmuted.")
        return SystemResponse(SystemStatus.SUCCESS, "Volume unmuted.")

    def is_muted(self) -> bool:
        if self._volume is None:
            return False

        try:
            return bool(self._volume.GetMute())
        except (AttributeError, OSError, ValueError) as exc:
            logger.warning("Unable to query mute state: %s", exc)
            return False

    def health_check(self) -> bool:
        try:
            return self._available and isinstance(self.get_volume(), int)
        except Exception as exc:  # noqa: BLE001
            logger.exception("Volume Manager health check failed: %s", exc)
            return False