# Main Logic

import sys

from app.config.logging import setup_logging, get_logger
from app.core.assistant import JarvisAssistant
from app.core.exceptions import JarvisError

setup_logging()

logger = get_logger(__name__)


def main() -> int:
    """
    Application entry point.
    """

    try:
        logger.info("Starting JARVIS...")

        assistant = JarvisAssistant()

        assistant.start()

        logger.info("JARVIS is running.")

        input("\nPress ENTER to exit...\n")

        assistant.stop()

        logger.info("JARVIS closed successfully.")

        return 0

    except JarvisError as error:
        logger.exception("JARVIS Error: %s", error)
        return 1

    except KeyboardInterrupt:
        logger.warning("Shutdown requested by user.")
        return 0

    except Exception:
        logger.exception("Unexpected application error.")
        return 1


if __name__ == "__main__":
    sys.exit(main())