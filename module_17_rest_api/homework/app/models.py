import sqlite3
from dataclasses import dataclass
from typing import Optional, List

DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME = 'authors'

@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    id: Optional[int] = None

@dataclass
class Book:
    title: str
    author_id: int
    id: Optional[int] = None

def init_db():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS `{AUTHORS_TABLE_NAME}` (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                middle_name TEXT
            );
        """)
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS `{BOOKS_TABLE_NAME}` (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                FOREIGN KEY (author_id) REFERENCES {AUTHORS_TABLE_NAME}(id) ON DELETE CASCADE
            );
        """)

def add_author(author: Author) -> Author:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO `{AUTHORS_TABLE_NAME}` (first_name, last_name, middle_name) VALUES (?, ?, ?)",
            (author.first_name, author.last_name, author.middle_name)
        )
        author.id = cursor.lastrowid
        return author

def get_author_by_id(author_id: int) -> Optional[Author]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `{AUTHORS_TABLE_NAME}` WHERE id = ?", (author_id,))
        row = cursor.fetchone()
        if row:
            return Author(id=row[0], first_name=row[1], last_name=row[2], middle_name=row[3])

def delete_author_by_id(author_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(f"DELETE FROM `{AUTHORS_TABLE_NAME}` WHERE id = ?", (author_id,))
        conn.commit()

def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO `{BOOKS_TABLE_NAME}` (title, author_id) VALUES (?, ?)",
            (book.title, book.author_id)
        )
        book.id = cursor.lastrowid
        return book

def get_all_books() -> List[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `{BOOKS_TABLE_NAME}`")
        return [Book(id=row[0], title=row[1], author_id=row[2]) for row in cursor.fetchall()]

def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        if row:
            return Book(id=row[0], title=row[1], author_id=row[2])

def update_book(book: Book) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE `{BOOKS_TABLE_NAME}` SET title = ?, author_id = ? WHERE id = ?",
            (book.title, book.author_id, book.id)
        )
        conn.commit()

def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM `{BOOKS_TABLE_NAME}` WHERE id = ?", (book_id,))
        conn.commit()