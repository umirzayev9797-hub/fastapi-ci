"""
Реализуйте приложение для учёта финансов, умеющее запоминать, сколько денег было потрачено за день,
а также показывать затраты за отдельный месяц и за целый год.

В программе должно быть три endpoints:

/add/<date>/<int:number> — сохранение информации о совершённой в рублях трате за какой-то день;
/calculate/<int:year> — получение суммарных трат за указанный год;
/calculate/<int:year>/<int:month> — получение суммарных трат за указанные год и месяц.

Дата для /add/ передаётся в формате YYYYMMDD, где YYYY — год, MM — месяц (от 1 до 12), DD — число (от 01 до 31).
Гарантируется, что переданная дата имеет такой формат и она корректна (никаких 31 февраля).
"""

from flask import Flask

app = Flask(__name__)

# Хранилище расходов:
# {
#   year: {
#       'total': int,
#       month: {
#           'total': int
#       }
#   }
# }
storage: dict[int, dict] = {}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int):
    """
       Сохраняет информацию о расходе за указанную дату.

       :param date: дата в формате YYYYMMDD
       :param number: сумма расхода в рублях
       :return: подтверждающее сообщение
       """
    year: int = int(date[:4])
    month: int = int(date[4:6])

    year_data = storage.setdefault(year, {'total': 0})
    month_data = year_data.setdefault(month, {'total': 0})

    year_data['total'] += number
    month_data['total'] += number

    return 'Расход сохранён'


@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    """
       Возвращает суммарные расходы за указанный год.

       :param year: год
       :return: сумма расходов
       """
    if year not in storage:
        return '0'

    return str(storage[year]['total'])


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    """
       Возвращает суммарные расходы за указанные год и месяц.

       :param year: год
       :param month: месяц
       :return: сумма расходов
       """
    if year not in storage or month not in storage[year]:
        return '0'

    return str(storage[year][month]['total'])


if __name__ == "__main__":
    app.run(debug=True)
