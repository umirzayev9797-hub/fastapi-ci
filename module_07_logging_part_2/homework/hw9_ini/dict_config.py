import sys

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    # -------- FORMATTERS --------
    "formatters": {
        "fileFormatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%Z",
        },
        "consoleFormatter": {
            "format": "%(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%Z",
        },
    },

    # -------- HANDLERS --------
    "handlers": {
        "consoleHandler": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "consoleFormatter",
            "stream": sys.stdout,
        },
        "fileHandler": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "fileFormatter",
            "filename": "logfile.log",
        },
    },

    # -------- LOGGERS --------
    "loggers": {
        "appLogger": {
            "level": "DEBUG",
            "handlers": ["consoleHandler", "fileHandler"],
            "propagate": False,
        }
    },

    # -------- ROOT LOGGER --------
    "root": {
        "level": "DEBUG",
        "handlers": ["consoleHandler"],
    },
}
# TODO переписать реализацию ini-файла в формате dict-конфигурации.