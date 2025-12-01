import os
import re
import datetime
import random
from flask import Flask


# --- Настройка для Задачи 6: /get_random_word ---
# Получаем абсолютный путь к папке, где лежит текущий файл (app.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')
# Глобальная переменная для хранения списка слов
WORDS_LIST = []


def get_words_from_book(filepath: str) -> list[str]:
    """
    Читает файл, извлекает все слова и возвращает их список.
    Использует регулярное выражение для удаления знаков препинания.

    Args:
        filepath: Абсолютный путь к файлу книги.

    Returns:
        Список всех слов в книге.
    """
    try:
        # Используем 'with' для корректной работы с файлом
        with open(filepath, 'r', encoding='utf-8') as book:
            text = book.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл книги не найден по пути: {filepath}")
        return []

    words = re.findall(r'\b\w+\b', text.lower())

    return words
# ЕДИНОРАЗОВЫЙ ВЫЗОВ: Загружаем слова при запуске модуля
WORDS_LIST = get_words_from_book(BOOK_FILE)
print(f"Загружено {len(WORDS_LIST)} слов из книги 'Война и мир'.")

# --- Глобальные списки для Задач 2 и 3 (Исправлено) ---
# Каждый элемент - отдельная строка для корректной обработки
cars_list = ['Chevrolet', 'Renault', 'Ford', 'Lada']
cats_list = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']

# --- Глобальный счетчик для Задачи 7: /counter ---
visit_counter = 0

app = Flask(__name__)

# Задача 1: /hello_world
@app.route('/hello_world')
def hello_world():
    return 'Привет, мир!'


# Задача 2: /cars
# Возвращает список машин, объединенных запятой. Список не пересоздается.
@app.route('/cars')
def cars():
    # Соединяем элементы списка в одну строку через запятую и пробел
    return ', '.join(cars_list)

# Задача 3: /cats
# Возвращает случайную породу. Список не пересоздается.
@app.route('/cats')
def cats():
    random_cats = random.choice(cats_list)
    return f'Случайная порода кошек: {random_cats}'


# Задача 4: /get_time/now
# Возвращает текущее время. Время обновляется при запросе.
@app.route('/get_time/now')
def get_time_now():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return f'Точное время: {current_time}'

# Задача 5: /get_time/future
# Возвращает время через час. Время обновляется при запросе.
@app.route('/get_time/future')
def get_time_future():
    # Получаем текущее время
    current_time = datetime.datetime.now()

    # Создаем объект timedelta для одного часа
    one_hour = datetime.timedelta(hours=1)

    # Вычисляем время через один час
    future_time = current_time + one_hour

    # Форматируем время для отображения (например, ГГГГ-ММ-ДД ЧЧ:ММ:СС)
    current_time_after_hour = future_time.strftime("%Y-%m-%d %H:%M:%S")
    return f'Точное время через час будет {current_time_after_hour}'

# Задача 6: /get_random_word
# Возвращает случайное слово. Файл не открывается заново.
@app.route('/get_random_word')
def get_random_word():
    """
    Возвращает случайное слово из предварительно загруженного списка.
    """
    if not WORDS_LIST:
        return "Ошибка: Не удалось загрузить слова из книги. Проверьте путь и наличие файла.", 500

    # Выбираем случайное слово из загруженного списка
    # Это выполняется быстро, так как файл не открывается заново.
    random_word = random.choice(WORDS_LIST)

    # Слово отображается без знаков препинания (т.к. они были удалены при загрузке)
    return f"Случайное слово из книги «Война и мир»: **{random_word}**"

# Задача 7: /counter
# Увеличивает счетчик при каждом обращении.
@app.route('/counter')
def counter():
    global visit_counter
    visit_counter += 1
    # Возвращается строка, а не число
    return f"Страница открывалась {visit_counter} раз"


if __name__ == '__main__':
    app.run(debug=True)
