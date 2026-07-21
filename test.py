from app.executor.executor import Executor
from app.executor.models import (
    ExecutionRequest,
)
from app.intent.models import (
    Intent,
    IntentName,
)
from app.router.models import ToolRoute


def main():

    print("=" * 65)
    print("PHASE 11.3 - EXECUTOR TEST")
    print("=" * 65)

    executor = Executor()

    assert executor.health_check()

    print("Health:", executor.health_check())

    request = ExecutionRequest(
        intent=Intent(
            name=IntentName.OPEN_APPLICATION,
            entities={
                "application": "notepad",
            },
        ),
        route=ToolRoute(
            manager="ApplicationManager",
            method="open",
        ),
        arguments={
            "application": "notepad",
        },
    )

    result = executor.execute(request)

    print(result)

    assert result.success

    print()

    print("🎉 PHASE 11.3 EXECUTOR PASSED")


if __name__ == "__main__":
    main()