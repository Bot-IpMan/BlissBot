FROM python:3.10-slim

# Встановлення системних залежностей
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копіювання та встановлення Python залежностей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Створення директорії для shared файлів
RUN mkdir -p /app/shared

EXPOSE 8000

# Збільшуємо таймаут для завантаження моделі
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "300"]
