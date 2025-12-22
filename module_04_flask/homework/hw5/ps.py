"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""

import shlex
import subprocess
from flask import Flask, request
from flask import Flask

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> str:
    # 1. Получаем аргументы командной строки списком
    args: list[str] = request.args.getlist("arg")

    # 2. Безопасно экранируем каждый аргумент
    safe_args = [shlex.quote(arg) for arg in args]

    # 3. Формируем команду ps с аргументами
    command = ["ps"] + safe_args

    # 4. Выполняем команду
    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    # 5. Возвращаем результат в <pre>
    return f"<pre>{result.stdout}</pre>"


if __name__ == "__main__":
    app.run(debug=True, host = "0.0.0.0")
