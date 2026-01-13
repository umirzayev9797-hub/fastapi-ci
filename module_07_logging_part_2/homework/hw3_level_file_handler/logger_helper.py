import logging
import sys
from pathlib import Path


class LevelFileHandler(logging.Handler):
    """
    Custom logging handler that writes log records
    to different files depending on log level.
    """

    LEVEL_TO_FILE = {
        logging.DEBUG: "calc_debug.log",
        logging.INFO: "calc_info.log",
        logging.WARNING: "calc_warning.log",
        logging.ERROR: "calc_error.log",
        logging.CRITICAL: "calc_critical.log",
    }

    def __init__(self, log_dir: str = "."):
        super().__init__()
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            log_file = self.LEVEL_TO_FILE.get(record.levelno)
            if not log_file:
                return

            file_path = self.log_dir / log_file
            message = self.format(record)

            with file_path.open("a", encoding="utf-8") as f:
                f.write(message + "\n")

        except Exception:
            self.handleError(record)
