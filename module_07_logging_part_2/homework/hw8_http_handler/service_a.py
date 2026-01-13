import logging
import logging.config

from logging_config import LOGGING_CONFIG


def main():
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger("service_a")

    logger.info("Service A started")
    logger.warning("Service A warning")
    logger.error("Service A error")


if __name__ == "__main__":
    main()
