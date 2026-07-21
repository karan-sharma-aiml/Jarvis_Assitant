"""Speech-to-Text module."""

from __future__ import annotations

import logging
import tempfile
import time
from pathlib import Path

import numpy as np

try:
    import sounddevice as sd
except Exception as error:  # pragma: no cover - runtime fallback
    sd = None
    _SOUNDDEVICE_IMPORT_ERROR = error
else:
    _SOUNDDEVICE_IMPORT_ERROR = None

try:
    from scipy.io.wavfile import write
except Exception as error:  # pragma: no cover - runtime fallback
    write = None
    _SCIPY_IMPORT_ERROR = error
else:
    _SCIPY_IMPORT_ERROR = None

try:
    from faster_whisper import WhisperModel
except Exception as error:  # pragma: no cover - runtime fallback
    WhisperModel = None
    _WHISPER_IMPORT_ERROR = error
else:
    _WHISPER_IMPORT_ERROR = None

from app.voice.models import TranscriptionResult

logger = logging.getLogger(__name__)


class SpeechToText:
    """Offline Speech-to-Text using Faster Whisper."""

    def __init__(
        self,
        model_name: str = "base",
        sample_rate: int = 16000,
    ) -> None:
        self.sample_rate = sample_rate
        self.model = None
        self._init_error: Exception | None = None

        if WhisperModel is None:
            self._init_error = _WHISPER_IMPORT_ERROR
            logger.warning("faster-whisper is unavailable: %s", self._init_error)
            return

        try:
            self.model = WhisperModel(
                model_name,
                device="cpu",
                compute_type="int8",
            )
        except Exception as error:  # pragma: no cover - runtime fallback
            self._init_error = error
            logger.warning("Whisper model initialization failed: %s", error)

    def record_audio(self, duration: int = 5) -> Path:
        """Record microphone audio to a temporary WAV file."""
        if sd is None:
            raise RuntimeError("sounddevice is unavailable") from _SOUNDDEVICE_IMPORT_ERROR
        if write is None:
            raise RuntimeError("scipy is unavailable") from _SCIPY_IMPORT_ERROR

        print(f"🎤 Listening for {duration} seconds...")

        try:
            audio = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype=np.int16,
            )
            sd.wait()
        except Exception as error:  # pragma: no cover - runtime fallback
            raise RuntimeError("Microphone recording failed") from error

        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp_path = Path(temp_file.name)
        temp_file.close()

        try:
            write(str(temp_path), self.sample_rate, audio)
        except Exception:
            temp_path.unlink(missing_ok=True)
            raise

        return temp_path

    def transcribe(self, duration: int = 5) -> TranscriptionResult:
        """Record and transcribe microphone speech."""
        start = time.time()

        if self.model is None:
            return TranscriptionResult(text="", language="", duration=time.time() - start)

        audio_file = self.record_audio(duration)

        try:
            segments, info = self.model.transcribe(str(audio_file))
            text = " ".join(segment.text.strip() for segment in segments)
            elapsed = time.time() - start
            return TranscriptionResult(text=text, language=info.language, duration=elapsed)
        finally:
            try:
                audio_file.unlink(missing_ok=True)
            except PermissionError:
                pass
