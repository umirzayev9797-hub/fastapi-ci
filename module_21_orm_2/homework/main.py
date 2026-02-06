import datetime
from db.database import engine, Base, SessionLocal
from models.library import Author, Book, Student, ReceivingBook


def seed_data():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Авторы
    a1 = Author(name="Лев", surname="Толстой")
    a2 = Author(name="Александр", surname="Пушкин")

    # Книги Толстого
    b1 = Book(name="Война и мир", count=5, release_date=datetime.date(1869, 1, 1), author=a1)
    b2 = Book(name="Анна Каренина", count=3, release_date=datetime.date(1877, 1, 1), author=a1)
    b3 = Book(name="Смерть Ивана Ильича", count=2, release_date=datetime.date(1886, 1, 1), author=a1)

    # Книги Пушкина
    b4 = Book(name="Евгений Онегин", count=10, release_date=datetime.date(1833, 1, 1), author=a2)

    # Студент
    s = Student(name="Иван", surname="Иванов", phone="1", email="i@ex.com", average_score=5.0, scholarship=True)

    db.add_all([a1, a2, b1, b2, b3, b4, s])
    db.commit()

    # Студент читал ТОЛЬКО "Война и мир"
    rec = ReceivingBook(book_id=b1.id, student_id=s.id, date_of_issue=datetime.datetime.now())
    db.add(rec)
    db.commit()
    db.close()
    print("Данные для теста загружены.")


if __name__ == "__main__":
    seed_data()