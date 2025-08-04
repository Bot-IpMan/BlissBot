FROM node:18-alpine

# Встановлення системних залежностей
RUN apk add --no-cache \
    android-tools \
    openjdk11-jre \
    curl \
    bash \
    wget

# Встановлення Appium
RUN npm install -g appium@2.4.1

# Налаштування змінних середовища для пропуску завантажень
ENV APPIUM_SKIP_CHROMEDRIVER_INSTALL=1
ENV npm_config_timeout=300000
ENV npm_config_registry=https://registry.npmjs.org/

# Встановлення UiAutomator2 драйвера з розширеним таймаутом
RUN npm config set timeout 300000 && \
    npm config set registry https://registry.npmjs.org/ && \
    appium driver install uiautomator2 || \
    (echo "Спроба 2..." && sleep 5 && appium driver install uiautomator2) || \
    (echo "Спроба 3 з пропуском всіх завантажень..." && \
     APPIUM_SKIP_CHROMEDRIVER_INSTALL=1 \
     npm_config_timeout=600000 \
     appium driver install uiautomator2)

# Перевірка встановлених драйверів
RUN appium driver list --installed || echo "Драйвери не встановлені, але продовжуємо..."

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
