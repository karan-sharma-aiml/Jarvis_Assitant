from app.agent.agent import Agent
from app.agent.executor import Executor
from app.agent.manager import AgentManager
from app.agent.observer import Observer
from app.agent.planner import Planner
from app.agent.reasoner import Reasoner
from app.agent.reflection import Reflection

from app.tools.calculator import CalculatorTool
from app.tools.manager import ToolManager
from app.tools.registry import ToolRegistry


registry = ToolRegistry()

registry.register(CalculatorTool())

tool_manager = ToolManager(registry)

agent = Agent(
    planner=Planner(),
    reasoner=Reasoner(),
    executor=Executor(tool_manager),
    observer=Observer(),
    reflection=Reflection(),
)

manager = AgentManager(agent)

state = manager.execute(
    "Calculate 250 / 5",
    selected_tool="calculator",
    tool_arguments={
        "expression": "250 / 5"
    }
)

print("=" * 60)

print("Agent Manager Test")

print()

print("Success:")

print(state.success)

print()

print("Tool Result:")

print(state.tool_result)

print()

print("Reflection:")

print(state.metadata["reflection"])

print()

print("Thoughts:")

for thought in state.thoughts:
    print(thought)