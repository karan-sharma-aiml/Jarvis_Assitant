"""
JARVIS Document Parser

Extracts plain text from supported document types.

Handles optional dependencies gracefully:
- pypdf (for PDF parsing) - lazy loaded on first PDF parse
- python-docx (for DOCX parsing) - lazy loaded on first DOCX parse

The parser supports both binary formats (PDF, DOCX) and text-based
formats (TXT, Markdown, JSON, CSV, HTML). Binary format dependencies
are optional and only loaded when actually needed.

Responsibilities:
- Read document content from various formats
- Parse supported formats (TXT, PDF, DOCX, Markdown, JSON, CSV, HTML)
- Return ParsedDocument with extracted text
- Provide clear error messages for missing optional dependencies

No cleaning, chunking, embeddings, or retrieval logic belongs here.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable

from app.rag.models import (
    Document,
    DocumentType,
    ParsedDocument,
)

logger = logging.getLogger(__name__)


def _require_pypdf() -> type:
    """
    Lazily import pypdf with user-friendly error handling.

    Returns:
        PdfReader class from pypdf

    Raises:
        ImportError: If pypdf is not installed, with installation instructions
    """

    try:
        from pypdf import PdfReader

        return PdfReader
    except ImportError as e:
        raise ImportError(
            "pypdf is required to parse PDF files.\n"
            "Install it using:\n\n"
            "    pip install pypdf\n"
        ) from e


def _require_docx() -> type:
    """
    Lazily import python-docx with user-friendly error handling.

    Returns:
        Document class from docx

    Raises:
        ImportError: If python-docx is not installed, with installation instructions
    """

    try:
        from docx import Document

        return Document
    except ImportError as e:
        raise ImportError(
            "python-docx is required to parse DOCX files.\n"
            "Install it using:\n\n"
            "    pip install python-docx\n"
        ) from e


class DocumentParser:
    """
    Parse supported documents into plain text.

    Supports the following document types:
    - TXT: Plain text files (always available)
    - PDF: PDF files (requires pypdf - lazy loaded)
    - DOCX: Microsoft Word documents (requires python-docx - lazy loaded)
    - Markdown: Markdown files (text-based, always available)
    - JSON: JSON files (text-based, always available)
    - CSV: CSV files (text-based, always available)
    - HTML: HTML files (text-based, always available)

    Optional dependencies (pypdf, python-docx) are only imported when
    actually parsing files of those types, allowing the application to
    start even if they're not installed.
    """

    def parse(
        self,
        document: Document,
    ) -> ParsedDocument:
        """
        Parse a single document and extract its text content.

        Args:
            document: Document object containing file path and type.

        Returns:
            ParsedDocument: Original document plus extracted text content.

        Raises:
            ValueError: If document type is not supported.
            ImportError: If required optional dependency is missing
                (with installation instructions).
            IOError: If file cannot be read.
            Exception: Format-specific parsing errors (PDF, DOCX, etc).
        """

        parser = self._get_parser(document.document_type)

        logger.debug(
            "Starting parse: type=%s, path=%s",
            document.document_type.value,
            document.path.name,
        )

        content = parser(document.path)

        logger.info(
            "Successfully parsed document: path=%s, type=%s, bytes=%d",
            document.path.name,
            document.document_type.value,
            len(content.encode('utf-8')),
        )

        return ParsedDocument(
            document=document,
            content=content,
        )

    def _get_parser(
        self,
        document_type: DocumentType,
    ) -> Callable[[Path], str]:
        """
        Get the appropriate parser function for a document type.

        Args:
            document_type: Type of document to parse.

        Returns:
            Callable parser function that takes Path and returns str.

        Raises:
            ValueError: If document type is not supported.
        """

        parsers: dict[DocumentType, Callable[[Path], str]] = {
            DocumentType.TXT: self._parse_text,
            DocumentType.MARKDOWN: self._parse_text,
            DocumentType.JSON: self._parse_text,
            DocumentType.CSV: self._parse_text,
            DocumentType.HTML: self._parse_text,
            DocumentType.PDF: self._parse_pdf,
            DocumentType.DOCX: self._parse_docx,
        }

        if document_type not in parsers:
            raise ValueError(
                f"Unsupported document type: {document_type.value}"
            )

        return parsers[document_type]

    @staticmethod
    def _parse_text(
        path: Path,
    ) -> str:
        """
        Parse text-based documents.

        Handles: TXT, Markdown, JSON, CSV, HTML

        Args:
            path: Path to text file.

        Returns:
            File contents as string.

        Raises:
            IOError: If file cannot be read.
            UnicodeDecodeError: If file encoding is invalid.
        """

        logger.debug(
            "Parsing text-based document: %s",
            path.name,
        )

        try:
            content = path.read_text(
                encoding='utf-8',
                errors='ignore',
            )
            logger.debug(
                "Text file read: %s bytes",
                len(content.encode('utf-8')),
            )
            return content
        except IOError as e:
            logger.error(
                "Failed to read text file: %s - %s",
                path,
                str(e),
            )
            raise

    @staticmethod
    def _parse_pdf(
        path: Path,
    ) -> str:
        """
        Parse PDF document and extract all text.

        Lazily imports pypdf only when actually parsing a PDF.
        If pypdf is not installed, provides clear error message
        with installation instructions.

        Args:
            path: Path to PDF file.

        Returns:
            Extracted text from all PDF pages, joined with newlines.

        Raises:
            ImportError: If pypdf is not installed (with instructions).
            IOError: If PDF file cannot be read.
            Exception: If PDF parsing fails.
        """

        logger.debug(
            "Parsing PDF document: %s",
            path.name,
        )

        # Lazy import - only fails if actually parsing PDF
        PdfReader = _require_pypdf()

        try:
            reader = PdfReader(path)

            pages: list[str] = []

            logger.debug(
                "PDF file loaded: %d pages",
                len(reader.pages),
            )

            for page_num, page in enumerate(reader.pages, start=1):

                try:
                    text = page.extract_text() or ""
                    pages.append(text)
                    logger.debug(
                        "Extracted text from page %d: %d chars",
                        page_num,
                        len(text),
                    )
                except Exception as e:
                    logger.warning(
                        "Failed to extract text from page %d: %s",
                        page_num,
                        str(e),
                    )

            extracted = "\n".join(pages)
            logger.debug(
                "PDF parsing complete: %d pages, %d total chars",
                len(reader.pages),
                len(extracted),
            )
            return extracted

        except IOError as e:
            logger.error(
                "Failed to read PDF file: %s - %s",
                path,
                str(e),
            )
            raise
        except Exception as e:
            logger.error(
                "PDF parsing error: %s - %s",
                path,
                str(e),
            )
            raise

    @staticmethod
    def _parse_docx(
        path: Path,
    ) -> str:
        """
        Parse Microsoft Word document and extract all text.

        Lazily imports python-docx only when actually parsing a DOCX file.
        If python-docx is not installed, provides clear error message
        with installation instructions.

        Args:
            path: Path to DOCX file.

        Returns:
            Extracted text from all paragraphs, joined with newlines.

        Raises:
            ImportError: If python-docx is not installed (with instructions).
            IOError: If DOCX file cannot be read.
            Exception: If DOCX parsing fails.
        """

        logger.debug(
            "Parsing DOCX document: %s",
            path.name,
        )

        # Lazy import - only fails if actually parsing DOCX
        DocxDocument = _require_docx()

        try:
            document = DocxDocument(path)

            logger.debug(
                "DOCX file loaded: %d paragraphs",
                len(document.paragraphs),
            )

            paragraphs: list[str] = []

            for para_num, paragraph in enumerate(
                document.paragraphs,
                start=1,
            ):

                text = paragraph.text
                if text:
                    paragraphs.append(text)
                    logger.debug(
                        "Extracted text from paragraph %d: %d chars",
                        para_num,
                        len(text),
                    )

            extracted = "\n".join(paragraphs)
            logger.debug(
                "DOCX parsing complete: %d paragraphs, %d total chars",
                len(document.paragraphs),
                len(extracted),
            )
            return extracted

        except IOError as e:
            logger.error(
                "Failed to read DOCX file: %s - %s",
                path,
                str(e),
            )
            raise
        except Exception as e:
            logger.error(
                "DOCX parsing error: %s - %s",
                path,
                str(e),
            )
            raise