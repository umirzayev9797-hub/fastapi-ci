import sqlite3
import os

def get_easy_teacher_students():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.normpath(os.path.join(current_dir, '..', '..', 'homework.db'))

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Логика:
        # 1. Находим group_id того задания, за которое средний балл выше всего.
        # 2. Выбираем всех студентов, которые состоят в этой группе.
        query = '''
            SELECT s.full_name
            FROM students s
            WHERE s.group_id = (
                SELECT a.group_id
                FROM assignments a
                JOIN assignments_grades ag ON a.assisgnment_id = ag.assisgnment_id
                GROUP BY a.assisgnment_id
                ORDER BY AVG(CAST(ag.grade AS FLOAT)) DESC
                LIMIT 1
            )
        '''

        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            for row in results:
                print(row[0])
        else:
            # Если по заданиям не вышло, попробуем через teacher_id,
            # но исключив таблицу-посредник students_groups
            query_alt = '''
                SELECT s.full_name
                FROM students s
                WHERE s.group_id IN (
                    SELECT a.group_id
                    FROM assignments a
                    JOIN assignments_grades ag ON a.assisgnment_id = ag.assisgnment_id
                    GROUP BY a.teacher_id
                    ORDER BY AVG(CAST(ag.grade AS FLOAT)) DESC
                    LIMIT 1
                )
            '''
            cursor.execute(query_alt)
            results_alt = cursor.fetchall()
            for row in results_alt:
                print(row[0])

    except sqlite3.Error as e:
        print(f"Ошибка: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    get_easy_teacher_students()