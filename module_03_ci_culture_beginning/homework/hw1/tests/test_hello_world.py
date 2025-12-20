import unittest
from freezegun import freeze_time

from hello_word_with_day import app, GREETINGS


def extract_greeting(text: str) -> str:
    """
    Извлекает приветствие с днём недели из ответа сервера.
    Используется для проверки корректности дня недели.
    """
    for greeting in GREETINGS:
        if greeting in text:
            return greeting
    return ""


class TestHelloWorld(unittest.TestCase):
    """Тесты эндпоинта /hello-world/<name>"""

    @classmethod
    def setUpClass(cls):
        """Создание тестового клиента Flask один раз для всех тестов"""
        app.testing = True
        cls.client = app.test_client()

    def check_weekday(self, frozen_date: str, expected_greeting: str):
        """
        Универсальная проверка:
        для фиксированной даты должен возвращаться корректный день недели
        """
        with freeze_time(frozen_date):
            response = self.client.get('/hello-world/Иван')
            self.assertEqual(response.status_code, 200)

            text = response.data.decode('utf-8')
            greeting = extract_greeting(text)

            self.assertEqual(greeting, expected_greeting)

    def test_correct_greeting_for_all_weekdays(self):
        """
        Приветствие должно соответствовать дню недели.
        Проверяются все 7 дней.
        """
        test_cases = {
            "2024-01-01": "Хорошего понедельника",
            "2024-01-02": "Хорошего вторника",
            "2024-01-03": "Хорошей среды",
            "2024-01-04": "Хорошего четверга",
            "2024-01-05": "Хорошей пятницы",
            "2024-01-06": "Хорошей субботы",
            "2024-01-07": "Хорошего воскресенья",
        }

        for date, greeting in test_cases.items():
            self.check_weekday(date, greeting)

    def test_username_does_not_affect_weekday(self):
        """
        Если в имени пользователя указано пожелание дня недели,
        оно не должно влиять на определение текущего дня.
        """
        with freeze_time("2024-01-01"):  # понедельник
            response = self.client.get('/hello-world/Хорошей среды')
            self.assertEqual(response.status_code, 200)

            text = response.data.decode('utf-8')
            greeting = extract_greeting(text)

            self.assertEqual(greeting, "Хорошего понедельника")


if __name__ == '__main__':
    unittest.main()
