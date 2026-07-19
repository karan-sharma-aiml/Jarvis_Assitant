
# LLM Provider - Gemini

from __future__ import annotations

import logging
from typing import Any, TypedDict

from google import genai

from app.config.settings import settings
from app.core.exceptions import (
    InvalidResponseError,
    ProviderConnectionError,
)
from app.llm.base import BaseLLMProvider


logger = logging.getLogger(__name__)


class GeminiTextPart(TypedDict, total=False):
    """Text part of Gemini response."""
    text: str


class GeminiPart(TypedDict, total=False):
    """Part of Gemini response content."""
    text: str


class GeminiContent(TypedDict):
    """Content structure in Gemini response."""
    parts: list[GeminiPart]
    role: str


class GeminiCandidate(TypedDict, total=False):
    """Candidate in Gemini response."""
    content: GeminiContent


class GeminiProviderResponse(TypedDict, total=False):
    """Response structure from Gemini API."""
    candidates: list[GeminiCandidate]
    text: str


class GeminiProvider(BaseLLMProvider):
    """
    Google Gemini LLM provider using the official google.genai SDK.

    Supports text generation and chat completions via Google's Gemini API.
    Provides health checks, model validation, and structured response parsing.

    Uses the latest official SDK (google.genai) which replaces the deprecated
    google.generativeai package.

    Attributes:
        model: Model identifier (e.g., 'gemini-2.0-flash')
        supports_streaming: True - Gemini supports streaming responses
        supports_tools: True - Gemini supports function/tool calling
        supports_images: True - Gemini supports image input
    """

    def __init__(self) -> None:
        """
        Initialize Gemini provider.

        Validates API key configuration and creates client connection.

        Raises:
            ProviderConnectionError: If API key is not configured.
        """
        super().__init__(model=settings.GEMINI_MODEL)

        if not settings.GEMINI_API_KEY:
            raise ProviderConnectionError(
                "GEMINI_API_KEY is not configured."
            )

        # Initialize Google Genai client
        self._client = genai.Client(api_key=settings.GEMINI_API_KEY)

        logger.info(
            "Initialized Gemini Provider | Model=%s",
            self.model,
        )

    @property
    def provider_name(self) -> str:
        """Return the provider identifier."""
        return "gemini"

    def generate(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """
        Generate a completion for a single prompt.

        Args:
            prompt: Text prompt to complete.
            **kwargs: Additional parameters (temperature, top_p, etc.).

        Returns:
            Generated text completion.

        Raises:
            ProviderConnectionError: If Gemini API call fails.
            InvalidResponseError: If response cannot be parsed.
        """
        try:
            response = self._client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=kwargs if kwargs else None,
            )

            result = self._extract_text_response(response)
            logger.debug(
                "Generated completion | Model=%s | Prompt_len=%d | Result_len=%d",
                self.model,
                len(prompt),
                len(result),
            )
            return result

        except genai.errors.APIError as error:
            logger.exception("Gemini API error during generate")
            raise ProviderConnectionError(str(error)) from error
        except Exception as error:
            logger.exception("Unexpected error during Gemini generate")
            raise ProviderConnectionError(str(error)) from error

    def chat(
        self,
        message: str,
        **kwargs: Any,
    ) -> str:
        """
        Chat interface for multi-turn conversations.

        Args:
            message: User message to send.
            **kwargs: Additional parameters (temperature, top_p, etc.).

        Returns:
            Assistant's response text.

        Raises:
            ProviderConnectionError: If Gemini API call fails.
            InvalidResponseError: If response cannot be parsed.
        """
        try:
            # Create a new chat session for this request
            chat = self._client.chats.create(model=self.model)

            # Send message to chat
            response = chat.send_message(
                message,
                config=kwargs if kwargs else None,
            )

            result = self._extract_text_response(response)
            logger.debug(
                "Chat response received | Model=%s | Message_len=%d | Response_len=%d",
                self.model,
                len(message),
                len(result),
            )
            return result

        except genai.errors.APIError as error:
            logger.exception("Gemini API error during chat")
            raise ProviderConnectionError(str(error)) from error
        except Exception as error:
            logger.exception("Unexpected error during Gemini chat")
            raise ProviderConnectionError(str(error)) from error

    def health_check(self) -> bool:
        """
        Verify Gemini API connectivity.

        Attempts a simple API call to check availability.

        Returns:
            True if Gemini is reachable, False otherwise.
        """
        try:
            self._client.models.generate_content(
                model=self.model,
                contents="Hello",
            )
            logger.debug("Health check passed")
            return True

        except Exception as error:
            logger.debug("Health check failed: %s", str(error))
            return False

    def is_available(self) -> bool:
        """
        Check if Gemini is ready to serve requests.

        This is distinct from health_check in that it may perform
        additional validation if needed.

        Returns:
            True if Gemini is operational, False otherwise.
        """
        return self.health_check()

    @property
    def supports_streaming(self) -> bool:
        """Gemini supports streaming responses."""
        return True

    @property
    def supports_tools(self) -> bool:
        """Gemini supports function/tool calling."""
        return True

    @property
    def supports_images(self) -> bool:
        """Gemini supports image input."""
        return True

    def _extract_text_response(
        self,
        response: Any,
    ) -> str:
        """
        Extract and validate text from Gemini response.

        Handles the new google.genai SDK response structure.

        Args:
            response: Raw response object from Gemini API.

        Returns:
            Extracted text content.

        Raises:
            InvalidResponseError: If response contains no text.
        """
        # The new SDK provides response.text directly
        text = getattr(response, "text", "")

        if not text:
            raise InvalidResponseError(
                "Gemini returned an empty response."
            )

        return text.strip()

    def __repr__(self) -> str:
        """Return string representation of provider."""
        return (
            f"{self.__class__.__name__}"
            f"(model='{self.model}')"
        )

