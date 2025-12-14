"""
Реализуйте endpoint /hello-world/<имя>, который возвращает строку «Привет, <имя>. Хорошей пятницы!».
Вместо хорошей пятницы endpoint должен уметь желать хорошего дня недели в целом, на русском языке.

Пример запроса, сделанного в субботу:

/hello-world/Саша  →  Привет, Саша. Хорошей субботы!
"""
from datetime import datetime
from flask import Flask

app = Flask(__name__)

WEEKDAYS_RU: tuple[str, ...] = (
    'понедельника',
    'вторника',
    'среды',
    'четверга',
    'пятницы',
    'субботы',
    'воскресенья',
)

@app.route('/hello-world/<name>')
def hello_world(name: str) -> str:
    """
        Endpoint приветствует пользователя по имени и желает хорошего дня недели
        на русском языке в родительном падеже.

        :param name: имя пользователя из URL
        :return: приветственное сообщение
        """
    weekday_index: int = datetime.today().weekday()
    weekday_name: str = WEEKDAYS_RU[weekday_index]

    return f'Привет, {name}. Хорошего {weekday_name}!'


if __name__ == '__main__':
    app.run(debug=True)