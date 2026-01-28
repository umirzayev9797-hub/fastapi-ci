import sqlite3

def analyze_island_salaries():
    try:
        # Используем контекстный менеджер
        with sqlite3.connect('hw_4_database.db') as conn:
            cursor = conn.cursor()

            # 1. За чертой бедности (< 5000)
            cursor.execute("SELECT COUNT(*) FROM salaries WHERE salary < 5000")
            poverty_count = cursor.fetchone()[0]

            # 2. Средняя зарплата
            # Используем AVG на стороне БД
            cursor.execute("SELECT AVG(salary) FROM salaries")
            avg_salary = cursor.fetchone()[0]

            # 3. Медианная зарплата
            # В SQLite нет встроенного MEDIAN, используем сортировку и LIMIT
            cursor.execute("""
                SELECT salary FROM salaries 
                ORDER BY salary 
                LIMIT 1 OFFSET (SELECT COUNT(*) FROM salaries) / 2
            """)
            median_salary = cursor.fetchone()[0]

            # 4. Коэффициент социального неравенства F (Опциональное задание одним запросом)
            # Считаем T (Топ 10%) и K (Остальные 90%)
            cursor.execute("""
                SELECT 
                    ROUND(CAST(top_10.sum_t AS REAL) / rest_90.sum_k * 100, 2)
                FROM 
                    (SELECT SUM(salary) as sum_t FROM (
                        SELECT salary FROM salaries ORDER BY salary DESC LIMIT (SELECT COUNT(*) / 10 FROM salaries)
                    )) as top_10,
                    (SELECT SUM(salary) as sum_k FROM (
                        SELECT salary FROM salaries ORDER BY salary ASC LIMIT (SELECT COUNT(*) * 9 / 10 FROM salaries)
                    )) as rest_90
            """)
            inequality_f = cursor.fetchone()[0]

            # Вывод результатов
            print(f"Жителей за чертой бедности: {poverty_count}")
            print(f"Средняя зарплата: {round(avg_salary, 2)} гульденов")
            print(f"Медианная зарплата: {median_salary} гульденов")
            print(f"Коэффициент социального неравенства F: {inequality_f}%")

    except sqlite3.Error as e:
        print(f"Ошибка БД: {e}")

if __name__ == "__main__":
    analyze_island_salaries()