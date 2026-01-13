import logging
import logging.config
from contextlib import redirect_stdout
from logging_tree import printout

# импортируем модули, где создаются логгеры
import utils
from logging_config import LOGGING_CONFIG


def main():
    # 1. применяем конфигурацию
    logging.config.dictConfig(LOGGING_CONFIG)

    # 2. явно создаём логгеры
    logger_main = logging.getLogger(__name__)
    logger_utils = logging.getLogger("utils")

    # 3. пишем тестовые сообщения
    logger_main.debug("debug from main")
    logger_utils.info("info from utils")

    # 4. выводим дерево логгеров в файл
    with open("logging_tree.txt", "w", encoding="utf-8") as file:
        with redirect_stdout(file):
            printout()


if __name__ == "__main__":
    main()
