FROM python:3.9-slim

WORKDIR /app

# 1. Копируем зависимости отдельно для кэша
COPY requirements.txt .

# 2. Объединяем установку и чистку (минимизируем слои)
RUN pip install --no-cache-dir -r requirements.txt

# 3. Копируем код (самый меняющийся слой - в конце)
COPY . .

# 4. Запуск массивом
ENTRYPOINT ["python", "app.py"]
