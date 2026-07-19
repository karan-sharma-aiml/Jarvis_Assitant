"""
JARVIS Text Cleaner

Provides text normalization utilities for the Knowledge Engine.

Responsibilities:
- Normalize Unicode
- Normalize whitespace
- Remove repeated blank lines
- Remove page numbers
- Remove separator lines

This module intentionally performs NO chunking or parsing.
"""

from __future__ import annotations

import re
import unicodedata


class TextCleaner:
    """
    Cleans extracted document text before chunking.
    """

    @staticmethod
    def clean(text: str) -> str:
        """
        Apply every cleaning step.
        """

        text = TextCleaner.normalize_unicode(text)

        text = TextCleaner.normalize_line_endings(text)

        text = TextCleaner.remove_page_numbers(text)

        text = TextCleaner.remove_separator_lines(text)

        text = TextCleaner.remove_extra_whitespace(text)

        text = TextCleaner.remove_blank_lines(text)

        return text.strip()

    @staticmethod
    def normalize_unicode(text: str) -> str:
        """
        Normalize unicode characters.
        """

        return unicodedata.normalize(
            "NFKC",
            text,
        )

    @staticmethod
    def normalize_line_endings(text: str) -> str:
        """
        Convert CRLF/CR into LF.
        """

        return (
            text.replace("\r\n", "\n")
            .replace("\r", "\n")
        )

    @staticmethod
    def remove_extra_whitespace(text: str) -> str:
        """
        Collapse repeated spaces.
        """

        return re.sub(
            r"[ \t]+",
            " ",
            text,
        )

    @staticmethod
    def remove_blank_lines(text: str) -> str:
        """
        Collapse multiple blank lines.
        """

        return re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

    @staticmethod
    def remove_separator_lines(text: str) -> str:
        """
        Remove separator lines.

        Example:

        ----------
        ==========
        __________
        """

        return re.sub(
            r"^[=\-_*]{3,}$",
            "",
            text,
            flags=re.MULTILINE,
        )

    @staticmethod
    def remove_page_numbers(text: str) -> str:
        """
        Remove simple page number patterns.

        Supported:

        Page 1

        Page 25

        PAGE 100
        """

        return re.sub(
            r"^\s*page\s+\d+\s*$",
            "",
            text,
            flags=re.IGNORECASE | re.MULTILINE,
        )