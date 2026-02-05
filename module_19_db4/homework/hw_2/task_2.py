import sqlite3
import os

def get_top_students():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.normpath(os.path.join(current_dir, '..', '..', 'homework.db'))

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Используем CAST для точности и LIMIT 10 для картриджа
    query = '''
        SELECT 
            s.full_name, 
            AVG(CAST(ag.grade AS FLOAT)) as avg_grade
        FROM students s
        JOIN assignments_grades ag ON s.student_id = ag.student_id
        GROUP BY s.student_id
        ORDER BY avg_grade DESC
        LIMIT 10
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        # row[0] - имя, row[1] - средний балл
        print(f"{row[0]} {round(row[1], 2)}")

    conn.close()

if __name__ == "__main__":
    get_top_students()