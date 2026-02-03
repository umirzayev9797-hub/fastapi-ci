from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError
from models import (
    init_db, add_book, add_author, delete_author_by_id,
    get_all_books, get_book_by_id, update_book, delete_book_by_id, get_author_by_id
)
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)


class AuthorList(Resource):
    def post(self):
        data = request.json
        try:
            author = AuthorSchema().load(data)
        except ValidationError as exc:
            return exc.messages, 400
        author = add_author(author)
        return AuthorSchema().dump(author), 201


class AuthorResource(Resource):
    def delete(self, author_id):
        delete_author_by_id(author_id)
        return '', 204


class BookList(Resource):
    def get(self):
        return BookSchema().dump(get_all_books(), many=True), 200

    def post(self):
        data = request.json
        try:
            book_data = BookSchema().load(data)
        except ValidationError as exc:
            return exc.messages, 400

        if not get_author_by_id(book_data.author_id):
            return {"author_id": ["Author not found"]}, 400

        book = add_book(book_data)
        return BookSchema().dump(book), 201


class BookResource(Resource):
    def get(self, book_id):
        book = get_book_by_id(book_id)
        if not book:
            return {"message": "Book not found"}, 404
        return BookSchema().dump(book), 200

    def put(self, book_id):
        if not get_book_by_id(book_id):
            return {"message": "Book not found"}, 404
        try:
            updated_book = BookSchema().load(request.json)
        except ValidationError as exc:
            return exc.messages, 400

        if not get_author_by_id(updated_book.author_id):
            return {"author_id": ["Author not found"]}, 400

        updated_book.id = book_id
        update_book(updated_book)
        return BookSchema().dump(updated_book), 200

    def patch(self, book_id):
        book_obj = get_book_by_id(book_id)
        if not book_obj:
            return {"message": "Book not found"}, 404

        data = request.json
        if 'title' in data:
            book_obj.title = data['title']
        if 'author_id' in data:
            if not get_author_by_id(data['author_id']):
                return {"author_id": ["Author not found"]}, 400
            book_obj.author_id = data['author_id']

        update_book(book_obj)
        return BookSchema().dump(book_obj), 200

    def delete(self, book_id):
        if not get_book_by_id(book_id):
            return {"message": "Book not found"}, 404
        delete_book_by_id(book_id)
        return '', 204


api.add_resource(AuthorList, '/api/authors')
api.add_resource(AuthorResource, '/api/authors/<int:author_id>')
api.add_resource(BookList, '/api/books')
api.add_resource(BookResource, '/api/books/<int:book_id>')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)