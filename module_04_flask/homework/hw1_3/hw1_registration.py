"""
В эндпоинт /registration добавьте все валидаторы, о которых говорилось в последнем видео:

1) email (текст, обязательно для заполнения, валидация формата);
2) phone (число, обязательно для заполнения, длина — десять символов, только положительные числа);
3) name (текст, обязательно для заполнения);
4) address (текст, обязательно для заполнения);
5) index (только числа, обязательно для заполнения);
6) comment (текст, необязательно для заполнения).
"""

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional
from hw2_validators import number_length, NumberLength

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"


class RegistrationForm(FlaskForm):
    email = StringField(
        validators=[
            DataRequired(message="Email обязателен"),
            Email(message="Некорректный формат email")
        ]
    )

    phone = IntegerField(
        validators=[
            DataRequired(message="Телефон обязателен"),
            NumberRange(min=0, message="Телефон должен быть положительным числом"),
            NumberLength(10, 10, message="Телефон должен содержать 10 цифр")
        ]
    )

    name = StringField(
        validators=[
            DataRequired(message="Имя обязательно")
        ]
    )

    address = StringField(
        validators=[
            DataRequired(message="Адрес обязателен")
        ]
    )

    index = IntegerField(
        validators=[
            DataRequired(message="Индекс обязателен"),
            NumberRange(min=0, message="Индекс должен быть числом")
        ]
    )

    comment = StringField(
        validators=[
            Optional()
        ]
    )


@app.route("/registration", methods=["POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data
        phone = form.phone.data

        return f"Successfully registered user {email} with phone +7{phone}"

    return f"Invalid input, {form.errors}", 400


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True, host = "0.0.0.0")

