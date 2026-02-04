import operator
from flask import Flask
from flask_jsonrpc import JSONRPC
from typing import Union

app = Flask(__name__)
# Включаем browsable api для автоматической документации
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

@jsonrpc.method('calc.add')
def add(a: float, b: float) -> float:
    """
    Возвращает сумму двух чисел (a + b).
    """
    return operator.add(a, b)

@jsonrpc.method('calc.subtract')
def subtract(a: float, b: float) -> float:
    """
    Возвращает разность двух чисел (a - b).
    """
    return operator.sub(a, b)

@jsonrpc.method('calc.multiply')
def multiply(a: float, b: float) -> float:
    """
    Возвращает произведение двух чисел (a * b).
    """
    return operator.mul(a, b)

@jsonrpc.method('calc.divide')
def divide(a: float, b: float) -> Union[float, dict]:
    """
    Возвращает результат деления (a / b).
    Если b = 0, возвращает ошибку.
    """
    if b == 0:
        # Это вызовет корректный JSON-RPC Error ответ
        raise ValueError("Division by zero")
    return operator.truediv(a, b)

if __name__ == '__main__':
    # Используем порт 5000, как в твоем примере curl
    app.run('0.0.0.0', port=5000, debug=True)