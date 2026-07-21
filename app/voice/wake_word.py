"""Wake word detection with graceful fallback."""

from __future__ import annotations

import logging

try:
    import numpy as np
except Exception:  # pragma: no cover - runtime fallback
    np = None

try:
    import sounddevice as sd
except Exception as error:  # pragma: no cover - runtime fallback
    sd = None
    _SOUNDDEVICE_IMPORT_ERROR = error
else:
    _SOUNDDEVICE_IMPORT_ERROR = None

try:
    from openwakeword.model import Model
except Exception as error:  # pragma: no cover - runtime fallback
    Model = None
    _WAKEWORD_IMPORT_ERROR = error
else:
    _WAKEWORD_IMPORT_ERROR = None

logger = logging.getLogger(__name__)


class WakeWordDetector:
    """Detects the wake word."""

    def __init__(
        self,
        wakeword: str = "jarvis",
        sample_rate: int = 16000,
        chunk_size: int = 1280,
    ) -> None:
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.wakeword = wakeword
        self.model = None

        if Model is None:
            logger.warning("Wake-word dependency unavailable: %s", _WAKEWORD_IMPORT_ERROR)
            return

        try:
            self.model = Model(wakeword_models=[wakeword])
        except Exception as error:  # pragma: no cover - runtime fallback
            logger.warning("Falling back to passive wake-word mode: %s", error)
            self.model = None

    def wait_for_wake_word(self) -> None:
        """Block until wake word is detected or fallback mode is used."""
        print("🎤 Waiting for wake word...")

        if self.model is None:
            print("⚠️ Wake-word model unavailable; continuing in fallback mode")
            return

        if sd is None:
            print("⚠️ sounddevice unavailable; continuing in fallback mode")
            return

        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype="int16",
                blocksize=self.chunk_size,
            ) as stream:
                while True:
                    audio, _ = stream.read(self.chunk_size)
                    prediction = self.model.predict(audio.flatten())

                    if prediction.get(self.wakeword, 0) > 0.5:
                        print("✅ Wake word detected")
                        return
        except Exception as error:  # pragma: no cover - runtime fallback
            logger.warning("Wake-word listening failed: %s", error)
            print("⚠️ Wake-word listening interrupted; continuing in fallback mode")