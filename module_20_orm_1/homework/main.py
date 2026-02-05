from db.database import engine, Base, SessionLocal
from models.library import Student


def test_student_methods():
    # 1. Создаем таблицы
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 2. Очищаем таблицу перед тестом
        db.query(Student).delete()

        # 3. Добавляем тестовых студентов
        s1 = Student(name="Ivan", surname="Ivanov", phone="111", email="i@ex.com",
                     average_score=4.5, scholarship=True)
        s2 = Student(name="Petr", surname="Petrov", phone="222", email="p@ex.com",
                     average_score=3.8, scholarship=False)
        s3 = Student(name="Sidor", surname="Sidorov", phone="333", email="s@ex.com",
                     average_score=4.9, scholarship=True)

        db.add_all([s1, s2, s3])
        db.commit()

        print("--- ТЕСТ 1: Студенты со стипендией ---")
        lucky_ones = Student.get_scholarship_students(db)
        for s in lucky_ones:
            print(f"Стипендиат: {s.full_name} (Балл: {s.average_score})")

        print("\n--- ТЕСТ 2: Студенты с баллом выше 4.0 ---")
        smart_ones = Student.get_high_score_students(db, 4.0)
        for s in smart_ones:
            print(f"Отличник (>4.0): {s.full_name} (Балл: {s.average_score})")

    except Exception as e:
        print(f"Ошибка: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    test_student_methods()