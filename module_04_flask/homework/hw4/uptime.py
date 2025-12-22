"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""

from flask import Flask
import subprocess
import shlex

app = Flask(__name__)


@app.route("/uptime", methods=['GET'])
def uptime() -> str:
    command_str = "uptime -p"
    command = shlex.split(command_str)

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    uptime_value = result.stdout.strip()

    return f"Current uptime is {uptime_value}"


if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0")
