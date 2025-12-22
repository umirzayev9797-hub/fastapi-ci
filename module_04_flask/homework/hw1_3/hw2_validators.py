"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""
from typing import Optional
from flask_wtf import FlaskForm
from wtforms import Field
from wtforms import ValidationError

# Способ 1: Класс (используется как NumberLength(min=10, max=10))
class NumberLength:
    def __init__(self, min: int, max: int, message: str = None):
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form, field):
        if field.data is None:
            data_len = 0
        else:
            data_len = len(str(abs(field.data)))

        if data_len < self.min or data_len > self.max:
            raise ValidationError(
                self.message or f"Длина должна быть от {self.min} до {self.max} символов."
            )

# Способ 2: Функция (используется как number_length(min=10, max=10))
def number_length(min: int, max: int, message: Optional[str] = None):
    def _number_length(form: FlaskForm, field: Field):
        if field.data is None:
            data_len = 0
        else:
            data_len = len(str(abs(field.data)))

        if data_len < min or data_len > max:
            raise ValidationError(
                message or f"Длина должна быть от {min} до {max} символов."
            )
    return _number_length