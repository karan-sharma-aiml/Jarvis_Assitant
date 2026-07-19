# Main Logic

from app.config.settings import settings
from app.config.logging import get_logger

logger = get_logger(__name__)


class JarvisAssistant:
    """
    Main JARVIS Assistant.

    This class acts as the central controller of the application.
    Future modules such as LLM, Memory, Agents, Voice,
    Automation, and RAG will be connected here.
    """

    def __init__(self) -> None:
        self.name = settings.APP_NAME
        self.version = settings.APP_VERSION
        self.environment = settings.ENVIRONMENT

        logger.info("Initializing %s...", self.name)

    def start(self) -> None:
        """
        Start JARVIS.
        """

        logger.info("========================================")
        logger.info("%s started successfully.", self.name)
        logger.info("Version      : %s", self.version)
        logger.info("Environment  : %s", self.environment)
        logger.info("Provider     : %s", settings.DEFAULT_PROVIDER)
        logger.info("========================================")

    def stop(self) -> None:
        """
        Stop JARVIS.
        """

        logger.info("%s stopped.", self.name)

    def status(self) -> dict:
        """
        Return current assistant status.
        """

        return {
            "name": self.name,
            "version": self.version,
            "environment": self.environment,
            "provider": settings.DEFAULT_PROVIDER,
            "running": True,
        }