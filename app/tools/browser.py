"""
JARVIS Browser Tool

Safely opens web pages using the system's default browser.

Responsibilities:
- Validate URLs
- Open HTTP/HTTPS URLs
- Prevent unsupported URL schemes
"""

from __future__ import annotations

import ipaddress
import logging
import re
import webbrowser
from typing import Any, Optional
from urllib.parse import ParseResult, urlparse, urlunparse

from app.tools.base import BaseTool
from app.tools.exceptions import ToolExecutionError, ToolValidationError
from app.tools.models import ToolCategory

logger = logging.getLogger(__name__)

# Schemes that are explicitly forbidden (non-HTTP schemes or potentially
# dangerous handlers). This list follows the security requirements.
_FORBIDDEN_SCHEMES = {
    "file",
    "ftp",
    "javascript",
    "data",
    "mailto",
    "chrome",
    "about",
    "edge",
}

# Allowed schemes
_ALLOWED_SCHEMES = {"http", "https"}

# Simple regex for control characters / suspicious input
_CTL_RE = re.compile(r"[\x00-\x1f\x7f]")


class BrowserTool(BaseTool):
    """
    Tool for opening web pages in the default browser.
    """

    @property
    def name(self) -> str:
        return "browser"

    @property
    def description(self) -> str:
        return "Open a URL in the default web browser."

    @property
    def category(self) -> ToolCategory:
        return ToolCategory.WEB

    def validate(self, **kwargs: Any) -> None:
        """Validate ``url`` in ``kwargs``.

        Security policy:
        - Only ``http`` and ``https`` schemes allowed.
        - Explicitly reject common unsafe schemes (``file:``, ``javascript:``, etc.).
        - Reject malformed URLs and those without a network location.
        - Prevent credential-containing URLs (user:pass@host).
        - Prevent opening local/loopback IPs by default (use ``allow_local=True`` to override).

        Accepted inputs (backwards-compatible): ``url`` (str).
        """

        raw = kwargs.get("url")

        if not isinstance(raw, str):
            raise ToolValidationError("Parameter 'url' must be a string")

        # Delegate to the parsing/validation helper (no mutation of kwargs)
        self._parse_and_validate(raw, allow_local=bool(kwargs.get("allow_local", False)))

    def _parse_and_validate(self, url: str, *, allow_local: bool = False) -> ParseResult:
        """Parse and validate a URL string and return the parsed result.

        This helper performs the same checks as :meth:`validate` but returns
        the parsed ``ParseResult`` so callers (like ``execute``) can reuse
        the parsed value without relying on mutated kwargs.
        """

        url = url.strip()
        if not url:
            raise ToolValidationError("URL cannot be empty")

        if _CTL_RE.search(url):
            raise ToolValidationError("URL contains control characters")

        try:
            parsed = urlparse(url)
        except Exception as exc:  # pragma: no cover - extremely defensive
            raise ToolValidationError("Malformed URL") from exc

        scheme = (parsed.scheme or "").lower()

        if not scheme:
            raise ToolValidationError("URL missing scheme (e.g. 'https://')")

        if scheme in _FORBIDDEN_SCHEMES or scheme not in _ALLOWED_SCHEMES:
            raise ToolValidationError("Only HTTP and HTTPS URLs are allowed")

        if not parsed.netloc:
            raise ToolValidationError("Invalid URL: missing network location")

        if parsed.username or parsed.password:
            raise ToolValidationError("URLs with embedded credentials are not allowed")

        hostname: Optional[str] = parsed.hostname
        if not hostname:
            raise ToolValidationError("Invalid URL: missing hostname")

        try:
            ip = ipaddress.ip_address(hostname)
            if ip.is_loopback or ip.is_private or ip.is_link_local:
                if not allow_local:
                    raise ToolValidationError("Local network addresses are not allowed")
        except ValueError:
            if hostname.lower() == "localhost" and not allow_local:
                raise ToolValidationError("Localhost URLs are not allowed")

        if scheme == "file":
            raise ToolValidationError("file:// URLs are not permitted")

        return parsed

    def execute(self, **kwargs: Any) -> str:
        """
        Open the provided URL.
        """
        # Validate (does not mutate kwargs) and obtain a parsed result
        raw = kwargs.get("url")
        parsed = self._parse_and_validate(raw, allow_local=bool(kwargs.get("allow_local", False)))

        # For future compatibility allow callers to request different open
        # behaviors via kwargs (these are optional and ignored for now):
        # - open_new_tab (bool)
        # - open_new_window (bool)
        # We map these to the 'new' parameter of webbrowser.open when present.
        open_new_tab = bool(kwargs.get("open_new_tab", True))
        open_new_window = bool(kwargs.get("open_new_window", False))

        # Map to webbrowser.open 'new' parameter: 0=same,1=new window,2=new tab
        new_flag = 2 if open_new_tab and not open_new_window else (1 if open_new_window else 0)

        # Construct the safe URL without embedded credentials (already checked)
        safe_url = urlunparse(parsed._replace(fragment=""))

        try:
            opened = webbrowser.open(safe_url, new=new_flag)
        except Exception as exc:
            logger.exception("Failed to open URL: %s", safe_url)
            raise ToolExecutionError("Unable to open URL") from exc

        if not opened:
            logger.warning("webbrowser.open returned False for: %s", safe_url)
            raise ToolExecutionError("Unable to open the browser")

        logger.info("Opened URL: %s", safe_url)
        return f"Opened: {safe_url}"