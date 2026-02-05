import sqlite3
import os

def get_toughest_teacher():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.normpath(os.path.join(current_dir, '..', '..', 'homework.db'))

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = '''
            SELECT 
                t.full_name, 
                AVG(ag.grade) as avg_grade
            FROM teachers t
            JOIN assignments a ON t.teacher_id = a.teacher_id
            JOIN assignments_grades ag ON a.assisgnment_id = ag.assisgnment_id
            GROUP BY t.teacher_id
            ORDER BY avg_grade ASC
            LIMIT 1
        '''

        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            print(f"{result[0]} {round(result[1], 2)}")

    except sqlite3.Error as e:
        print(f"Ошибка: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    get_toughest_teacher()