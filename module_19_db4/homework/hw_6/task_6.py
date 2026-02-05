import sqlite3
import os

def get_avg_grade_for_reading_tasks():
    # Путь к базе данных
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.normpath(os.path.join(current_dir, '..', '..', 'homework.db'))

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = '''
            SELECT AVG(CAST(grade AS FLOAT))
            FROM assignments_grades
            WHERE assisgnment_id IN (
                SELECT assisgnment_id
                FROM assignments
                WHERE assignment_text LIKE '%прочитать%' 
                   OR assignment_text LIKE '%выучить%'
            )
        '''

        cursor.execute(query)
        result = cursor.fetchone()

        if result and result[0] is not None:
            print(f"Средняя оценка за задания на чтение и заучивание: {round(result[0], 2)}")
        else:
            print("Задания с такими ключевыми словами не найдены.")

    except sqlite3.Error as e:
        print(f"Ошибка: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    get_avg_grade_for_reading_tasks()