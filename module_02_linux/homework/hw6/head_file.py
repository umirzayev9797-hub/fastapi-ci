"""
Реализуйте endpoint, который показывает превью файла, принимая на вход два параметра: SIZE (int) и RELATIVE_PATH —
и возвращая первые SIZE символов файла по указанному в RELATIVE_PATH пути.

Endpoint должен вернуть страницу с двумя строками.
В первой строке будет содержаться информация о файле: его абсолютный путь и размер файла в символах,
а во второй строке — первые SIZE символов из файла:

<abs_path> <result_size><br>
<result_text>

где abs_path — написанный жирным абсолютный путь до файла;
result_text — первые SIZE символов файла;
result_size — длина result_text в символах.

Перенос строки осуществляется с помощью HTML-тега <br>.

Пример:

/head_file/8/docs/simple.txt
/home/user/module_2/docs/simple.txt 8
hello wo

/head_file/12/docs/simple.txt
/home/user/module_2/docs/simple.txt 12
hello world!
"""
import os
from flask import abort, Flask

app = Flask(__name__)


@app.route("/head_file/<int:size>/<path:relative_path>")
def head_file(size: int, relative_path: str):
    """
        Endpoint возвращает превью файла: первые size символов.

        Формат ответа:
        <b>abs_path</b> result_size<br>
        result_text

        :param size: количество символов для чтения
        :param relative_path: относительный путь к файлу
        :return: HTML-страница с превью файла
        """
    if size < 0:
        abort(400, description='SIZE должен быть неотрицательным')

    abs_path: str = os.path.abspath(relative_path)

    if not os.path.isfile(abs_path):
        abort(404, description='Файл не найден')

    try:
        with open(abs_path, 'r', encoding='utf-8') as file:
            result_text: str = file.read(size)
    except OSError:
        abort(500, description='Не удалось прочитать файл')

    result_size: int = len(result_text)

    return (
        f'<b>{abs_path}</b> {result_size}<br>'
        f'{result_text}'
    )


if __name__ == "__main__":
    app.run(debug=True)
