import sqlite3

# Имя менеджера выносим в константу для удобства
MANAGER_NAME = "Иван Совин"

def ivan_sovin_the_most_effective(
        cursor: sqlite3.Cursor,
        name: str,
) -> None:
    # 1. Получаем зарплату Ивана Совина и сотрудника
    # Используем LIKE, как советовали в условии
    query_get_salaries = """
        SELECT name, salary 
        FROM table_effective_manager 
        WHERE name IN (?, ?)
    """
    cursor.execute(query_get_salaries, (MANAGER_NAME, name))
    results = dict(cursor.fetchall())

    manager_salary = results.get(MANAGER_NAME)
    employee_salary = results.get(name)

    # Если сотрудника нет в базе или это сам Иван Совин — ничего не делаем
    if employee_salary is None or name == MANAGER_NAME:
        print(f"Сотрудник {name} не найден или является эффективным менеджером.")
        return

    # 2. Рассчитываем новую зарплату (+10%)
    new_salary = employee_salary * 1.1

    # 3. Принимаем управленческое решение
    if new_salary > manager_salary:
        # Увольняем (удаляем из БД)
        print(f"Зарплата {name} превысит зарплату менеджера. Сотрудник уволен.")
        cursor.execute(
            "DELETE FROM table_effective_manager WHERE name = ?",
            (name,)
        )
    else:
        # Повышаем зарплату
        print(f"Зарплата {name} успешно повышена до {new_salary:.2f}")
        cursor.execute(
            "UPDATE table_effective_manager SET salary = ? WHERE name = ?",
            (new_salary, name)
        )

if __name__ == '__main__':
    name: str = input('Введите имя сотрудника: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        ivan_sovin_the_most_effective(cursor, name)
        conn.commit()