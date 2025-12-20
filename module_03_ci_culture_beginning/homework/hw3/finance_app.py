from flask import Flask, request, jsonify

app = Flask(__name__)

# Простое хранилище: ключ = дата YYYYMMDD, значение = сумма
storage = {}


@app.route('/add/', methods=['POST'])
def add():
    """
    Добавляет запись о финансовой операции
    Формат даты: YYYYMMDD
    sum: сумма операции (целое число)
    """
    date = request.form.get('date')
    sum_str = request.form.get('sum')

    # Проверка формата даты
    if not date or len(date) != 8 or not date.isdigit():
        raise ValueError("Неверный формат даты, ожидается YYYYMMDD")

    try:
        value = int(sum_str)
    except (TypeError, ValueError):
        raise ValueError("Сумма должна быть целым числом")

    # Добавление суммы к уже существующей дате
    if date in storage:
        storage[date] += value
    else:
        storage[date] = value

    return jsonify({"status": "ok", "date": date, "sum": storage[date]}), 200


@app.route('/calculate/', methods=['GET'])
def calculate():
    """
    Возвращает общий итог по всем операциям
    Можно добавить диапазон дат через query string: ?from=YYYYMMDD&to=YYYYMMDD
    """
    from_date = request.args.get('from')
    to_date = request.args.get('to')

    total = 0
    for date_str, value in storage.items():
        if from_date and date_str < from_date:
            continue
        if to_date and date_str > to_date:
            continue
        total += value

    return jsonify({"total": total}), 200


if __name__ == '__main__':
    app.run(debug=True)
