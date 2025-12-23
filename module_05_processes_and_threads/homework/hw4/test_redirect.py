import unittest
import io
import sys
from redirect import Redirect


class RedirectManagerTests(unittest.TestCase):

    def test_redirect_stdout_and_stderr(self):
        mock_stdout = io.StringIO()
        mock_stderr = io.StringIO()

        # Оборачиваем в try-except, так как Redirect не должен глотать ошибки
        try:
            with Redirect(stdout=mock_stdout, stderr=mock_stderr):
                print("STDOUT CAPTURED")
                raise ValueError("STDERR CAPTURED")
        except ValueError:
            pass

        self.assertIn("STDOUT CAPTURED", mock_stdout.getvalue())
        self.assertIn("ValueError: STDERR CAPTURED", mock_stderr.getvalue())

    def test_redirect_stdout_only(self):
        mock_stdout = io.StringIO()
        with Redirect(stdout=mock_stdout):
            print("ONLY STDOUT")

        self.assertIn("ONLY STDOUT", mock_stdout.getvalue())

    def test_nested_contexts(self):
        outer_stdout = io.StringIO()
        inner_stdout = io.StringIO()

        with Redirect(stdout=outer_stdout):
            print("OUTER")
            with Redirect(stdout=inner_stdout):
                print("INNER")
            print("OUTER AGAIN")

        self.assertEqual(outer_stdout.getvalue().strip(), "OUTER\nOUTER AGAIN")
        self.assertEqual(inner_stdout.getvalue().strip(), "INNER")


if __name__ == '__main__':
    # Перенаправляем вывод тестов в файл, чтобы не смешивать с логикой stdout
    with open('test_results.txt', 'w') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.main(testRunner=runner)