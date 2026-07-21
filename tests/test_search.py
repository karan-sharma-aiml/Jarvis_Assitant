import pytest

from app.tools.search import SearchTool, _SEARCH_ENGINES
from app.tools.exceptions import ToolValidationError


class DummyBrowser:
    def __init__(self):
        self.opened_urls = []

    def execute(self, *, url: str):
        self.opened_urls.append(url)
        return f"Opened: {url}"


def test_valid_query_defaults_google():
    browser = DummyBrowser()
    tool = SearchTool(browser=browser)

    result = tool.execute(query="openai chatgpt")

    assert result == f"Opened: {browser.opened_urls[0]}"
    assert "google.com/search" in browser.opened_urls[0]
    assert "openai+chatgpt" in browser.opened_urls[0]


def test_empty_query_raises():
    tool = SearchTool(browser=DummyBrowser())
    with pytest.raises(ToolValidationError):
        tool.execute(query="   ")


def test_invalid_engine_raises():
    tool = SearchTool(browser=DummyBrowser())
    with pytest.raises(ToolValidationError):
        tool.execute(query="test", engine="unknown")


def test_special_characters_and_unicode():
    browser = DummyBrowser()
    tool = SearchTool(browser=browser)

    query = "café & restaurant / 東京"
    result = tool.execute(query=query, engine="duckduckgo")

    assert "duckduckgo.com" in browser.opened_urls[0]
    # URL-encoded representation should include percent-encoded bytes or pluses
    assert ("%" in browser.opened_urls[0]) or ("+" in browser.opened_urls[0])


def test_very_long_query():
    browser = DummyBrowser()
    tool = SearchTool(browser=browser)

    long_query = "a" * 5000
    result = tool.execute(query=long_query, engine="bing")

    assert "bing.com" in browser.opened_urls[0]
    assert browser.opened_urls[0].endswith("a" * 5000)