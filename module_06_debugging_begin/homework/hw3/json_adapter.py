"""
Удобно сохранять логи в определённом формате, чтобы затем их можно было фильтровать и анализировать. 
Сконфигурируйте логгер так, чтобы он писал логи в файл skillbox_json_messages.log в следующем формате:

{"time": "<время>", "level": "<уровень лога>", "message": "<сообщение>"}

Но есть проблема: если в message передать двойную кавычку, то лог перестанет быть валидной JSON-строкой:

{"time": "21:54:15", "level": "INFO", "message": "“"}

Чтобы этого избежать, потребуется LoggerAdapter. Это класс из модуля logging,
который позволяет модифицировать логи перед тем, как они выводятся.
У него есть единственный метод — process, который изменяет сообщение или именованные аргументы, переданные на вход.

class JsonAdapter(logging.LoggerAdapter):
  def process(self, msg, kwargs):
    # меняем msg
    return msg, kwargs

Использовать можно так:

logger = JsonAdapter(logging.getLogger(__name__))
logger.info('Сообщение')

Вам нужно дописать метод process так, чтобы в логах была всегда JSON-валидная строка.
"""

import logging
import json
from datetime import datetime
class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        level = kwargs.get("extra", {}).get("level", self.logger.getEffectiveLevel())
        level_name = logging.getLevelName(level)
        safe_msg = json.dumps(msg, ensure_ascii=False)
        record_time = datetime.now().strftime("%H:%M:%S")
        return f'{{"time": "{record_time}", "level": "{level_name}", "message": {safe_msg}}}', {}


def configure_json_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[logging.FileHandler("skillbox_json_messages.log")]
    )

if __name__ == "__main__":
    configure_json_logging()
    base_logger = logging.getLogger(__name__)
    logger = JsonAdapter(base_logger)

    logger.info("Сообщение")
    logger.error('Кавычка)"')
    logger.debug("Еще одно сообщение")
