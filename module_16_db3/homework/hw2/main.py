import sqlite3
import os


def run_task(file_num):
    sql_file = f'2_{file_num}.sql'
    # Имя базы из твоего файла generate_hw_database.py
    db_name = 'hw.db'
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', db_name))

    if not os.path.exists(sql_file):
        return

    try:
        # Подключаемся к существующей базе hw.db
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            with open(sql_file, 'r', encoding='utf-8') as f:
                cursor.execute(f.read())

            rows = cursor.fetchall()
            print(f"\n--- Результат {sql_file} ---")
            if not rows:
                print("Данные не найдены.")
            else:
                for row in rows:
                    print(row)
    except Exception as e:
        print(f"Ошибка в {sql_file}: {e}")


if __name__ == "__main__":
    for i in range(1, 6):
        run_task(i)