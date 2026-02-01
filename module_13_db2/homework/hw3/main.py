import sqlite3
import datetime

def log_bird(
        cursor: sqlite3.Cursor,
        bird_name: str,
        date_time: str,
) -> None:
    """
    Добавляет новую запись о наблюдении птицы в таблицу table_birds.
    """
    # Используем параметризацию для защиты от инъекций
    query = """
        INSERT INTO table_birds (bird_name, timestamp)
        VALUES (?, ?)
    """
    cursor.execute(query, (bird_name, date_time))


def check_if_such_bird_already_seen(
        cursor: sqlite3.Cursor,
        bird_name: str
) -> bool:
    """
    Проверяет, встречалась ли такая птица в базе ранее.
    Использует оператор EXISTS для оптимальной проверки.
    """
    # EXISTS возвращает 1, если найдена хотя бы одна запись, и 0, если нет
    query = """
        SELECT EXISTS(
            SELECT 1 
            FROM table_birds 
            WHERE bird_name = ?
        )
    """
    cursor.execute(query, (bird_name,))

    # Извлекаем результат (будет 0 или 1) и конвертируем в bool
    result = cursor.fetchone()[0]
    return bool(result)

if __name__ == "__main__":
    print("Программа помощи ЮНатам v0.1")
    name: str = input("Пожалуйста введите имя птицы\n> ")
    count_str: str = input("Сколько птиц вы увидели?\n> ")
    count: int = int(count_str)
    right_now: str = datetime.datetime.utcnow().isoformat()

    with sqlite3.connect("../homework.db") as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        log_bird(cursor, name, right_now)

        if check_if_such_bird_already_seen(cursor, name):
            print("Такую птицу мы уже наблюдали!")
