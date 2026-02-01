import sqlite3


def generate_test_data(
        cursor: sqlite3.Cursor,
        number_of_groups: int
) -> None:
    # 1. Подготавливаем заготовки названий (должно хватить на 16 групп)
    # Нам нужно: 16 сильных, 32 средних (2 на группу) и 16 слабых
    strong_teams = [f"Strong Team {i}" for i in range(1, 17)]
    medium_teams = [f"Medium Team {i}" for i in range(1, 33)]
    weak_teams = [f"Weak Team {i}" for i in range(1, 17)]

    commands_data = []  # Данные для uefa_commands
    draw_data = []  # Данные для uefa_draw

    current_command_id = 1

    # 2. Формируем данные по группам
    for group_num in range(1, number_of_groups + 1):
        # Состав группы: 1 сильная, 2 средних, 1 слабая
        group_setup = [
            (strong_teams.pop(0), "Strong"),
            (medium_teams.pop(0), "Medium"),
            (medium_teams.pop(0), "Medium"),
            (weak_teams.pop(0), "Weak")
        ]

        for team_name, level in group_setup:
            # Данные для первой таблицы: (id, name, country, level)
            commands_data.append((current_command_id, team_name, "Country", level))

            # Данные для второй таблицы: (command_id, group_id)
            draw_data.append((current_command_id, group_num))

            current_command_id += 1

    # 3. Очищаем таблицы перед заполнением (опционально, но полезно)
    cursor.execute("DELETE FROM uefa_commands")
    cursor.execute("DELETE FROM uefa_draw")

    # 4. Массовая вставка через executemany
    cursor.executemany(
        "INSERT INTO uefa_commands (command_number, command_name, command_country, command_level) VALUES (?, ?, ?, ?)",
        commands_data
    )

    cursor.executemany(
        "INSERT INTO uefa_draw (command_number, group_number) VALUES (?, ?)",
        draw_data
    )


if __name__ == '__main__':
    number_of_groups: int = int(input('Введите количество групп (от 4 до 16): '))
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        generate_test_data(cursor, number_of_groups)
        conn.commit()
