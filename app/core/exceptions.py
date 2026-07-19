# Error Handling

class JarvisError(Exception):
    """
    Base exception for all JARVIS errors.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


# =========================
# Configuration
# =========================

class ConfigurationError(JarvisError):
    """
    Raised when application configuration is invalid.
    """


# =========================
# LLM
# =========================

class LLMError(JarvisError):
    """
    Base LLM exception.
    """


class ProviderNotFoundError(LLMError):
    """
    Raised when the requested LLM provider does not exist.
    """


class ProviderConnectionError(LLMError):
    """
    Raised when a provider cannot be reached.
    """


class InvalidResponseError(LLMError):
    """
    Raised when the provider returns an invalid response.
    """


# =========================
# Memory
# =========================

class MemoryError(JarvisError):
    """
    Memory-related exception.
    """


# =========================
# RAG
# =========================

class RAGError(JarvisError):
    """
    Base RAG exception.
    """


class DocumentLoadError(RAGError):
    """
    Raised when a document cannot be loaded.
    """


class EmbeddingError(RAGError):
    """
    Raised when embeddings cannot be generated.
    """


class VectorStoreError(RAGError):
    """
    Raised when vector database operations fail.
    """


# =========================
# Speech
# =========================

class SpeechError(JarvisError):
    """
    Speech processing error.
    """


# =========================
# Automation
# =========================

class AutomationError(JarvisError):
    """
    Automation error.
    """


# =========================
# File Manager
# =========================

class FileOperationError(JarvisError):
    """
    File operation failed.
    """


# =========================
# Agent
# =========================

class AgentError(JarvisError):
    """
    AI Agent execution failed.
    """