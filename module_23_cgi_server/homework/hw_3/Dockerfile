FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Запускаем gunicorn с увеличенным тайм-аутом воркера
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "600", "app:app"]