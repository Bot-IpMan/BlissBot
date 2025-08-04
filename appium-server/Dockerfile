FROM node:18-alpine

# Встановлення системних залежностей
RUN apk add --no-cache \
    android-tools \
    openjdk11-jre \
    curl \
    bash

# Встановлення Appium та драйверів
RUN npm install -g appium@2.4.1
RUN appium driver install uiautomator2@2.34.0

# Перевірка встановлених драйверів
RUN appium driver list --installed

WORKDIR /opt/appium

# Копіювання конфігурації
COPY appium.conf.js .
COPY start.sh .
RUN chmod +x start.sh

# Створення необхідних директорій
RUN mkdir -p /opt/appium/logs /opt/appium/screenshots /opt/appium/apks

EXPOSE 4723

# Healthcheck для контейнера
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:4723/wd/hub/status || exit 1

ENTRYPOINT ["/opt/appium/start.sh"]
