FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir gunicorn

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "routes:app"]