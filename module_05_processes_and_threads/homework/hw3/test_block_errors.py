import unittest
from block_errors import BlockErrors

class BlockErrorsTests(unittest.TestCase):

    def test_ignore_error(self):
        # Пример 1: ошибка должна подавиться
        try:
            with BlockErrors({ZeroDivisionError, TypeError}):
                result = 1 / 0
        except:
            self.fail("ZeroDivisionError should be ignored but was raised")

    def test_propagate_unexpected_error(self):
        # Пример 2: TypeError не в allowed → должен всплыть
        with self.assertRaises(TypeError):
            with BlockErrors({ZeroDivisionError}):
                result = 1 / "0"

    def test_inner_error_propagates_but_outer_ignores(self):
        # Пример 3:
        # inner allowed={ZeroDivisionError} → TypeError не подавляем → вылетит
        # outer allowed={TypeError} → подавляем TypeError от inner
        try:
            with BlockErrors({TypeError}):
                with BlockErrors({ZeroDivisionError}):
                    result = 1 / "0"
                print("Inner block: completed")
        except:
            self.fail("Outer block should ignore TypeError but it propagated")

    def test_ignore_base_exception(self):
        # Пример 4: Exception — базовый класс для TypeError → подавляем
        try:
            with BlockErrors({Exception}):
                result = 1 / "0"
        except:
            self.fail("All Exception types should be ignored but was raised")

    def test_ignore_child_exception(self):
        # Доп. проверка: дочерний класс ZeroDivisionError от ArithmeticError должен подавиться
        try:
            with BlockErrors({ArithmeticError}):
                result = 10 / 0
        except:
            self.fail("Child of ArithmeticError should be ignored but was raised")

    def test_propagate_non_allowed_error(self):
        # KeyError не входит в allowed → должен всплыть
        with self.assertRaises(KeyError):
            with BlockErrors({TypeError}):
                {}["missing_key"]

    def test_nested_behavior(self):
        # Вложенность: inner allowed={ZeroDivisionError} подавляет 1/0
        # outer allowed={TypeError} подавляет только TypeError, но не мешает inner
        try:
            with BlockErrors({TypeError}):
                with BlockErrors({ZeroDivisionError}):
                    result = 1 / 0  # подавится inner
                result = 1 + 1  # обычный код работает
        except:
            self.fail("Nested blocks failed to ignore expected errors")


if __name__ == '__main__':
    unittest.main()
