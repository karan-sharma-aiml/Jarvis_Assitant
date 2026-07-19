"""Tool models used by the tool-calling engine.

This module contains lightweight Pydantic models that describe tool
metadata, requests, and responses. Models intentionally contain NO
business logic — only minimal validation and typing to make the rest of the
system safer and easier to use.

Design constraints and decisions:
- Keep the public fields and names unchanged for backward compatibility.
- Make models lightweight and friendly to ORMs/serializers by enabling
  ``orm_mode`` and ``validate_assignment``.
- Provide minimal field validation (non-empty strings) but avoid strict
  semantic checks (e.g. full semver parsing) to prevent breaking existing
  callers.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Mapping, Optional

from pydantic import BaseModel, Field, validator, ConfigDict


class ToolCategory(StrEnum):
    """Categories used to organize tools."""

    SYSTEM = "system"
    FILESYSTEM = "filesystem"
    TERMINAL = "terminal"
    SEARCH = "search"
    WEB = "web"
    COMMUNICATION = "communication"
    PRODUCTIVITY = "productivity"
    UTILITY = "utility"


class ToolExecutionStatus(StrEnum):
    """Execution result status."""

    SUCCESS = "success"
    FAILED = "failed"
    VALIDATION_ERROR = "validation_error"
    UNAVAILABLE = "unavailable"


class ToolMetadata(BaseModel):
    """Static information about a tool.

    Fields:
    - ``name``: unique, short identifier for the tool (non-empty)
    - ``description``: short human-friendly description (non-empty)
    - ``category``: see :class:`ToolCategory`
    - ``version``: free-form version string (defaults to ``1.0.0``)
    - ``enabled``: whether the tool is enabled

    Keep validation minimal to avoid breaking existing metadata producers.
    """

    name: str = Field(..., description="Unique tool identifier")
    description: str = Field(..., description="Human-friendly description")
    category: ToolCategory = Field(..., description="Tool category")
    version: str = Field("1.0.0", description="Tool implementation version")
    enabled: bool = Field(True, description="Whether the tool is enabled")

    @validator("name", "description")
    def _non_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("must be a non-empty string")
        return value

    model_config = ConfigDict(from_attributes=True, validate_assignment=True)


class ToolRequest(BaseModel):
    """Request passed to a tool.

    Fields:
    - ``tool_name``: name of the tool to execute (non-empty)
    - ``arguments``: mapping of argument names to values
    """

    tool_name: str = Field(..., description="Target tool name")
    arguments: dict[str, Any] = Field(default_factory=dict, description="Tool arguments")

    @validator("tool_name")
    def _tool_name_non_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("tool_name must be a non-empty string")
        return value

    model_config = ConfigDict(from_attributes=True, validate_assignment=True)


class ToolResponse(BaseModel):
    """Response returned by a tool.

    Fields:
    - ``tool_name``: the tool that produced this response
    - ``status``: execution status from :class:`ToolExecutionStatus`
    - ``output``: optional arbitrary output data
    - ``error``: optional human-readable error message
    - ``metadata``: optional additional metadata
    """

    tool_name: str = Field(..., description="Tool that produced the response")
    status: ToolExecutionStatus = Field(..., description="Execution status")
    output: Any | None = Field(None, description="Tool output")
    error: Optional[str] = Field(None, description="Optional error message")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Response metadata")

    @validator("tool_name")
    def _response_tool_name_non_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("tool_name must be a non-empty string")
        return value

    model_config = ConfigDict(from_attributes=True, validate_assignment=True)
