import unittest
import datetime
from person import Person


class TestPerson(unittest.TestCase):

    def setUp(self):
        self.person = Person("Ivan", 2000)

    def test_get_name(self):
        self.assertEqual(self.person.get_name(), "Ivan")

    def test_set_name(self):
        self.person.set_name("Alex")
        self.assertEqual(self.person.get_name(), "Alex")

    def test_get_address_default(self):
        self.assertEqual(self.person.get_address(), "")

    def test_set_address(self):
        self.person.set_address("Moscow")
        self.assertEqual(self.person.get_address(), "Moscow")

    def test_is_homeless_true(self):
        self.person.set_address("")
        self.assertTrue(self.person.is_homeless())

    def test_is_homeless_false(self):
        self.person.set_address("Moscow")
        self.assertFalse(self.person.is_homeless())

    def test_get_age(self):
        current_year = datetime.datetime.now().year
        expected_age = current_year - 2000
        self.assertEqual(self.person.get_age(), expected_age)


if __name__ == "__main__":
    unittest.main()
