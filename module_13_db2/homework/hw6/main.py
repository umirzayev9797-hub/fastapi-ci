import sqlite3


def update_work_schedule(cursor: sqlite3.Cursor) -> None:
    # 1. Явно запрашиваем только ID и Хобби.
    # Если в DBeaver колонка называется просто hobby, убери 'preferable_'
    cursor.execute("SELECT id, preferable_sport FROM table_friendship_employees")
    employees = cursor.fetchall()

    # Соответствие дней недели и хобби (0 - Пн, 6 - Вс)
    days_to_hobbies = {
        0: "футбол",
        1: "хоккей",
        2: "шахматы",
        3: "SUP-сёрфинг",
        4: "бокс",
        5: "Dota2",
        6: "шахбокс"
    }

    # 2. Очищаем старое расписание
    cursor.execute("DELETE FROM table_friendship_schedule")

    new_schedule = []
    employee_index = 0
    total_employees = len(employees)

    # Проходим по всем 366 дням
    for day_number in range(366):
        day_of_week = day_number % 7
        forbidden_hobby = days_to_hobbies[day_of_week]

        day_team = []
        attempts = 0

        # Набираем 10 человек в смену
        while len(day_team) < 10 and attempts < total_employees:
            employee = employees[employee_index]
            # Берем только первые два элемента, сколько бы их там ни было
            emp_id = employee[0]
            emp_hobby = employee[1]

            if emp_hobby != forbidden_hobby:
                day_team.append((day_number, emp_id))

            # Сдвигаем индекс к следующему сотруднику
            employee_index = (employee_index + 1) % total_employees
            attempts += 1

        new_schedule.extend(day_team)

    # 3. Записываем обновленное расписание в БД
    cursor.executemany(
        "INSERT INTO table_friendship_schedule (date, employee_id) VALUES (?, ?)",
        new_schedule
    )

if __name__ == '__main__':
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        update_work_schedule(cursor)
        conn.commit()
