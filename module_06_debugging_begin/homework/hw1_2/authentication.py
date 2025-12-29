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

# 1. Создаём логгер
logger = logging.getLogger("password_checker")

# 2. Конфигурируем logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler("stderr.txt")
    ]
)

# Список распространённых английских слов для проверки
ENGLISH_WORDS = {
    "password", "admin", "user", "login", "qwerty", "hello", "world",
    "letmein", "welcome", "monkey", "dragon", "iloveyou", "football",
    "baseball", "master", "superman", "trustno1", "abc123"
}


def is_strong_password(password: str) -> bool:
    """
    Проверяет пароль по новым стандартам:
    пароль НЕ должен содержать английские слова.
    """
    pwd_lower = password.lower()

    for word in ENGLISH_WORDS:
        if word in pwd_lower:
            logger.info(f"Пароль содержит английское слово '{word}' → небезопасный.")
            return False

    return True


def input_and_check_password() -> bool:
    logger.info("Старт проверки пароля (input_and_check_password)")
    password: str = getpass.getpass()

    # Проверка на пустой ввод
    if not password:
        logger.warning("Введён пустой пароль.")
        return False

    # Проверка силы пароля
    if not is_strong_password(password):
        logger.warning("Слишком слабый пароль по новым стандартам безопасности.")
        return False

    # Хеширование и сравнение
    try:
        hasher = hashlib.md5()
        hasher.update(password.encode("latin-1"))

        target_hash = "098f6bcd4621d373cade4e832627b4f6"

        if hasher.hexdigest() == target_hash:
            logger.info("Пароль верный, хеш совпал.")
            return True
        else:
            logger.info("Пароль неверный, хеш не совпал.")

    except ValueError as ex:
        logger.exception("Ошибка хеширования пароля!", exc_info=ex)

    return False


if __name__ == "__main__":
    logger.info("Вы пытаетесь аутентифицироваться в Skillbox")
    count_number: int = 3
    logger.info(f"Доступно {count_number} попытки ввода пароля")

    while count_number > 0:
        if input_and_check_password():
            exit(0)
        count_number -= 1
        logger.info(f"Осталось попыток: {count_number}")

    logger.error("Трижды введён неверный пароль!")
    exit(1)
