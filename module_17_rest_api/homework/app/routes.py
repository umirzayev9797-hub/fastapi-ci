from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError
from models import init_db, add_book, add_author, delete_author_by_id, get_all_books
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)

class AuthorList(Resource):
    def post(self):
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        author = add_author(author)
        return schema.dump(author), 201

class AuthorResource(Resource):
    def delete(self, author_id):
        delete_author_by_id(author_id)
        return '', 204

class BookList(Resource):
    def get(self):
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    def post(self):
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        book = add_book(book)
        return schema.dump(book), 201

api.add_resource(AuthorList, '/api/authors')
api.add_resource(AuthorResource, '/api/authors/<int:author_id>')
api.add_resource(BookList, '/api/books')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)