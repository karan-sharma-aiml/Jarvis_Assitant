from app.intent.models import (
    Intent,
    IntentName,
)
from app.router.tool_router import ToolRouter


def main():

    print("=" * 65)
    print("PHASE 11.2 - TOOL ROUTER TEST")
    print("=" * 65)

    router = ToolRouter()

    assert router.health_check()

    print("Health:", router.health_check())
    print("Routes:", router.route_count())
    print()

    intent = Intent(
        name=IntentName.OPEN_APPLICATION,
        entities={
            "application": "vscode",
        },
    )

    route = router.route(intent)

    assert route is not None

    print(route)

    assert route.manager == "ApplicationManager"
    assert route.method == "open"

    assert router.can_route(intent)

    unknown = Intent.unknown("Who is Virat Kohli?")

    assert router.route(unknown) is None

    assert not router.can_route(unknown)

    print()

    print("🎉 PHASE 11.2 TOOL ROUTER PASSED")


if __name__ == "__main__":
    main()