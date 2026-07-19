
# LLM

from __future__ import annotations

import logging
from typing import Any

import ollama
from ollama import Client

from app.config.settings import settings
from app.core.exceptions import (
    InvalidResponseError,
    ProviderConnectionError,
)
from app.llm.base import BaseLLMProvider


logger = logging.getLogger(__name__)


class OllamaProvider(BaseLLMProvider):
    """
    Production-ready Ollama provider.
    """

    def __init__(self) -> None:
        super().__init__(model=settings.OLLAMA_MODEL)

        self._client = Client(
            host=settings.OLLAMA_BASE_URL,
        )

        logger.info(
            "Initialized Ollama Provider | Model=%s | Host=%s",
            self.model,
            settings.OLLAMA_BASE_URL,
        )

    @property
    def provider_name(self) -> str:
        return "ollama"

    def generate(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """
        Generate a completion using Ollama.
        """

        try:
            response = self._client.generate(
                model=self.model,
                prompt=prompt,
                **kwargs,
            )

            return self._extract_generate_response(response)

        except ollama.ResponseError as error:
            logger.exception("Ollama generate response error.")
            raise ProviderConnectionError(str(error)) from error

        except Exception as error:
            logger.exception("Unexpected Ollama generate error.")
            raise ProviderConnectionError(str(error)) from error

    def chat(
        self,
        message: str,
        **kwargs: Any,
    ) -> str:
        """
        Chat with Ollama.
        """

        try:
            response = self._client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": message,
                    }
                ],
                **kwargs,
            )

            return self._extract_chat_response(response)

        except ollama.ResponseError as error:
            logger.exception("Ollama chat response error.")
            raise ProviderConnectionError(str(error)) from error

        except Exception as error:
            logger.exception("Unexpected Ollama chat error.")
            raise ProviderConnectionError(str(error)) from error

    def health_check(self) -> bool:
        """
        Verify Ollama availability.
        """

        try:
            self._client.ps()
            return True

        except Exception:
            return False

    def is_available(self) -> bool:
        """
        Check whether Ollama is available.
        """

        return self.health_check()

    @property
    def supports_streaming(self) -> bool:
        return True

    @property
    def supports_tools(self) -> bool:
        return False

    @property
    def supports_images(self) -> bool:
        return False

    def _extract_generate_response(
        self,
        response: dict[str, Any],
    ) -> str:
        """
        Validate generate response.
        """

        text = response.get("response", "").strip()

        if not text:
            raise InvalidResponseError(
                "Ollama returned an empty generate response."
            )

        return text

    def _extract_chat_response(
        self,
        response: dict[str, Any],
    ) -> str:
        """
        Validate chat response.
        """

        message = response.get("message", {})
        content = message.get("content", "").strip()

        if not content:
            raise InvalidResponseError(
                "Ollama returned an empty chat response."
            )

        return content

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(model='{self.model}')"
        )

