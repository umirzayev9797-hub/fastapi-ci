import sqlite3
import os

def build_cinema_db():
    sql_path = 'create_schema.sql'
    db_path = 'cinema.db'

    if not os.path.exists(sql_path):
        print(f"Файл {sql_path} не найден!")
        return

    with open(sql_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()
        print("База данных cinema.db успешно создана согласно схеме.")

if __name__ == "__main__":
    build_cinema_db()