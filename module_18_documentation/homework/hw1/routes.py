from flask import Flask, request
from flask_restful import Api, Resource
from flasgger import Swagger, swag_from
from models import init_db, add_book, add_author, get_all_books, Book
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

# Спецификация для авторов (Python-словарь) — ТРЕБОВАНИЕ ЗАДАЧИ
author_spec = {
    "tags": ["Authors"],
    "parameters": [{
        "name": "body",
        "in": "body",
        "required": True,
        "schema": {
            "id": "Author",
            "required": ["first_name", "last_name"],
            "properties": {
                "first_name": {"type": "string", "example": "Александр"},
                "last_name": {"type": "string", "example": "Пушкин"}
            }
        }
    }],
    "responses": {"201": {"description": "Автор успешно создан"}}
}

class AuthorList(Resource):
    @swag_from(author_spec)
    def post(self):
        author = AuthorSchema().load(request.json)
        author = add_author(author)
        return AuthorSchema().dump(author), 201

class BookList(Resource):
    def get(self):
        """
        Получить список всех книг
        ---
        tags:
          - Books
        responses:
          200:
            description: Список успешно получен
        """
        return BookSchema().dump(get_all_books(), many=True), 200

    @swag_from('books_spec.yml') # YAML файл — ТРЕБОВАНИЕ ЗАДАЧИ
    def post(self):
        data = BookSchema().load(request.json)
        if 'author' in data:
            new_author = add_author(data['author'])
            data['author_id'] = new_author.id
        book = add_book(Book(title=data['title'], author_id=data['author_id']))
        return BookSchema().dump(book), 201

api.add_resource(AuthorList, '/api/authors')
api.add_resource(BookList, '/api/books')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)