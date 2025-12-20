import unittest
from flask import json
from finance_app import app, storage


class TestFinanceApp(unittest.TestCase):
    """Тесты для приложения Учёт финансов"""

    @classmethod
    def setUpClass(cls):
        """Создаём тестовый клиент и изначальные данные"""
        app.testing = True
        cls.client = app.test_client()
        # Изначальные данные для всех тестов
        storage.clear()
        storage.update({
            "20251220": 100,
            "20251221": 200,
        })

    def test_add_endpoint_valid(self):
        """Проверка добавления новой записи с валидной датой"""
        response = self.client.post('/add/', data={'date': '20251222', 'sum': '150'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('20251222', storage)
        self.assertEqual(storage['20251222'], 150)

    def test_add_endpoint_invalid_date(self):
        """Проверка добавления с невалидной датой (формат должен быть YYYYMMDD)"""
        with self.assertRaises(Exception):
            self.client.post('/add/', data={'date': '20-12-2025', 'sum': '150'})

    def test_calculate_endpoint_total(self):
        """Проверка расчёта общего итога"""
        response = self.client.get('/calculate/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        expected_total = sum(storage.values())
        self.assertEqual(data['total'], expected_total)

    def test_calculate_endpoint_empty_storage(self):
        """Проверка расчёта, если storage пуст"""
        storage.clear()
        response = self.client.get('/calculate/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['total'], 0)

    def test_add_endpoint_updates_existing_date(self):
        """Добавление суммы к уже существующей дате"""
        storage.clear()
        storage.update({"20251220": 100})
        response = self.client.post('/add/', data={'date': '20251220', 'sum': '50'})
        self.assertEqual(storage['20251220'], 150)

    def test_calculate_endpoint_with_range(self):
        """Проверка /calculate/ с диапазоном дат (если поддерживается)"""
        storage.clear()
        storage.update({"20251220": 100, "20251221": 200, "20251222": 300})
        response = self.client.get('/calculate/', query_string={'from': '20251221', 'to': '20251222'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['total'], 200 + 300)


if __name__ == '__main__':
    unittest.main()
