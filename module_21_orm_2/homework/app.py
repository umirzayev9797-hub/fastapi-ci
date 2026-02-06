from flask import Flask, jsonify
from sqlalchemy import func, extract
from db.database import SessionLocal
from models.library import Book, ReceivingBook, Student
import datetime

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

@app.route('/stats/avg-books-month', methods=['GET'])
def get_avg_books_per_month():
    """
    1. Среднее количество книг, которые студенты брали в этом месяце.
    Логика: (Общее кол-во выдач за месяц) / (Кол-во уникальных студентов, бравших книги).
    """
    db = SessionLocal()
    try:
        today = datetime.date.today()
        # Фильтруем выдачи за текущий месяц и год
        query = db.query(ReceivingBook).filter(
            extract('month', ReceivingBook.date_of_issue) == today.month,
            extract('year', ReceivingBook.date_of_issue) == today.year
        )

        total_issues = query.count()
        unique_students = query.distinct(ReceivingBook.student_id).count()

        avg_value = total_issues / unique_students if unique_students > 0 else 0

        return jsonify({
            "month": today.month,
            "total_issues": total_issues,
            "unique_students": unique_students,
            "average_per_student": round(avg_value, 2)
        }), 200
    finally:
        db.close()


@app.route('/stats/popular-book-high-score', methods=['GET'])
def get_popular_book_for_smart_students():
    """
    2. Самая популярная книга среди студентов со средним баллом > 4.0.
    """
    db = SessionLocal()
    try:
        # Соединяем выдачи с таблицей студентов для фильтрации по баллу
        popular_book = db.query(Book.name, func.count(ReceivingBook.id).label('total')) \
            .join(ReceivingBook, Book.id == ReceivingBook.book_id) \
            .join(Student, Student.id == ReceivingBook.student_id) \
            .filter(Student.average_score > 4.0) \
            .group_by(Book.id) \
            .order_by(func.count(ReceivingBook.id).desc()) \
            .first()

        if not popular_book:
            return jsonify({"message": "Данные не найдены"}), 404

        return jsonify({
            "book_name": popular_book[0],
            "times_taken": popular_book[1]
        }), 200
    finally:
        db.close()


@app.route('/stats/top-students-year', methods=['GET'])
def get_top_students_year():
    db = SessionLocal()
    try:
        today = datetime.date.today()
        top_students = db.query(
            Student.name,
            Student.surname,
            func.count(ReceivingBook.id).label('book_count')
        ) \
            .join(ReceivingBook, Student.id == ReceivingBook.student_id) \
            .filter(extract('year', ReceivingBook.date_of_issue) == today.year) \
            .group_by(Student.id) \
            .order_by(func.count(ReceivingBook.id).desc()) \
            .limit(10) \
            .all()

        # Формируем список словарей
        result = [
            {
                "student_name": f"{s[0]} {s[1]}",
                "books_read": s[2]
            }
            for s in top_students
        ]

        # Благодаря app.config['JSON_AS_ASCII'] = False здесь будет кириллица
        return jsonify(result), 200
    finally:
        db.close()


if __name__ == '__main__':
    app.run(debug=True, port=5000)