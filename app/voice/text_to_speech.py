"""Text-to-Speech module."""

from __future__ import annotations

import asyncio
import logging
import tempfile
from pathlib import Path

try:
    import edge_tts
except Exception as error:  # pragma: no cover - runtime fallback
    edge_tts = None
    _EDGE_TTS_IMPORT_ERROR = error
else:
    _EDGE_TTS_IMPORT_ERROR = None

from app.voice.speaker import Speaker

logger = logging.getLogger(__name__)


class TextToSpeech:
    """
    Microsoft Edge TTS wrapper.
    """

    def __init__(
        self,
        voice: str = "en-US-AndrewNeural",
        rate: str = "+0%",
        volume: str = "+0%",
    ) -> None:

        self.voice = voice
        self.rate = rate
        self.volume = volume

        self.speaker = Speaker()

    async def _generate_audio(
        self,
        text: str,
    ) -> Path:
        if edge_tts is None:
            raise RuntimeError("edge-tts is unavailable") from _EDGE_TTS_IMPORT_ERROR

        with tempfile.NamedTemporaryFile(
            suffix=".mp3",
            delete=False,
        ) as output:
            temp_path = Path(output.name)

            communicate = edge_tts.Communicate(
                text=text,
                voice=self.voice,
                rate=self.rate,
                volume=self.volume,
            )

            await communicate.save(str(temp_path))

        return temp_path

    async def speak(
        self,
        text: str,
    ) -> None:

        if not text.strip():
            return

        try:
            audio = await self._generate_audio(text)
        except Exception as error:  # pragma: no cover - runtime fallback
            logger.warning("Text-to-speech generation failed: %s", error)
            return

        try:
            self.speaker.play(str(audio))
        finally:
            try:
                audio.unlink(missing_ok=True)
            except PermissionError:
                pass

    def say(
        self,
        text: str,
    ) -> None:

        asyncio.run(self.speak(text))

    def stop(self) -> None:
        self.speaker.stop()

    @property
    def is_speaking(self) -> bool:
        return self.speaker.is_speaking