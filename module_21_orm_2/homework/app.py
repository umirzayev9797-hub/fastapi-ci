from flask import Flask, request, jsonify
from sqlalchemy import func
from db.database import SessionLocal
from models.library import Book, ReceivingBook, Author, Student

app = Flask(__name__)


@app.route('/books/author/<int:author_id>', methods=['GET'])
def get_books_count_by_author(author_id):
    """
    1. Получить количество оставшихся книг конкретного автора.
    Считаем сумму поля 'count' для всех книг автора.
    """
    db = SessionLocal()
    try:
        # Используем func.sum для агрегации
        total_count = db.query(func.sum(Book.count)) \
            .filter(Book.author_id == author_id) \
            .scalar()  # scalar() вернет число, а не кортеж

        return jsonify({
            "author_id": author_id,
            "remaining_books_count": total_count if total_count else 0
        }), 200
    finally:
        db.close()


@app.route('/recommendations/<int:student_id>', methods=['GET'])
def get_recommendations(student_id):
    """
    2. Список книг, которые студент не читал, но авторов которых он уже знает.
    """
    db = SessionLocal()
    try:
        # Шаг A: Находим ID всех книг, которые студент УЖЕ читал
        read_books_ids = db.query(ReceivingBook.book_id) \
            .filter(ReceivingBook.student_id == student_id) \
            .subquery()

        # Шаг B: Находим ID всех авторов, книги которых этот студент брал
        authors_student_knows = db.query(Book.author_id) \
            .filter(Book.id.in_(read_books_ids)) \
            .distinct().subquery()

        # Шаг C: Находим книги этих авторов, которые НЕ входят в список прочитанных
        recommended_books = db.query(Book).filter(
            Book.author_id.in_(authors_student_knows),
            Book.id.not_in(read_books_ids)
        ).all()

        result = [
            {"id": b.id, "name": b.name, "author_id": b.author_id}
            for b in recommended_books
        ]

        return jsonify(result), 200
    finally:
        db.close()


if __name__ == '__main__':
    app.run(debug=True, port=5000)