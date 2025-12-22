"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""
import sys
import os

# Этот блок программно добавляет папку hw1_3 в пути поиска,
# даже если настройки IDE сбиты.
current_dir = os.path.dirname(os.path.abspath(__file__)) # папка tests
parent_dir = os.path.dirname(current_dir)                # папка hw1_3
sys.path.append(parent_dir)


import unittest

from hw1_registration import app


class RegistrationTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

        self.valid_data = {
            "email": "test@mail.com",
            "phone": "9123456789",
            "name": "Ivan",
            "address": "Moscow",
            "index": "123456",
            "comment": "Test comment"
        }

    # ---------- email ----------

    def test_email_valid(self):
        response = self.client.post("/registration", data=self.valid_data)
        self.assertEqual(response.status_code, 200)

    def test_email_invalid(self):
        data = self.valid_data.copy()
        data["email"] = "not-email"

        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.get_data(as_text=True))

    # ---------- phone ----------

    def test_phone_valid(self):
        response = self.client.post("/registration", data=self.valid_data)
        self.assertEqual(response.status_code, 200)

    def test_phone_too_short(self):
        data = self.valid_data.copy()
        data["phone"] = "123"

        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("phone", response.get_data(as_text=True))

    def test_phone_negative(self):
        data = self.valid_data.copy()
        data["phone"] = "-9123456789"

        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 400)

    # ---------- name ----------

    def test_name_valid(self):
        response = self.client.post("/registration", data=self.valid_data)
        self.assertEqual(response.status_code, 200)

    def test_name_empty(self):
        data = self.valid_data.copy()
        data["name"] = ""

        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.get_data(as_text=True))

    # ---------- address ----------

    def test_address_empty(self):
        data = self.valid_data.copy()
        data["address"] = ""

        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("address", response.get_data(as_text=True))

    # ---------- index ----------

    def test_index_valid(self):
        response = self.client.post("/registration", data=self.valid_data)
        self.assertEqual(response.status_code, 200)

    def test_index_not_number(self):
        data = self.valid_data.copy()
        data["index"] = "abc"

        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("index", response.get_data(as_text=True))

    # ---------- comment ----------

    def test_comment_optional(self):
        data = self.valid_data.copy()
        data.pop("comment")

        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
