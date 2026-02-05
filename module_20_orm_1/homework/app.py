from flask import Flask, request, jsonify
from db.database import SessionLocal, engine, Base
from models.library import Book, ReceivingBook, Student
import datetime

app = Flask(__name__)

# Инициализируем БД при запуске приложения
Base.metadata.create_all(bind=engine)


@app.route('/books', methods=['GET'])
def get_all_books():
    """1. Получить все книги в библиотеке"""
    db = SessionLocal()
    books = db.query(Book).all()
    result = [
        {"id": b.id, "name": b.name, "count": b.count, "release_date": str(b.release_date)}
        for b in books
    ]
    db.close()
    return jsonify(result), 200


@app.route('/debtors', methods=['GET'])
def get_debtors():
    """2. Получить список должников (более 14 дней)"""
    db = SessionLocal()
    # Используем наше гибридное свойство прямо в фильтре SQL!
    debtors = db.query(ReceivingBook).filter(ReceivingBook.count_date_with_book > 14).all()

    result = [
        {"id": d.id, "student_id": d.student_id, "book_id": d.book_id, "days": d.count_date_with_book}
        for d in debtors
    ]
    db.close()
    return jsonify(result), 200


@app.route('/issue', methods=['POST'])
def issue_book():
    """3. Выдать книгу студенту"""
    data = request.json
    book_id = data.get('book_id')
    student_id = data.get('student_id')

    db = SessionLocal()
    new_issuance = ReceivingBook(
        book_id=book_id,
        student_id=student_id,
        date_of_issue=datetime.datetime.now()
    )
    db.add(new_issuance)
    db.commit()
    db.close()
    return jsonify({"message": "Книга успешно выдана", "student_id": student_id}), 201


@app.route('/return', methods=['POST'])
def return_book():
    """4. Сдать книгу в библиотеку"""
    data = request.json
    book_id = data.get('book_id')
    student_id = data.get('student_id')

    db = SessionLocal()
    # Ищем активную запись (где книга еще не возвращена)
    record = db.query(ReceivingBook).filter(
        ReceivingBook.book_id == book_id,
        ReceivingBook.student_id == student_id,
        ReceivingBook.date_of_return == None
    ).first()

    if not record:
        db.close()
        return jsonify({"error": "Запись о выдаче не найдена или книга уже сдана"}), 404

    record.date_of_return = datetime.datetime.now()
    db.commit()
    db.close()
    return jsonify({"message": "Книга успешно возвращена"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)