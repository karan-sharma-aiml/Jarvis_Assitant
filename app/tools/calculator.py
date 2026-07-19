"""
JARVIS Calculator Tool

Safely evaluates mathematical expressions.

Supported:
- +, -, *, /, //, %, **
- Parentheses
- Unary + and -

Unsafe operations such as imports, variables,
function calls, and attribute access are blocked.
"""

from __future__ import annotations

import ast
import operator
from typing import Any

from app.tools.base import BaseTool
from app.tools.exceptions import (
    ToolExecutionError,
    ToolValidationError,
)
from app.tools.models import ToolCategory


_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


class CalculatorTool(BaseTool):
    """
    Safe calculator tool.
    """

    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return "Evaluate mathematical expressions."

    @property
    def category(self) -> ToolCategory:
        return ToolCategory.UTILITY

    def validate(self, **kwargs: Any) -> None:
        expression = kwargs.get("expression")

        if expression is None:
            raise ToolValidationError(
                "Missing required argument: expression"
            )

        if not isinstance(expression, str):
            raise ToolValidationError(
                "Expression must be a string."
            )

        if not expression.strip():
            raise ToolValidationError(
                "Expression cannot be empty."
            )

    def execute(self, **kwargs: Any) -> float | int:
        """
        Execute calculator.
        """
        self.validate(**kwargs)

        expression: str = kwargs["expression"]

        try:
            tree = ast.parse(
                expression,
                mode="eval",
            )

            return self._evaluate(tree.body)

        except ToolValidationError:
            raise

        except Exception as error:
            raise ToolExecutionError(
                f"Invalid expression: {expression}"
            ) from error

    def _evaluate(
        self,
        node: ast.AST,
    ) -> float | int:

        if isinstance(node, ast.Constant):

            if not isinstance(node.value, (int, float)):
                raise ToolValidationError(
                    "Only numeric values are allowed."
                )

            return node.value

        if isinstance(node, ast.BinOp):

            operator_fn = _ALLOWED_OPERATORS.get(type(node.op))

            if operator_fn is None:
                raise ToolValidationError(
                    "Operator is not supported."
                )

            return operator_fn(
                self._evaluate(node.left),
                self._evaluate(node.right),
            )

        if isinstance(node, ast.UnaryOp):

            operator_fn = _ALLOWED_OPERATORS.get(type(node.op))

            if operator_fn is None:
                raise ToolValidationError(
                    "Unary operator not supported."
                )

            return operator_fn(
                self._evaluate(node.operand)
            )

        raise ToolValidationError(
            "Unsupported mathematical expression."
        )