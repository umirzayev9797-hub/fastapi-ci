import logging.handlers

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "http": {
            "format": "%(levelname)s|%(name)s|%(message)s"
        }
    },

    "handlers": {
        "http_handler": {
            "class": "logging.handlers.HTTPHandler",
            "level": "INFO",
            "formatter": "http",
            "host": "127.0.0.1:3000",
            "url": "/log",
            "method": "POST",
        }
    },

    "loggers": {
        "service_a": {
            "level": "INFO",
            "handlers": ["http_handler"],
            "propagate": False
        },
        "service_b": {
            "level": "INFO",
            "handlers": ["http_handler"],
            "propagate": False
        },

        # отключаем шум
        "urllib3": {
            "level": "WARNING",
            "handlers": [],
            "propagate": False
        },
        "werkzeug": {
            "level": "WARNING",
            "handlers": [],
            "propagate": False
        }
    }
}
