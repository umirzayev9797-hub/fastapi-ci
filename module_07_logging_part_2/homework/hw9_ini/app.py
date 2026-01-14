import logging
import logging.config
from dict_config import LOGGING_CONFIG


def main():
    logging.config.dictConfig(LOGGING_CONFIG)

    root_logger = logging.getLogger()
    app_logger = logging.getLogger("appLogger")

    root_logger.debug("Root debug (не видно в консоли)")
    root_logger.warning("Root warning (видно в консоли)")

    app_logger.debug("App debug (только в файл)")
    app_logger.warning("App warning (в файл и консоль)")


if __name__ == "__main__":
    main()
