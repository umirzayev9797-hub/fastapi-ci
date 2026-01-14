import sys
import logging

from utils import string_to_operator
from logger_helper import LevelFileHandler

logger = logging.getLogger(__name__)


def configure_logging() -> None:
    formatter = logging.Formatter(
        "%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s"
    )

    # stdout handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)

    # multi-level file handler
    file_handler = LevelFileHandler(log_dir="logs")
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[stdout_handler, file_handler]
    )



def calc(args):
    logger.debug("Arguments received: %s", args)

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        logger.error("Error while converting number 1: %s", num_1)
        logger.exception(e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        logger.error("Error while converting number 2: %s", num_2)
        logger.exception(e)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)

    logger.info("Result: %s", result)
    logger.info("%s %s %s = %s", num_1, operator, num_2, result)


if __name__ == '__main__':
    configure_logging()

    # calc(sys.argv[1:])
    calc('2+3')
