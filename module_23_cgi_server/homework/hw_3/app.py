import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/long_task')
def long_task():
    # Имитируем тяжелую задачу на 5 минут (300 секунд)
    time.sleep(300)
    return jsonify(message='We did it!')

if __name__ == '__main__':
    app.run()