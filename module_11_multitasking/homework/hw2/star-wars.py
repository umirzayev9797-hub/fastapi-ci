import requests
import sqlite3
import threading
import time
import logging

# Настройка логирования
logging.basicConfig(level='INFO', format='%(message)s')
logger = logging.getLogger(__name__)

# Блокировка для безопасной записи в БД из разных потоков
db_lock = threading.Lock()


def setup_db():
    """Создает базу данных и таблицу"""
    with sqlite3.connect('star_wars.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age TEXT,
                gender TEXT
            )
        ''')
        # Очистим таблицу перед тестом
        cursor.execute('DELETE FROM characters')
        conn.commit()


def save_to_db(char_id, name, age, gender):
    """Безопасная запись в БД с использованием Lock"""
    with db_lock:
        with sqlite3.connect('star_wars.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO characters (id, name, age, gender) VALUES (?, ?, ?, ?)',
                (char_id, name, age, gender)
            )
            conn.commit()


def get_character_data(char_id):
    """Запрос данных одного персонажа"""
    url = f'https://swapi.dev/api/people/{char_id}/'
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # В API возраст называется 'birth_year'
            return data['name'], data['birth_year'], data['gender']
    except Exception as e:
        logger.error(f"Error fetching ID {char_id}: {e}")
    return None


# --- ВАРИАНТ 1: ПОСЛЕДОВАТЕЛЬНО ---
def fetch_sequentially(ids):
    logger.info("Starting sequential fetch...")
    for char_id in ids:
        res = get_character_data(char_id)
        if res:
            save_to_db(char_id, *res)


# --- ВАРИАНТ 2: ПАРАЛЛЕЛЬНО ---
def fetch_parallel(ids):
    logger.info("Starting parallel fetch...")
    threads = []

    def worker(char_id):
        res = get_character_data(char_id)
        if res:
            save_to_db(char_id, *res)

    for char_id in ids:
        thread = threading.Thread(target=worker, args=(char_id,))
        threads.append(thread)
        thread.start()  # Сначала всех запускаем

    for thread in threads:
        thread.join()  # Потом всех ждем


def main():
    setup_db()
    char_ids = list(range(1, 21))

    # Тест 1: Последовательно
    start = time.time()
    fetch_sequentially(char_ids)
    seq_time = time.time() - start
    logger.info(f"Sequential time: {seq_time:.2f} seconds")

    # Сброс БД для чистоты эксперимента
    setup_db()

    # Тест 2: Параллельно
    start = time.time()
    fetch_parallel(char_ids)
    par_time = time.time() - start
    logger.info(f"Parallel time: {par_time:.2f} seconds")

    logger.info(f"\nSpeedup: {seq_time / par_time:.1f}x faster!")


if __name__ == "__main__":
    main()