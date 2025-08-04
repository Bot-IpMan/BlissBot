FROM node:18-alpine

# Встановлення системних залежностей
RUN apk add --no-cache \
    android-tools \
    openjdk11-jre \
    curl \
    bash

# Встановлення Appium
RUN npm install -g appium@2.4.1

# Встановлення UiAutomator2 драйвера з пропуском Chromedriver
ENV APPIUM_SKIP_CHROMEDRIVER_INSTALL=1
RUN appium driver install uiautomator2

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
