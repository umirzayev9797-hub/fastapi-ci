import sqlite3


def check_if_vaccine_has_spoiled(
        cursor: sqlite3.Cursor,
        truck_number: str
) -> bool:
    """
    Проверяет, испортилась ли вакцина в конкретном грузовике.
    Вакцина испорчена, если температура была вне диапазона [-20, -16]
    три и более раз.
    """
    # SQL-запрос считает количество записей с нарушением температурного режима
    # Используем NOT BETWEEN для поиска значений ВНЕ нормы
    query = """
        SELECT COUNT(*)
        FROM table_truck_with_vaccine
        WHERE truck_number = ? 
          AND temperature_in_celsius NOT BETWEEN -20 AND -16
    """

    # Выполняем запрос с параметризацией (защита от инъекций)
    cursor.execute(query, (truck_number,))

    # Извлекаем результат (первое число из кортежа)
    bad_measurements_count = cursor.fetchone()[0]

    # Если нарушений 3 или больше — возвращаем True (испорчено)
    return bad_measurements_count >= 3

if __name__ == '__main__':
    truck_number: str = input('Введите номер грузовика: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        spoiled: bool = check_if_vaccine_has_spoiled(cursor, truck_number)
        print('Испортилась' if spoiled else 'Не испортилась')
        conn.commit()
