import logging
from logger_helper import LevelFileHandler

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "default": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s"
        }
    },

    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "level_file": {
            "()": LevelFileHandler,          # кастомный handler
            "level": "DEBUG",
            "formatter": "default",
            "log_dir": "logs",
        },
    },

    "root": {
        "level": "DEBUG",
        "handlers": ["stdout", "level_file"],
    },
}
