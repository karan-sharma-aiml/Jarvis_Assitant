"""
Models used by the Windows Automation module.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SystemStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"


@dataclass(slots=True)
class SystemResponse:
    """
    Standard response returned by SystemManager.
    """

    status: SystemStatus
    message: str