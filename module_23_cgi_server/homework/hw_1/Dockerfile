FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir gunicorn

COPY . .

# Запускаем gunicorn, указывая на объект app в файле routes
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "routes:app"]