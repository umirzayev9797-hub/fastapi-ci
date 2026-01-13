import sys

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "filters": {
        "ascii_only": {
            "()": "ascii_filter.AsciiFilter",
        }
    },

    "formatters": {
        "default": {
            "format": "%(levelname)s | %(name)s | %(message)s"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "filters": ["ascii_only"],
            "stream": sys.stdout
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "default",
            "filters": ["ascii_only"],
            "filename": "output.log",
            "encoding": "utf-8"
        }
    },

    "loggers": {
        "__main__": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False
        }
    }
}
