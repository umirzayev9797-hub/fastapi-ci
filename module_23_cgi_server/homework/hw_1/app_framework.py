import json
import re


class WSGIApp:
    def __init__(self):
        self.routes = []

    def route(self, path):
        """Декоратор для регистрации путей."""

        def wrapper(handler):
            # Заменяем <name> на именованную группу регулярного выражения
            regex_path = re.sub(r'<(\w+)>', r'(?P<\1>[^/]+)', path)
            # Добавляем якоря начала и конца строки
            self.routes.append((re.compile(f'^{regex_path}$'), handler))
            return handler

        return wrapper

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '/')

        # Ищем подходящий роут
        for regex, handler in self.routes:
            match = regex.match(path)
            if match:
                # Вызываем функцию, передавая аргументы из URL (например, name)
                response_data = handler(**match.groupdict())

                status = '200 OK'
                headers = [('Content-Type', 'application/json; charset=utf-8')]
                start_response(status, headers)
                return [response_data.encode('utf-8')]

        # Если ничего не нашли — 404
        status = '404 NOT FOUND'
        headers = [('Content-Type', 'application/json; charset=utf-8')]
        start_response(status, headers)
        return [json.dumps({"error": "Not Found"}, indent=4).encode('utf-8')]