import json
from flask import Flask, request, jsonify

app = Flask(__name__)

LOG_STORAGE = []

@app.route('/log', methods=['POST'])
def log():
    """
    Записываем полученные логи которые пришли к нам на сервер
    return: текстовое сообщение об успешной записи, статус код успешной работы

    """
    log_record = request.form.to_dict()
    LOG_STORAGE.append(log_record)
    return "OK", 200


@app.route('/logs', methods=['GET'])
def logs():
    """
    Рендерим список полученных логов
    return: список логов обернутый в тег HTML <pre></pre>
    """
    return jsonify(LOG_STORAGE), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000)
# TODO запустить сервер