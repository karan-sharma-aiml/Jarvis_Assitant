"""Continuous listener using voice activity detection."""

from __future__ import annotations

import logging
import tempfile
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
    import webrtcvad
except Exception as error:  # pragma: no cover - runtime fallback
    webrtcvad = None
    _VAD_IMPORT_ERROR = error
else:
    _VAD_IMPORT_ERROR = None

try:
    from scipy.io.wavfile import write
except Exception as error:  # pragma: no cover - runtime fallback
    write = None
    _SCIPY_IMPORT_ERROR = error
else:
    _SCIPY_IMPORT_ERROR = None

logger = logging.getLogger(__name__)


class VoiceListener:
    """Records until silence is detected."""

    def __init__(self, sample_rate: int = 16000) -> None:
        self.sample_rate = sample_rate
        self.vad = None
        self._init_error: Exception | None = None

        if webrtcvad is None:
            self._init_error = _VAD_IMPORT_ERROR
            logger.warning("webrtcvad is unavailable: %s", self._init_error)
            return

        try:
            self.vad = webrtcvad.Vad(2)
        except Exception as error:  # pragma: no cover - runtime fallback
            self._init_error = error
            logger.warning("VAD initialization failed: %s", error)

    def listen(self) -> Path:
        print("🎤 Listening...")

        if sd is None:
            raise RuntimeError("sounddevice is unavailable") from _SOUNDDEVICE_IMPORT_ERROR
        if write is None:
            raise RuntimeError("scipy is unavailable") from _SCIPY_IMPORT_ERROR

        frames: list[np.ndarray] = []
        silence_frames = 0

        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype="int16",
                blocksize=480,
            ) as stream:
                while len(frames) < 50:
                    audio, _ = stream.read(480)
                    frames.append(audio)

                    if self.vad is not None:
                        frame = audio.tobytes()
                        try:
                            if self.vad.is_speech(frame, self.sample_rate):
                                silence_frames = 0
                            else:
                                silence_frames += 1
                        except Exception as error:  # pragma: no cover - runtime fallback
                            logger.warning("VAD processing failed: %s", error)
                            silence_frames += 1

                    if silence_frames > 20:
                        break
        except Exception as error:  # pragma: no cover - runtime fallback
            raise RuntimeError("Microphone input failed") from error

        if not frames:
            raise RuntimeError("No audio frames captured")

        recording = np.concatenate(frames)
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp_path = Path(temp_file.name)
        temp_file.close()

        try:
            write(str(temp_path), self.sample_rate, recording)
        except Exception:
            temp_path.unlink(missing_ok=True)
            raise

        return temp_path