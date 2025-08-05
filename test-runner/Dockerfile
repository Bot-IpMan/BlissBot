FROM python:3.10-slim

# Встановлення системних залежностей
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Встановлення Python залежностей для Appium
RUN pip install --no-cache-dir \
    Appium-Python-Client==3.1.1 \
    selenium==4.15.0 \
    requests

# Копіювання тестового скрипта
COPY test_blissbot.py .
RUN chmod +x test_blissbot.py

# Створення директорій для скріншотів
RUN mkdir -p /app/screenshots

CMD ["python", "test_blissbot.py"]
