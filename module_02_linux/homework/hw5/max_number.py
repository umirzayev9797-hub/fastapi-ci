"""
Реализуйте endpoint, начинающийся с /max_number, в который можно передать список чисел, разделённых слешем /.
Endpoint должен вернуть текст «Максимальное переданное число {number}»,
где number — выделенное курсивом наибольшее из переданных чисел.

Примеры:

/max_number/10/2/9/1
Максимальное число: 10

/max_number/1/1/1/1/1/1/1/2
Максимальное число: 2

"""

from flask import abort, Flask

app = Flask(__name__)


@app.route("/max_number/<path:numbers>")
def max_number(numbers: str) -> str:
    """
        Endpoint принимает список чисел, разделённых символом '/',
        и возвращает максимальное из них.

        Поддерживаются:
        - целые числа
        - отрицательные числа
        - числа с плавающей точкой

        :param numbers: строка вида '10/2/9/1'
        :return: текст с максимальным числом
        """
    parts: list[str] = numbers.split('/')
    parsed_numbers: list[float] = []

    for part in parts:
        try:
            parsed_numbers.append(float(part))
        except ValueError:
            abort(400, description=f'Некорректное значение: {part}')

    if not parsed_numbers:
        abort(400, description='Список чисел пуст')

    max_value: float = max(parsed_numbers)

    # Если число целое — выводим без .0
    if max_value.is_integer():
        max_value = int(max_value)

    return f'Максимальное число: <i>{max_value}</i>'


if __name__ == "__main__":
    app.run(debug=True)
