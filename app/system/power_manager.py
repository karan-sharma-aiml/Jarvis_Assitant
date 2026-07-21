"""
JARVIS Power Manager

Windows power management.

Responsibilities
----------------
- Shutdown
- Restart
- Sleep
- Hibernate
- Lock
- Logoff
- Cancel shutdown

Windows only.
"""

from __future__ import annotations

import ctypes
import logging
import subprocess

from app.system.models import SystemResponse, SystemStatus

logger = logging.getLogger(__name__)


class PowerManager:
    def _run_command(self, args: list[str]) -> tuple[bool, str]:
        try:
            completed = subprocess.run(args, capture_output=True, text=True, check=False)
        except (OSError, ValueError) as exc:
            logger.exception("Power command failed: %s", exc)
            return False, str(exc)

        output = " ".join(part for part in [completed.stdout, completed.stderr] if part).strip()

        if completed.returncode == 0:
            return True, output

        logger.warning("Power command %s failed with code %s: %s", args, completed.returncode, output)
        return False, output or f"Command failed with exit code {completed.returncode}"

    def shutdown(self, delay: int = 0, dry_run: bool = False) -> SystemResponse:
        if dry_run:
            return SystemResponse(SystemStatus.SUCCESS, f"Shutdown scheduled after {delay} seconds (dry-run).")

        success, detail = self._run_command(["shutdown", "/s", "/t", str(delay)])
        if success:
            logger.info("Shutdown requested with delay %s", delay)
            return SystemResponse(SystemStatus.SUCCESS, "Shutdown command sent.")

        return SystemResponse(SystemStatus.FAILED, detail or "Unable to send shutdown command.")

    def restart(self, delay: int = 0, dry_run: bool = False) -> SystemResponse:
        if dry_run:
            return SystemResponse(SystemStatus.SUCCESS, f"Restart scheduled after {delay} seconds (dry-run).")

        success, detail = self._run_command(["shutdown", "/r", "/t", str(delay)])
        if success:
            logger.info("Restart requested with delay %s", delay)
            return SystemResponse(SystemStatus.SUCCESS, "Restart command sent.")

        return SystemResponse(SystemStatus.FAILED, detail or "Unable to send restart command.")

    def cancel_shutdown(self) -> SystemResponse:
        success, detail = self._run_command(["shutdown", "/a"])

        if success:
            output = detail.lower()
            if "no shutdown" in output or "not been scheduled" in output or "no shutdown was in progress" in output:
                logger.info("No shutdown is currently scheduled.")
                return SystemResponse(SystemStatus.SUCCESS, "No shutdown is currently scheduled.")

            logger.info("Shutdown cancellation requested.")
            return SystemResponse(SystemStatus.SUCCESS, "Shutdown cancelled.")

        if "no shutdown" in detail.lower() or "not been scheduled" in detail.lower() or "no shutdown was in progress" in detail.lower():
            logger.info("No shutdown is currently scheduled.")
            return SystemResponse(SystemStatus.SUCCESS, "No shutdown is currently scheduled.")

        return SystemResponse(SystemStatus.FAILED, detail or "Unable to cancel shutdown.")

    def lock(self, dry_run: bool = False) -> SystemResponse:
        if dry_run:
            return SystemResponse(SystemStatus.SUCCESS, "Lock command (dry-run).")

        try:
            ctypes.windll.user32.LockWorkStation()
        except (AttributeError, OSError, ValueError) as exc:
            logger.exception("Unable to lock workstation: %s", exc)
            return SystemResponse(SystemStatus.FAILED, "Unable to lock workstation.")

        logger.info("Lock requested.")
        return SystemResponse(SystemStatus.SUCCESS, "Computer locked.")

    def logoff(self, dry_run: bool = False) -> SystemResponse:
        if dry_run:
            return SystemResponse(SystemStatus.SUCCESS, "Logoff command (dry-run).")

        success, detail = self._run_command(["shutdown", "/l"])
        if success:
            logger.info("Logoff requested.")
            return SystemResponse(SystemStatus.SUCCESS, "User logged off.")

        return SystemResponse(SystemStatus.FAILED, detail or "Unable to log off.")

    def sleep(self, dry_run: bool = False) -> SystemResponse:
        if dry_run:
            return SystemResponse(SystemStatus.SUCCESS, "Sleep command (dry-run).")

        try:
            ctypes.windll.powrprof.SetSuspendState(False, True, False)
        except (AttributeError, OSError, ValueError) as exc:
            logger.exception("Unable to put the computer to sleep: %s", exc)
            return SystemResponse(SystemStatus.FAILED, "Unable to put the computer to sleep.")

        logger.info("Sleep requested.")
        return SystemResponse(SystemStatus.SUCCESS, "Computer sleeping.")

    def hibernate(self, dry_run: bool = False) -> SystemResponse:
        if dry_run:
            return SystemResponse(SystemStatus.SUCCESS, "Hibernate command (dry-run).")

        success, detail = self._run_command(["shutdown", "/h"])
        if success:
            logger.info("Hibernate requested.")
            return SystemResponse(SystemStatus.SUCCESS, "Hibernate command sent.")

        return SystemResponse(SystemStatus.FAILED, detail or "Unable to hibernate.")

    def health_check(self) -> bool:
        try:
            self.lock(dry_run=True)
            return True
        except Exception as exc:  # noqa: BLE001
            logger.exception("Power Manager health check failed: %s", exc)
            return False