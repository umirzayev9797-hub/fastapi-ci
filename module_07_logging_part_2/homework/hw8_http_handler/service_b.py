import logging
import logging.config

from logging_config import LOGGING_CONFIG


def main():
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger("service_b")

    logger.info("Service B started")
    logger.warning("Service B warning")
    logger.error("Service B error")


if __name__ == "__main__":
    main()
