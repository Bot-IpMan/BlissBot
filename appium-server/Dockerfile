# Використовуємо офіційний образ Appium
FROM appium/appium:v2.4.1-p0

# Встановлення додаткових інструментів
USER root
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Повертаємося до користувача appium
USER appium

# Встановлення UiAutomator2 драйвера (він може бути вже встановлений)
RUN appium driver list --installed || appium driver install uiautomator2 || echo "Драйвер вже встановлений"

WORKDIR /opt/appium

# Копіювання конфігурації
COPY --chown=appium:appium appium.conf.js .
COPY --chown=appium:appium start.sh .
RUN chmod +x start.sh

# Створення необхідних директорій
RUN mkdir -p /opt/appium/logs /opt/appium/screenshots /opt/appium/apks

EXPOSE 4723

# Healthcheck для контейнера
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:4723/wd/hub/status || exit 1

ENTRYPOINT ["/opt/appium/start.sh"]
