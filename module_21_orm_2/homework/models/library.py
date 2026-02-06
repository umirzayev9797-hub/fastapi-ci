import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, case, func
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from db.database import Base


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    # 1. Связь One-to-Many с каскадным удалением: удалив автора, удалим и его книги
    # 2. lazy="selectin" — "жадная" подгрузка (вторым отдельным запросом через IN), эффективна для коллекций
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan", lazy="selectin")

    @hybrid_property
    def full_name(self):
        return f"{self.name} {self.surname}"


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)

    # Внешний ключ
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"), nullable=False)

    # 1. back_populates связывает с Author
    # 2. lazy="joined" — "жадная" подгрузка через LEFT OUTER JOIN (сразу одним запросом)
    author = relationship("Author", back_populates="books", lazy="joined")

    receivings = relationship("ReceivingBook", back_populates="book", cascade="all, delete-orphan")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    # Связь с таблицей выдачи
    receivings = relationship("ReceivingBook", back_populates="student", cascade="all, delete-orphan")

    # --- MANY-TO-MANY через AssociationProxy ---
    # Позволяет писать student.books и получать список объектов Book напрямую
    books = association_proxy("receivings", "book")

    @hybrid_property
    def full_name(self):
        return f"{self.name} {self.surname}"


class ReceivingBook(Base):
    __tablename__ = "receiving_books"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    date_of_issue = Column(DateTime, nullable=False, default=datetime.datetime.now)
    date_of_return = Column(DateTime, nullable=True)

    book = relationship("Book", back_populates="receivings", lazy="joined")
    student = relationship("Student", back_populates="receivings", lazy="joined")

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