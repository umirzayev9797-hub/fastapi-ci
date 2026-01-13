import logging


class AsciiFilter(logging.Filter):
    """
    Фильтр пропускает только те лог-сообщения,
    текст которых содержит исключительно ASCII-символы
    """

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        return message.isascii()
