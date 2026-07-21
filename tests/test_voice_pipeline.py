"""
End-to-end integration test for the Voice module.
"""

from __future__ import annotations

import traceback

from app.voice.speech_to_text import SpeechToText
from app.voice.text_to_speech import TextToSpeech
from app.voice.listener import VoiceListener
from app.voice.wake_word import WakeWordDetector


def run_test(name: str, func):
    print(f"\n{name}")
    print("-" * 40)

    try:
        func()
        print("PASS")
    except Exception as error:
        print("FAIL")
        print(type(error).__name__, error)
        traceback.print_exc()


def test_imports():

    print("All voice modules imported successfully.")


def test_stt():

    stt = SpeechToText()

    print("SpeechToText initialized successfully.")

    assert stt is not None


def test_tts():

    tts = TextToSpeech()

    print("Speaking test...")

    tts.say("Hello Karan. Voice module is working.")

    assert tts is not None


def test_listener():

    listener = VoiceListener()

    print("Speak for a few seconds...")

    audio = listener.listen()

    print("Audio File:", audio)

    assert audio.exists()


def test_wake_word():

    detector = WakeWordDetector()

    print("Waiting for wake word...")

    detector.wait_for_wake_word()

    print("Wake-word module completed.")

    assert detector is not None


def main():

    print("=" * 60)
    print("JARVIS Voice Module Integration Test")
    print("=" * 60)

    run_test("1. Imports", test_imports)

    run_test("2. Speech To Text", test_stt)

    run_test("3. Text To Speech", test_tts)

    run_test("4. Listener", test_listener)

    run_test("5. Wake Word", test_wake_word)

    print("\n" + "=" * 60)
    print("Voice Module Test Completed")
    print("=" * 60)


if __name__ == "__main__":
    main()