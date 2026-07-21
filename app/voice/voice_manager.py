"""
JARVIS Voice Manager

Responsibilities
----------------
- Coordinate the complete voice pipeline.
- Listen to the user.
- Convert speech to text.
- Send text to ConversationManager.
- Speak the AI response.

Contains NO business logic.

Contains NO LLM implementation.

Contains NO memory implementation.
"""

from __future__ import annotations

import logging

from app.conversation.conversation_manager import ConversationManager
from app.voice.listener import VoiceListener
from app.voice.speech_to_text import SpeechToText
from app.voice.text_to_speech import TextToSpeech
from app.voice.wake_word import WakeWordDetector

logger = logging.getLogger(__name__)


class VoiceManager:
    """
    Coordinates the complete voice pipeline.
    """

    def __init__(
        self,
        conversation_manager: ConversationManager | None = None,
        stt: SpeechToText | None = None,
        tts: TextToSpeech | None = None,
        listener: VoiceListener | None = None,
        wake_word: WakeWordDetector | None = None,
        use_wake_word: bool = False,
    ) -> None:

        self._conversation = conversation_manager or ConversationManager()

        self._stt = stt or SpeechToText()

        self._tts = tts or TextToSpeech()

        self._listener = listener or VoiceListener()

        self._wake_word = wake_word or WakeWordDetector()

        self._use_wake_word = use_wake_word

        self._running = False

    @property
    def running(self) -> bool:
        return self._running

    def listen_once(self) -> str:
        """
        Listen once and return recognized text.
        """

        if self._use_wake_word:
            self._wake_word.wait_for_wake_word()

        audio_file = self._listener.listen()

        result = self._stt.transcribe(audio_file)

        return result.text.strip()

    def speak(self, text: str) -> None:
        """
        Speak one response.
        """

        if not text.strip():
            return

        self._tts.say(text)

    def process_once(self) -> None:
        """
        Execute one conversation turn.
        """

        user_text = self.listen_once()

        if not user_text:
            logger.info("No speech detected.")
            return

        print(f"\n🧑 You : {user_text}")

        response = self._conversation.chat(user_text)

        print(f"\n🤖 Jarvis : {response}")

        self.speak(response)

    def start(self) -> None:
        """
        Continuous voice assistant.
        """

        self._running = True

        logger.info("Voice assistant started.")

        print("\n========== JARVIS ==========")
        print("Press Ctrl+C to stop.\n")

        try:

            while self._running:

                self.process_once()

        except KeyboardInterrupt:

            print("\nStopping JARVIS...")

        finally:

            self.stop()

    def stop(self) -> None:
        """
        Stop assistant.
        """

        self._running = False

        self._tts.stop()

        logger.info("Voice assistant stopped.")