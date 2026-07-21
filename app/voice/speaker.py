"""Audio playback helper."""

from __future__ import annotations

import logging

try:
    import pygame
except Exception as error:  # pragma: no cover - runtime fallback
    pygame = None
    _PYGAME_IMPORT_ERROR = error
else:
    _PYGAME_IMPORT_ERROR = None

logger = logging.getLogger(__name__)


class Speaker:
    """Handles audio playback."""

    def __init__(self) -> None:
        self._available = False
        self._init_error: Exception | None = None

        if pygame is None:
            self._init_error = _PYGAME_IMPORT_ERROR
            logger.warning("pygame is unavailable: %s", self._init_error)
            return

        try:
            pygame.mixer.init()
        except Exception as error:  # pragma: no cover - runtime fallback
            self._init_error = error
            logger.warning("pygame mixer initialization failed: %s", error)
            return

        self._available = True

    def play(self, file_path: str) -> None:
        if not self._available or pygame is None:
            return

        if not file_path:
            return

        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as error:  # pragma: no cover - runtime fallback
            logger.warning("Audio playback failed: %s", error)
        finally:
            self._stop_internal()

    def stop(self) -> None:
        if not self._available or pygame is None:
            return
        self._stop_internal()

    def _stop_internal(self) -> None:
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        except Exception:  # pragma: no cover - runtime fallback
            pass

    def close(self) -> None:
        if not self._available or pygame is None:
            return
        try:
            pygame.mixer.quit()
        except Exception:  # pragma: no cover - runtime fallback
            pass
        self._available = False

    @property
    def is_speaking(self) -> bool:
        if not self._available or pygame is None:
            return False
        try:
            return bool(pygame.mixer.music.get_busy())
        except Exception:  # pragma: no cover - runtime fallback
            return False