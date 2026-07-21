"""
Application Manager

Real Windows application automation.

Responsibilities
----------------
- Open applications
- Close applications
- Check running status
- List running processes
"""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

import psutil

from app.system.models import SystemResponse, SystemStatus

logger = logging.getLogger(__name__)


APPLICATIONS: dict[str, list[str]] = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "calc": ["calc.exe"],
    "paint": ["mspaint.exe"],
    "cmd": ["cmd.exe"],
    "powershell": ["powershell.exe"],
    "explorer": ["explorer.exe"],
    "task manager": ["taskmgr.exe"],
    "vs code": [
        str(Path.home() / "AppData/Local/Programs/Microsoft VS Code/Code.exe"),
        r"C:\Program Files\Microsoft VS Code\Code.exe",
        "code",
    ],
    "chrome": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "chrome",
    ],
    "edge": [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "msedge",
    ],
}


class ApplicationManager:
    def open(self, application: str) -> SystemResponse:
        app = application.strip().lower()

        if not app:
            logger.warning("Application name was empty.")
            return SystemResponse(SystemStatus.FAILED, "Application name is required.")

        if app not in APPLICATIONS:
            logger.warning("Unknown application requested: %s", application)
            return SystemResponse(SystemStatus.FAILED, f"Unknown application: {application}")

        for command in APPLICATIONS[app]:
            try:
                subprocess.Popen(command)
            except (OSError, ValueError, subprocess.SubprocessError) as exc:
                logger.warning("Unable to open %s using %s: %s", application, command, exc)
                continue

            logger.info("Application opened: %s", application)
            return SystemResponse(SystemStatus.SUCCESS, f"{application} opened successfully.")

        logger.warning("Unable to open application: %s", application)
        return SystemResponse(SystemStatus.FAILED, f"Unable to open {application}.")

    def close(self, process_name: str) -> SystemResponse:
        target = process_name.strip().lower()

        if not target:
            logger.warning("Process name was empty.")
            return SystemResponse(SystemStatus.FAILED, "Process name is required.")

        killed = False

        for proc in psutil.process_iter(["name"]):
            try:
                proc_name = proc.info.get("name", "")
                if target in proc_name.lower():
                    proc.kill()
                    killed = True
            except (psutil.Error, AttributeError, KeyError, TypeError) as exc:
                logger.warning("Unable to stop process %s: %s", proc.info.get("name", "unknown"), exc)

        if killed:
            logger.info("Application closed: %s", process_name)
            return SystemResponse(SystemStatus.SUCCESS, f"{process_name} closed.")

        logger.warning("Application not running: %s", process_name)
        return SystemResponse(SystemStatus.FAILED, f"{process_name} is not running.")

    def is_running(self, process_name: str) -> bool:
        target = process_name.strip().lower()

        if not target:
            return False

        for proc in psutil.process_iter(["name"]):
            try:
                proc_name = proc.info.get("name", "")
                if target in proc_name.lower():
                    return True
            except (psutil.Error, AttributeError, KeyError, TypeError):
                continue

        return False

    def list_running(self) -> list[str]:
        names: list[str] = []

        for proc in psutil.process_iter(["name"]):
            try:
                proc_name = proc.info.get("name")
                if proc_name:
                    names.append(proc_name)
            except (psutil.Error, AttributeError, KeyError, TypeError):
                continue

        return sorted(set(names))

    def health_check(self) -> bool:
        try:
            self.list_running()
            return True
        except Exception as exc:  # noqa: BLE001
            logger.exception("Application Manager health check failed: %s", exc)
            return False