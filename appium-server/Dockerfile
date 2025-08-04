# Варіант 2: Простіший підхід без створення користувача
FROM node:18-slim

# Встановлення системних залежностей
RUN apt-get update && apt-get install -y \
    curl \
    netcat-traditional \
    openjdk-11-jdk \
    && rm -rf /var/lib/apt/lists/*

# Встановлення Appium та драйвера
RUN npm install -g appium@2.4.1 && \
    appium driver install uiautomator2

WORKDIR /opt/appium

# Створення необхідних директорій
RUN mkdir -p logs screenshots apks

# Копіювання конфігурації
COPY appium.conf.js .
COPY start.sh .
RUN chmod +x start.sh

EXPOSE 4723

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:4723/wd/hub/status || exit 1

ENTRYPOINT ["/opt/appium/start.sh"]
