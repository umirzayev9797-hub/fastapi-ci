import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, case, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Session
from db.database import Base

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    @hybrid_property
    def full_name(self):
        return f"{self.name} {self.surname}"

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, nullable=False)

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    @hybrid_property
    def full_name(self):
        return f"{self.name} {self.surname}"

    # --- ЗАДАНИЕ: Classmethods ---

    @classmethod
    def get_scholarship_students(cls, db: Session):
        """Получить список студентов, имеющих стипендию"""
        return db.query(cls).filter(cls.scholarship == True).all()

    @classmethod
    def get_high_score_students(cls, db: Session, threshold: float):
        """Получить студентов со средним баллом выше порога"""
        return db.query(cls).filter(cls.average_score > threshold).all()

class ReceivingBook(Base):
    __tablename__ = "receiving_books"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime, nullable=True)

    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return:
            delta = self.date_of_return - self.date_of_issue
        else:
            delta = datetime.datetime.now() - self.date_of_issue
        return delta.days

    @count_date_with_book.expression
    def count_date_with_book(cls):
        return case(
            (cls.date_of_return != None,
             func.julianday(cls.date_of_return) - func.julianday(cls.date_of_issue)),
            else_=func.julianday(func.now()) - func.julianday(cls.date_of_issue)
        )