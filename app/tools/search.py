"""JARVIS Search Tool

Builds a search URL from a natural language query and delegates opening
the result to the BrowserTool. This module only constructs search URLs;
it does not open browsers directly or perform any browser automation.
"""

from __future__ import annotations

import logging
from typing import Any, Iterable, Mapping, Optional
from urllib.parse import quote_plus, urlparse

from app.tools.base import BaseTool
from app.tools.browser import BrowserTool
from app.tools.exceptions import ToolValidationError
from app.tools.models import ToolCategory

logger = logging.getLogger(__name__)


# Canonical search engine templates. Key names are lowercase.
_SEARCH_ENGINES: dict[str, str] = {
    "google": "https://www.google.com/search?q={}",
    "duckduckgo": "https://duckduckgo.com/?q={}",
    "bing": "https://www.bing.com/search?q={}",
}


class SearchTool(BaseTool):
    """Convert natural language queries into search requests.

    Design notes:
    - The tool validates queries and engine selection, builds a safe search URL,
      and delegates opening to a BrowserTool instance.
    - ``BrowserTool`` is injected optionally to allow testing and future
      composition; when omitted, a default ``BrowserTool`` is created.
    """

    def __init__(self, browser: Optional[BrowserTool] = None) -> None:
        # Allow dependency injection for testing and lifecycle control.
        self._browser: BrowserTool = browser or BrowserTool()

    @property
    def name(self) -> str:
        return "search"

    @property
    def description(self) -> str:
        return "Search the web using a search engine."

    @property
    def category(self) -> ToolCategory:
        return ToolCategory.WEB

    def _normalize_engine(self, engine: Optional[str]) -> str:
        if not engine:
            return "google"
        return str(engine).strip().lower()

    def validate(self, **kwargs: Any) -> None:
        """Validate input parameters.

        Expected kwargs:
        - ``query``: required non-empty string.
        - ``engine``: optional search engine key.
        """

        query = kwargs.get("query")
        if not isinstance(query, str):
            raise ToolValidationError("Query must be a string.")

        query_str = query.strip()
        if not query_str:
            raise ToolValidationError("Query cannot be empty.")

        engine = self._normalize_engine(kwargs.get("engine"))
        if engine not in _SEARCH_ENGINES:
            raise ToolValidationError(f"Unsupported search engine: {engine}")

    def _build_search_url(self, query: str, engine: str) -> str:
        """Build and validate the search URL for ``engine``.

        This method URL-encodes the query and constructs the search URL
        from a trusted template. It performs a lightweight parse of the
        resulting URL to ensure the scheme and netloc are present.
        """

        encoded = quote_plus(query)
        template = _SEARCH_ENGINES[engine]
        url = template.format(encoded)

        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            logger.error("Constructed invalid search URL: %s", url)
            raise ToolValidationError("Constructed an invalid search URL")

        return url

    def execute(self, **kwargs: Any) -> str:
        """Validate inputs, build a search URL, and open it via BrowserTool.

        Returns whatever ``BrowserTool.execute`` returns (keeps API stable).
        """

        # Validate user inputs
        self.validate(**kwargs)

        # Extract and normalize inputs
        query: str = kwargs["query"].strip()
        engine: str = self._normalize_engine(kwargs.get("engine"))

        logger.debug("SearchTool: query=%r engine=%s", query, engine)

        # Build the safe search URL and delegate opening to BrowserTool
        url = self._build_search_url(query, engine)
        return self._browser.execute(url=url)