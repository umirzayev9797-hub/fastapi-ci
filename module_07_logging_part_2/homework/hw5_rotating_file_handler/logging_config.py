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
        # общий stdout (как раньше)
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },

        # многоуровневый файловый (из задачи 3–4)
        "level_file": {
            "()": LevelFileHandler,
            "level": "DEBUG",
            "formatter": "default",
            "log_dir": "logs",
        },

        # НОВЫЙ handler для utils
        "utils_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "default",
            "filename": "utils.log",
            "when": "h",
            "interval": 1,
            "backupCount": 10,
            "encoding": "utf-8",
        },
    },

    "root": {
        "level": "DEBUG",
        "handlers": ["stdout", "level_file"],
    },

    "loggers": {
        "utils": {
            "level": "INFO",
            "handlers": ["utils_file"],
            "propagate": False,
        }
    },
}
