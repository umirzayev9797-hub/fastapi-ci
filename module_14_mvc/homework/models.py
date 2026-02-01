import sqlite3
from typing import Any, Optional, List

DATA: List[dict] = [
    {'id': 1, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.', 'views': 0},
    {'id': 2, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville', 'views': 0},
    {'id': 3, 'title': 'War and Peace', 'author': 'Leo Tolstoy', 'views': 0},
]

class Book:
    def __init__(self, id: int, title: str, author: str, views: int = 0) -> None:
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.views: int = views

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='table_books';")
        exists = cursor.fetchone()
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `table_books` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT, 
                    author TEXT,
                    views INTEGER DEFAULT 0
                )
                """
            )
            cursor.executemany(
                "INSERT INTO `table_books` (title, author, views) VALUES (?, ?, ?)",
                [(item['title'], item['author'], item.get('views', 0)) for item in initial_records]
            )

def get_all_books() -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        # Увеличиваем просмотры для всех книг при вызове списка
        cursor.execute("UPDATE `table_books` SET views = views + 1")
        cursor.execute("SELECT * from `table_books`")
        return [Book(*row) for row in cursor.fetchall()]

def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        # Увеличиваем просмотр конкретной книги
        cursor.execute("UPDATE `table_books` SET views = views + 1 WHERE id = ?", (book_id,))
        cursor.execute("SELECT * FROM `table_books` WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        return Book(*row) if row else None

def add_new_book(title: str, author: str) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO `table_books` (title, author, views) VALUES (?, ?, 0)", (title, author))

def get_books_by_author(author_name: str) -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `table_books` WHERE author = ?", (author_name,))
        return [Book(*row) for row in cursor.fetchall()]