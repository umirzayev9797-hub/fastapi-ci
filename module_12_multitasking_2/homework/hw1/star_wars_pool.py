import requests
import sqlite3
import time
import logging
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

BASE_URL = 'https://swapi.dev/api/people/'


def setup_db():
    """Создает базу данных и таблицу"""
    with sqlite3.connect('star_wars_pool.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age TEXT,
                gender TEXT
            )
        ''')
        cursor.execute('DELETE FROM characters')
        conn.commit()


def fetch_and_save(char_id: int) -> None:
    """Функция-воркер: скачивает данные и сохраняет в БД"""
    url = f'{BASE_URL}{char_id}/'
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Записываем в БД (каждый воркер открывает свое соединение)
            with sqlite3.connect('star_wars_pool.db') as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT OR REPLACE INTO characters (id, name, age, gender) VALUES (?, ?, ?, ?)',
                    (char_id, data['name'], data['birth_year'], data['gender'])
                )
                conn.commit()
    except Exception as e:
        logger.error(f"Error with ID {char_id}: {e}")


# --- ВАРИАНТ 1: ThreadPool (Пулы потоков) ---
def run_thread_pool(ids: list, pool_size: int):
    logger.info(f"\nStarting ThreadPool with size {pool_size}...")
    start = time.time()
    with ThreadPool(processes=pool_size) as pool:
        pool.map(fetch_and_save, ids)
    end = time.time()
    logger.info(f"ThreadPool time: {end - start:.2f} seconds")


# --- ВАРИАНТ 2: ProcessPool (Пулы процессов) ---
def run_process_pool(ids: list, pool_size: int):
    logger.info(f"\nStarting ProcessPool with size {pool_size}...")
    start = time.time()
    with Pool(processes=pool_size) as pool:
        pool.map(fetch_and_save, ids)
    end = time.time()
    logger.info(f"ProcessPool time: {end - start:.2f} seconds")


def main():
    char_ids = list(range(1, 21))

    # 1. Тестируем потоки
    setup_db()
    run_thread_pool(char_ids, pool_size=20)

    # 2. Тестируем процессы
    setup_db()
    run_process_pool(char_ids, pool_size=5)  # Попробуем меньшее число ядер


if __name__ == "__main__":
    main()