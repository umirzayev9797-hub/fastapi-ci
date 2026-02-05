import sqlite3
import os

def get_late_assignments_stats():
    # Путь к базе данных в корне проекта
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.normpath(os.path.join(current_dir, '..', '..', 'homework.db'))

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Вложенный запрос (подзапрос в FROM):
        # 1. Сначала считаем количество просрочек для каждой группы
        # 2. Оборачиваем это во внешний запрос для статистики
        query = '''
            SELECT 
                AVG(late_count), 
                MAX(late_count), 
                MIN(late_count)
            FROM (
                SELECT COUNT(*) as late_count
                FROM assignments a
                JOIN assignments_grades ag ON a.assisgnment_id = ag.assisgnment_id
                WHERE ag.date > a.due_date
                GROUP BY a.group_id
            )
        '''

        cursor.execute(query)
        result = cursor.fetchone()

        if result and result[0] is not None:
            print(f"Среднее количество просрочек: {round(result[0], 2)}")
            print(f"Максимальное количество просрочек: {result[1]}")
            print(f"Минимальное количество просрочек: {result[2]}")
        else:
            print("Просроченных заданий не найдено.")

    except sqlite3.Error as e:
        print(f"Ошибка: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    get_late_assignments_stats()