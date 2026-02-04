from flask import Flask, request
from flask_restful import Api, Resource
import sqlite3
from werkzeug.serving import WSGIRequestHandler

# Оставляем эту настройку для тестов (+O)
# WSGIRequestHandler.protocol_version = "HTTP/1.1"

app = Flask(__name__)
api = Api(app)
DATABASE_NAME = 'table_books.db'

def init_db():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author_id INTEGER);")

class BookList(Resource):
    def get(self):
        return {"status": "ok"}, 200

api.add_resource(BookList, '/api/books')

if __name__ == '__main__':
    init_db()
    # Запускаем с threaded=True, чтобы сервер не вешался от пачки запросов
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)