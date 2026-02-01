from flask import Flask, render_template, redirect, url_for, abort
from typing import Any
from models import init_db, get_all_books, add_new_book, get_books_by_author, get_book_by_id, DATA
from forms import BookForm

app: Flask = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-123'

@app.route('/books')
def all_books() -> str:
    return render_template('index.html', books=get_all_books())

@app.route('/books/<int:book_id>')
def book_details(book_id: int) -> str:
    book = get_book_by_id(book_id)
    if book is None:
        abort(404, description="Book not found")
    return render_template('book_details.html', book=book)

@app.route('/books/form', methods=['GET', 'POST'])
def get_books_form() -> Any:
    form = BookForm()
    if form.validate_on_submit():
        add_new_book(form.book_title.data, form.author_name.data)
        return redirect(url_for('all_books'))
    return render_template('add_book.html', form=form)

@app.route('/books/author/<author_name>')
def books_by_author(author_name: str) -> str:
    books_list = get_books_by_author(author_name)
    return render_template('author_books.html', books=books_list, author_name=author_name)

if __name__ == '__main__':
    init_db(DATA)
    app.run(debug=True)