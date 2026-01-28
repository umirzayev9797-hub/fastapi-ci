import sqlite3


def analyze_tables():
    try:
        # Все запросы делаются в рамках одного подключения
        with sqlite3.connect('hw_3_database.db') as conn:
            cursor = conn.cursor()

            # 1. Сколько записей в каждой таблице?
            # Используем COUNT(*), чтобы не выгружать строки в Python
            results_count = {}
            for i in range(1, 4):
                cursor.execute(f"SELECT COUNT(*) FROM table_{i}")
                results_count[f"table_{i}"] = cursor.fetchone()[0]  # fetchone() для одной строки

            # 2. Сколько в table_1 уникальных записей?
            # DISTINCT находит уникальные, а COUNT их считает
            cursor.execute("SELECT COUNT(DISTINCT value) FROM table_1")
            unique_t1 = cursor.fetchone()[0]

            # 3. Как много записей из table_1 встречается в table_2?
            # INTERSECT находит общие строки между двумя запросами
            cursor.execute("""
                SELECT COUNT(*) FROM (
                    SELECT value FROM table_1
                    INTERSECT
                    SELECT value FROM table_2
                )
            """)
            intersect_1_2 = cursor.fetchone()[0]

            # 4. Как много записей из table_1 встречается и в table_2, и в table_3?
            # Цепочка INTERSECT для нахождения общих элементов в трех таблицах
            cursor.execute("""
                SELECT COUNT(*) FROM (
                    SELECT value FROM table_1
                    INTERSECT
                    SELECT value FROM table_2
                    INTERSECT
                    SELECT value FROM table_3
                )
            """)
            intersect_all = cursor.fetchone()[0]

            # Вывод результатов
            print(f"1. Количество записей: {results_count}")
            print(f"2. Уникальных записей в table_1: {unique_t1}")
            print(f"3. Общих записей (table_1 и table_2): {intersect_1_2}")
            print(f"4. Общих записей (во всех трех таблицах): {intersect_all}")

    except sqlite3.Error as e:
        print(f"Ошибка БД: {e}")


if __name__ == "__main__":
    analyze_tables()