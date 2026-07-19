
# LLM Manager

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from app.config.settings import Provider, settings
from app.core.exceptions import (
    LLMError,
    ProviderConnectionError,
    ProviderNotFoundError,
)
from app.llm.providers.gemini_provider import GeminiProvider
from app.llm.providers.ollama_provider import OllamaProvider

if TYPE_CHECKING:
    from app.llm.base import BaseLLMProvider

logger = logging.getLogger(__name__)

# Provider registry: maps Provider enum to provider class
# To add a new provider, simply add an entry here
PROVIDER_REGISTRY: dict[Provider, type[BaseLLMProvider]] = {
    Provider.OLLAMA: OllamaProvider,
    Provider.GEMINI: GeminiProvider,
    # Provider.GROQ: GroqProvider,  # TODO: Implement GroqProvider
    # Provider.OPENAI: OpenAIProvider,  # TODO: Implement OpenAIProvider
}


class LLMManager:
    """
    Central manager for all LLM providers.

    Handles provider registration, switching, and failover.
    Designed to be resilient: if one provider fails to initialize,
    others are still registered and available.

    Attributes:
        _providers: Mapping of Provider enum to provider instances.
        _current_provider: Currently active provider.

    Example:
        >>> manager = LLMManager()
        >>> manager.list_providers()
        ['ollama', 'gemini']
        >>> response = manager.chat("Hello")
        >>> manager.set_provider(Provider.GEMINI)
    """

    def __init__(self) -> None:
        """
        Initialize the LLM manager.

        Attempts to register all available providers from PROVIDER_REGISTRY.
        Silently skips providers that fail to initialize.
        Raises LLMError if no providers are available.
        """
        self._providers: dict[Provider, BaseLLMProvider] = {}
        self._current_provider: BaseLLMProvider | None = None

        # Register providers from registry
        self._register_providers_from_registry()

        # Verify at least one provider is available
        if not self._providers:
            raise LLMError(
                "No LLM providers could be initialized. "
                "Ensure at least one provider is properly configured."
            )

        # Select active provider
        self._select_active_provider()

        logger.info(
            "LLM Manager initialized with providers: %s | Active: %s",
            self.list_providers(),
            self._current_provider.provider_name,
        )

    def _register_providers_from_registry(self) -> None:
        """
        Register all providers defined in PROVIDER_REGISTRY.

        Silently skips providers that fail to initialize.
        Logs information about successful registrations and warnings for failures.
        """
        for provider_enum, provider_class in PROVIDER_REGISTRY.items():
            try:
                provider_instance = provider_class()
                self._providers[provider_enum] = provider_instance
                logger.info(
                    "Registered LLM provider: %s",
                    provider_enum.value,
                )

            except ProviderConnectionError as error:
                logger.warning(
                    "Provider %s is not configured or unavailable: %s",
                    provider_enum.value,
                    str(error),
                )
            except ImportError as error:
                logger.warning(
                    "Provider %s import failed: %s",
                    provider_enum.value,
                    str(error),
                )
            except Exception as error:
                logger.warning(
                    "Failed to initialize provider %s: %s",
                    provider_enum.value,
                    str(error),
                )

    def _select_active_provider(self) -> None:
        """
        Select the active provider.

        Attempts to use DEFAULT_PROVIDER from settings.
        Falls back to first available provider if default is unavailable.

        Raises:
            LLMError: If no providers are available.
        """
        # Try configured default provider
        if settings.DEFAULT_PROVIDER in self._providers:
            self._current_provider = self._providers[
                settings.DEFAULT_PROVIDER
            ]
            return

        # Fallback to first available provider
        if self._providers:
            first_provider_enum = next(iter(self._providers.keys()))
            self._current_provider = self._providers[first_provider_enum]
            logger.warning(
                "Default provider %s not available. "
                "Using %s instead.",
                settings.DEFAULT_PROVIDER.value,
                first_provider_enum.value,
            )
            return

        raise LLMError("No providers available for selection")

    def list_providers(self) -> list[str]:
        """
        List all registered provider names.

        Returns:
            List of available provider identifiers (string values).

        Example:
            >>> manager.list_providers()
            ['ollama', 'gemini']
        """
        return [provider.value for provider in self._providers.keys()]

    def get_provider(self) -> BaseLLMProvider:
        """
        Return the currently active provider.

        Returns:
            Active BaseLLMProvider instance.

        Raises:
            LLMError: If no provider is currently active.
        """
        if not self._current_provider:
            raise LLMError("No active provider selected")
        return self._current_provider

    def set_provider(self, provider_enum: Provider) -> None:
        """
        Switch the active provider.

        Args:
            provider_enum: Provider enum value.

        Raises:
            ProviderNotFoundError: If provider is not registered.

        Example:
            >>> manager.set_provider(Provider.GEMINI)
        """
        if provider_enum not in self._providers:
            raise ProviderNotFoundError(
                f"Provider '{provider_enum.value}' is not registered. "
                f"Available: {self.list_providers()}"
            )

        self._current_provider = self._providers[provider_enum]
        logger.info(
            "Switched LLM provider to: %s",
            provider_enum.value,
        )

    def chat(self, message: str, **kwargs) -> str:
        """
        Send a chat message to the active provider.

        Args:
            message: User message.
            **kwargs: Additional provider-specific parameters.

        Returns:
            Provider response.

        Raises:
            LLMError: If provider fails or no provider is active.
        """
        provider = self.get_provider()
        return provider.chat(message, **kwargs)

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a completion using the active provider.

        Args:
            prompt: Text prompt.
            **kwargs: Additional provider-specific parameters.

        Returns:
            Generated text.

        Raises:
            LLMError: If provider fails or no provider is active.
        """
        provider = self.get_provider()
        return provider.generate(prompt, **kwargs)

    def health_check(self) -> bool:
        """
        Check if the active provider is healthy.

        Returns:
            True if provider is reachable, False otherwise.
        """
        try:
            provider = self.get_provider()
            return provider.health_check()
        except LLMError as error:
            logger.debug("Health check failed: %s", str(error))
            return False

    def is_available(self) -> bool:
        """
        Check if the active provider is ready to serve requests.

        Returns:
            True if provider is operational, False otherwise.
        """
        try:
            provider = self.get_provider()
            return provider.is_available()
        except LLMError as error:
            logger.debug("Availability check failed: %s", str(error))
            return False

    def __repr__(self) -> str:
        """Return string representation."""
        provider_names = self.list_providers()
        active_name = (
            self._current_provider.provider_name
            if self._current_provider
            else "none"
        )
        return (
            f"LLMManager("
            f"providers={provider_names}, "
            f"active={active_name}"
            f")"
        )

