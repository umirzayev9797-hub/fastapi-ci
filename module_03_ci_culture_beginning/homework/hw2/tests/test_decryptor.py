import unittest

from decrypt import decrypt


class TestDecryptor(unittest.TestCase):
    """Тесты функции decrypt"""

    def test_no_or_single_dots(self):
        """
        Случаи без удаления символов
        (нет двух точек подряд)
        """
        cases = {
            "абра-кадабра.": "абра-кадабра",
            ".": "",
        }

        for encrypted, expected in cases.items():
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

    def test_two_dots_remove_previous_symbol(self):
        """
        Ровно две точки подряд удаляют предыдущий символ
        """
        cases = {
            "абраа..-кадабра": "абра-кадабра",
            "1..2.3": "23",
        }

        for encrypted, expected in cases.items():
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

    def test_multiple_dot_sequences(self):
        """
        Сложные комбинации точек и символов
        """
        cases = {
            "абраа..-.кадабра": "абра-кадабра",
            "абра--..кадабра": "абра-кадабра",
            "абрау...-кадабра": "абра-кадабра",
            "абр......a.": "a",
        }

        for encrypted, expected in cases.items():
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

    def test_only_dots(self):
        """
        Строки, состоящие только из точек
        """
        cases = {
            "абра........": "",
            "1.......................": "",
        }

        for encrypted, expected in cases.items():
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

