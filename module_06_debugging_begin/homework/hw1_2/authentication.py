"""
1. Сконфигурируйте логгер программы из темы 4 так, чтобы он:

* писал логи в файл stderr.txt;
* не писал дату, но писал время в формате HH:MM:SS,
  где HH — часы, MM — минуты, SS — секунды с ведущими нулями.
  Например, 16:00:09;
* выводил логи уровня INFO и выше.

2. К нам пришли сотрудники отдела безопасности и сказали, что, согласно новым стандартам безопасности,
хорошим паролем считается такой пароль, который не содержит в себе слов английского языка,
так что нужно доработать программу из предыдущей задачи.

Напишите функцию is_strong_password, которая принимает на вход пароль в виде строки,
а возвращает булево значение, которое показывает, является ли пароль хорошим по новым стандартам безопасности.
"""

import getpass
import hashlib
import logging
import re

# 1. Настройка логгера по требованиям
logger = logging.getLogger("password_checker")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler("stderr.txt")
    ]
)

# 2. Предобработка слов английского языка из словаря Linux
def load_english_words() -> set[str]:
    words = set()
    try:
        with open("/usr/share/dict/words", "r", encoding="latin-1", errors="ignore") as f:
            for line in f:
                w = line.strip()
                if len(w) > 4:
                    words.add(w.lower())
    except FileNotFoundError:
        logger.critical("Системный словарь /usr/share/dict/words не найден!")
        exit(1)
    return words

ENGLISH_DICT = load_english_words()
logger.info(f"Словарь английских слов загружен ({len(ENGLISH_DICT)} слов длиной > 4)")


def is_strong_password(password: str) -> bool:
    """
    Пароль считается сильным, если НЕ содержит слов английского языка длиной > 4 символов.
    Регистр игнорируется.
    Используется set для поиска → O(1) в среднем.
    """
    extracted_words = re.findall(r"[A-Za-z]+", password)

    for word in extracted_words:
        w = word.lower()
        if len(w) > 4 and w in ENGLISH_DICT:
            logger.info(f"Найдено английское слово '{w}' в пароле → пароль слабый.")
            return False

    return True


def input_and_check_password() -> bool:
    logger.info("Запрос ввода пароля")
    password: str = getpass.getpass()

    if not password:
        logger.warning("Введён пустой пароль!")
        return False

    if not is_strong_password(password):
        logger.warning("Пароль слишком слабый по стандартам безопасности!")
        return False

    try:
        hasher = hashlib.md5()
        hasher.update(password.encode("latin-1"))

        target_hash = "098f6bcd4621d373cade4e832627b4f6"

        if hasher.hexdigest() == target_hash:
            logger.info("Пароль верный, аутентификация успешна.")
            return True
        else:
            logger.info("Пароль неверный, хеш не совпал.")

    except ValueError as ex:
        logger.exception("Ошибка при обработке пароля!", exc_info=ex)

    return False


if __name__ == "__main__":
    logger.debug("TEST DEBUG")  # не должен попасть (ниже INFO)
    logger.info("TEST INFO")  # должен попасть
    logger.warning("TEST WARNING")  # должен попасть
    logger.error("TEST ERROR")  # должен попасть
    logger.critical("TEST CRITICAL")  # должен попасть

    try:
        raise ValueError("TEST EXCEPTION")
    except Exception as e:
        logger.exception("Exception handler test", exc_info=e)

    logger.info("Аутентификация в Skillbox")
    count_number: int = 3
    logger.info(f"Доступно {count_number} попытки")

    while count_number > 0:
        if input_and_check_password():
            exit(0)
        count_number -= 1
        logger.info(f"Осталось попыток: {count_number}")

    logger.error("Пароль трижды введён неверно!")
    exit(1)

