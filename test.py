"""
Integration Test

JARVIS Context Engine
"""

from app.context.manager import ContextManager


def main() -> None:

    manager = ContextManager()

    context = manager.create_context(
        user_input="Explain Artificial Intelligence",

        conversation_context=[
            "User greeted JARVIS.",
            "User wants to learn AI.",
        ],

        working_memory={
            "current_topic": "AI",
        },

        semantic_memory=[
            "User is a B.Tech AIML student.",
        ],

        episodic_memory=[
            "User completed Phase 7.",
        ],

        preferences={
            "language": "English",
            "response_style": "Detailed",
        },

        knowledge_context=[
            "Artificial Intelligence is the simulation of human intelligence.",
        ],

        metadata={
            "session": "phase_8_demo",
            "source": "integration_test",
        },
    )

    print("=" * 60)

    print("User Input")
    print("-" * 60)
    print(context.user_input)

    print()

    print("Conversation")
    print("-" * 60)
    print(context.conversation_context)

    print()

    print("Working Memory")
    print("-" * 60)
    print(context.working_memory)

    print()

    print("Semantic Memory")
    print("-" * 60)
    print(context.semantic_memory)

    print()

    print("Episodic Memory")
    print("-" * 60)
    print(context.episodic_memory)

    print()

    print("Preferences")
    print("-" * 60)
    print(context.preferences)

    print()

    print("Knowledge Context")
    print("-" * 60)
    print(context.knowledge_context)

    print()

    print("Metadata")
    print("-" * 60)
    print(context.metadata)

    print()

    print("Timestamp")
    print("-" * 60)
    print(context.timestamp)

    print()

    print("Health")
    print("-" * 60)
    print("Has Memory :", context.has_memory)
    print("Has Knowledge :", context.has_knowledge)
    print("Is Empty :", context.is_empty)

    print()

    print("=" * 60)
    print("Context Engine Integration Test Passed")
    print("=" * 60)


if __name__ == "__main__":
    main()