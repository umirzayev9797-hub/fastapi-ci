import datetime
from db.database import engine, Base, SessionLocal
from models.library import Author, Book, Student, ReceivingBook


def test_new_logic():
    Base.metadata.drop_all(bind=engine)  # Сбрасываем базу, чтобы применить ForeignKey
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 1. Массовая вставка и связи
        author = Author(name="Лев", surname="Толстой")
        book1 = Book(name="Война и мир", release_date=datetime.date(1869, 1, 1))
        book2 = Book(name="Анна Каренина", release_date=datetime.date(1877, 1, 1))

        author.books.extend([book1, book2])
        db.add(author)

        student = Student(name="Иван", surname="Иванов", phone="123", email="i@ex.com",
                          average_score=4.8, scholarship=True)
        db.add(student)
        db.commit()

        # 2. Выдача книги (AssociationProxy в действии)
        rec = ReceivingBook(book=book1, student=student, date_of_issue=datetime.datetime.now())
        db.add(rec)
        db.commit()

        # Теперь мы можем получить книги студента напрямую!
        print(f"Студент {student.full_name} взял книги: {[b.name for b in student.books]}")

        # 3. Демонстрация CASCADE
        print(f"Книг в базе до удаления автора: {db.query(Book).count()}")
        db.delete(author)
        db.commit()
        print(f"Книг в базе после удаления автора (CASCADE): {db.query(Book).count()}")

    finally:
        db.close()


if __name__ == "__main__":
    test_new_logic()