import sqlite3
import csv


def delete_wrong_fees(
        cursor: sqlite3.Cursor,
        wrong_fees_file: str
) -> None:
    # 1. Сначала считываем данные из CSV-файла в список
    with open(wrong_fees_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        # Если в CSV есть заголовок (например, car_number, date),
        # раскомментируй следующую строку, чтобы пропустить его:
        # next(reader)

        # Превращаем данные в список кортежей: [(номер, дата), (номер, дата), ...]
        wrong_data = [tuple(row) for row in reader]

    # 2. Выполняем массовое удаление (executemany)
    # Удаляем только при совпадении И номера автомобиля И даты
    query = """
        DELETE FROM table_fees
        WHERE truck_number = ? AND timestamp = ?
    """

    cursor.executemany(query, wrong_data)


if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        delete_wrong_fees(cursor, "../wrong_fees.csv")
        conn.commit()
