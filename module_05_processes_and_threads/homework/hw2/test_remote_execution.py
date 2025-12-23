import unittest
from remote_execution import app, execute_python_code, find_processes_using_port
import unittest
import time

class FlaskCodeExecutionTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_code_timeout(self):
        python_code = "import time; time.sleep(2); print('finished')"
        result = execute_python_code(python_code, 1)
        self.assertTrue(result["timeout"])
        self.assertEqual(result["error"], "Execution exceeded timeout limit")

    def test_invalid_form_data(self):
        response = self.client.post('/run_code', data={
            'code': "",
            'timeout': 40
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Invalid input", response.data)

    def test_unsafe_code_blocked(self):
        response = self.client.post('/run_code', data={
            'code': 'print("test"); echo "hack"',
            'timeout': 5
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Unsafe code detected", response.data)

    def test_valid_code_execution(self):
        response = self.client.post('/run_code', data={
            'code': "print('Hello Linux!')",
            'timeout': 5
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello Linux!", response.data)

    def test_lsof_pid_parsing(self):
        # Запускаем временный процесс, занимающий порт, имитировать сложно, но проверяем парсинг вывода lsof
        # Тут проверяем, что функция не падает и возвращает список
        process_ids = find_processes_using_port(5000)
        self.assertIsInstance(process_ids, list)

if __name__ == '__main__':
    unittest.main()

