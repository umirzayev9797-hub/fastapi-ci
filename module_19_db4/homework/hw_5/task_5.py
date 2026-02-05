import sqlite3
import os


def get_groups_analysis():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.normpath(os.path.join(current_dir, '..', '..', 'homework.db'))

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = '''
            SELECT 
                s.group_id,
                COUNT(DISTINCT s.student_id) AS total_students,
                ROUND(AVG(CAST(ag.grade AS FLOAT)), 2) AS avg_grade,
                (
                    SELECT COUNT(DISTINCT s2.student_id)
                    FROM students s2
                    WHERE s2.group_id = s.group_id AND s2.student_id NOT IN (SELECT student_id FROM assignments_grades)
                ) AS missing_submissions,
                COUNT(DISTINCT CASE WHEN ag.date > a.due_date THEN s.student_id END) AS late_students,
                (
                    SELECT COUNT(*) 
                    FROM (
                        SELECT student_id, assisgnment_id 
                        FROM assignments_grades 
                        GROUP BY student_id, assisgnment_id 
                        HAVING COUNT(*) > 1
                    ) AS duplicates
                    JOIN students s3 ON s3.student_id = duplicates.student_id
                    WHERE s3.group_id = s.group_id
                ) AS re_attempts
            FROM students s
            LEFT JOIN assignments_grades ag ON s.student_id = ag.student_id
            LEFT JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
            GROUP BY s.group_id
        '''

        cursor.execute(query)
        results = cursor.fetchall()

        print(
            f"{'Группа':<10} | {'Учеников':<10} | {'Ср. балл':<10} | {'Не сдали':<10} | {'Просрочки':<10} | {'Повторы':<10}")
        print("-" * 80)

        for row in results:
            print(f"{row[0]:<10} | {row[1]:<10} | {row[2] or 0:<10} | {row[3]:<10} | {row[4]:<10} | {row[5]:<10}")

    except sqlite3.Error as e:
        print(f"Ошибка: {e}")
    finally:
        if 'conn' in locals():
            conn.close()


if __name__ == "__main__":
    get_groups_analysis()