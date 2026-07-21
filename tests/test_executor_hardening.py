from app.executor.executor import Executor
from app.executor.models import ExecutionRequest, ExecutionResult, ExecutionStatus
from app.executor.registry import ManagerRegistry
from app.intent.models import Intent, IntentName, IntentSource
from app.router.models import ToolRoute


def test_executor_returns_failed_result_for_invalid_request() -> None:
    executor = Executor(registry=ManagerRegistry())
    invalid_request = ExecutionRequest(
        intent=None,  # type: ignore[arg-type]
        route=None,  # type: ignore[arg-type]
    )

    result = executor.execute(invalid_request)

    assert isinstance(result, ExecutionResult)
    assert result.status is ExecutionStatus.FAILED
    assert result.failed
    assert result.message


def test_executor_handles_unknown_manager_gracefully() -> None:
    executor = Executor(registry=ManagerRegistry())
    request = ExecutionRequest(
        intent=Intent(
            name=IntentName.CHAT,
            confidence=1.0,
            source=IntentSource.TEXT,
            original_text="hello",
        ),
        route=ToolRoute(manager="MissingManager", method="open"),
    )

    result = executor.execute(request)

    assert result.status is ExecutionStatus.FAILED
    assert "Unknown manager" in result.message
