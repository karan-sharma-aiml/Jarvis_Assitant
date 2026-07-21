from app.jarvis import Jarvis


def main():

    print("=" * 65)
    print("PHASE 11.8 - JARVIS INTEGRATION TEST")
    print("=" * 65)

    jarvis = Jarvis()

    assert jarvis.health_check()

    print(
        "Health:",
        jarvis.health_check(),
    )

    result = jarvis.process(
        "Open Notepad and Take Screenshot"
    )

    print(result)

    print()

    context = jarvis.conversation()

    print(
        "Conversation Messages:",
        context.total_messages,
    )

    assert context.total_messages == 2

    print()

    print("🎉 JARVIS V1 PASSED")


if __name__ == "__main__":
    main()