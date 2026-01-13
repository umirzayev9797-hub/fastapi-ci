import logging
import logging.config

from logging_config import LOGGING_CONFIG


def main():
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)

    # ASCII — должно попасть в лог
    logger.info("Simple ASCII message")
    logger.debug("Numbers 12345 and symbols !@#$%")

    # НЕ ASCII — НЕ должно попасть
    logger.info("Привет мир")
    logger.warning("ÎŒØ∏‡°⁄·°€йцукен")
    logger.error("Ошибка: деление на ноль")


if __name__ == "__main__":
    main()
