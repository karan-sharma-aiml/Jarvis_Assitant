# LLM

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseLLMProvider(ABC):
    """
    Abstract interface for every Large Language Model provider.

    Every provider (Ollama, Gemini, Groq, OpenAI, etc.)
    must inherit from this class.
    """

    def __init__(self, model: str) -> None:
        self._model = model

    @property
    def model(self) -> str:
        """
        Return the configured model name.
        """
        return self._model

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Return provider name.
        Example:
            ollama
            gemini
            groq
            openai
        """
        ...

    @abstractmethod
    def generate(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """
        Generate a response for a single prompt.
        """
        ...

    @abstractmethod
    def chat(
        self,
        message: str,
        **kwargs: Any,
    ) -> str:
        """
        Multi-turn chat interface.
        """
        ...

    @abstractmethod
    def health_check(self) -> bool:
        """
        Verify provider connectivity.
        """
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check whether the provider is ready.
        """
        ...

    @property
    def supports_streaming(self) -> bool:
        """
        Whether this provider supports streaming responses.
        """
        return False

    @property
    def supports_tools(self) -> bool:
        """
        Whether this provider supports tool/function calling.
        """
        return False

    @property
    def supports_images(self) -> bool:
        """
        Whether this provider supports image input.
        """
        return False

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(provider='{self.provider_name}', model='{self.model}')"
        )