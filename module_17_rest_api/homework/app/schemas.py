from marshmallow import Schema, fields, post_load
from models import Author, Book

class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str(allow_none=True)

    @post_load
    def create_author(self, data, **kwargs):
        return Author(**data)

class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author_id = fields.Int()
    author = fields.Nested(AuthorSchema) # Для создания автора при добавлении книги

    @post_load
    def create_book(self, data, **kwargs):
        return data