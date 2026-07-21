"""
JARVIS Brightness Manager

Responsibilities
----------------
- Get brightness
- Set brightness
- Increase brightness
- Decrease brightness

Windows only.
"""

from __future__ import annotations

import logging

import screen_brightness_control as sbc

from app.system.models import SystemResponse, SystemStatus

logger = logging.getLogger(__name__)


class BrightnessManager:
    """Windows brightness controller."""

    def get_brightness(self) -> int:
        """Return current brightness percentage."""
        try:
            return int(sbc.get_brightness()[0])
        except (AttributeError, IndexError, OSError, ValueError) as exc:
            logger.warning("Unable to read brightness: %s", exc)
            return 0

    def set_brightness(self, percent: int) -> SystemResponse:
        percent = max(0, min(100, percent))

        try:
            sbc.set_brightness(percent)
        except (AttributeError, OSError, ValueError) as exc:
            logger.exception("Unable to set brightness to %s%%: %s", percent, exc)
            return SystemResponse(SystemStatus.FAILED, f"Unable to set brightness to {percent}%")

        logger.info("Brightness changed to %s%%", percent)
        return SystemResponse(SystemStatus.SUCCESS, f"Brightness set to {percent}%")

    def increase(self, step: int = 10) -> SystemResponse:
        current = self.get_brightness()
        return self.set_brightness(current + step)

    def decrease(self, step: int = 10) -> SystemResponse:
        current = self.get_brightness()
        return self.set_brightness(current - step)

    def health_check(self) -> bool:
        try:
            brightness = self.get_brightness()
            return isinstance(brightness, int) and 0 <= brightness <= 100
        except Exception as exc:  # noqa: BLE001
            logger.exception("Brightness health check failed: %s", exc)
            return False