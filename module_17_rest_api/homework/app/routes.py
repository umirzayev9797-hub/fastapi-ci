from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError
from models import init_db, add_book, add_author, delete_author_by_id, get_author_by_id, get_books_by_author, Book
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)


class AuthorList(Resource):
    def post(self):
        try:
            author = AuthorSchema().load(request.json)
            author = add_author(author)
            return AuthorSchema().dump(author), 201
        except ValidationError as exc:
            return exc.messages, 400


class AuthorResource(Resource):
    def get(self, author_id):
        if not get_author_by_id(author_id):
            return {"message": "Author not found"}, 404
        books = get_books_by_author(author_id)
        return BookSchema().dump(books, many=True), 200

    def delete(self, author_id):
        if not get_author_by_id(author_id):
            return {"message": "Author not found"}, 404
        delete_author_by_id(author_id)
        return '', 204


class BookList(Resource):
    def post(self):
        try:
            data = BookSchema().load(request.json)
            # Если в JSON есть объект 'author', создаем его
            if 'author' in data:
                author_obj = add_author(data['author'])
                data['author_id'] = author_obj.id

            new_book = add_book(Book(title=data['title'], author_id=data['author_id']))
            return BookSchema().dump(new_book), 201
        except Exception as e:
            return {"error": str(e)}, 400


api.add_resource(AuthorList, '/api/authors')
api.add_resource(AuthorResource, '/api/authors/<int:author_id>')
api.add_resource(BookList, '/api/books')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)