import sqlite3
from dataclasses import dataclass
from typing import Optional, List

DATABASE_NAME = 'table_books.db'

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
        cursor.execute("CREATE TABLE IF NOT EXISTS authors (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL, last_name TEXT NOT NULL, middle_name TEXT);")
        cursor.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, author_id INTEGER NOT NULL, FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE);")

def add_author(author: Author) -> Author:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (first_name, last_name, middle_name) VALUES (?, ?, ?)", (author.first_name, author.last_name, author.middle_name))
        author.id = cursor.lastrowid
        return author

def get_author_by_id(author_id: int) -> Optional[Author]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (author_id,))
        row = cursor.fetchone()
        return Author(id=row[0], first_name=row[1], last_name=row[2], middle_name=row[3]) if row else None

def get_all_books():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        return [Book(id=row[0], title=row[1], author_id=row[2]) for row in cursor.fetchall()]

def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author_id) VALUES (?, ?)", (book.title, book.author_id))
        book.id = cursor.lastrowid
        return book