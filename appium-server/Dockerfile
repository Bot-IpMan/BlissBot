# Варіант 1: Використання офіційного базового образу Node.js
FROM node:18-slim

# Встановлення системних залежностей
RUN apt-get update && apt-get install -y \
    curl \
    netcat-traditional \
    openjdk-11-jdk \
    && rm -rf /var/lib/apt/lists/*

# Встановлення Appium глобально
RUN npm install -g appium@2.4.1

# Встановлення UiAutomator2 драйвера
RUN appium driver install uiautomator2

# Створення користувача appium
RUN useradd -m -u 1000 appium

# Створення робочих директорій
RUN mkdir -p /opt/appium/logs /opt/appium/screenshots /opt/appium/apks
RUN chown -R appium:appium /opt/appium

WORKDIR /opt/appium

# Копіювання конфігурації
COPY --chown=appium:appium appium.conf.js .
COPY --chown=appium:appium start.sh .
RUN chmod +x start.sh

# Перемикання на користувача appium
USER appium

EXPOSE 4723

# Healthcheck для контейнера
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:4723/wd/hub/status || exit 1

ENTRYPOINT ["/opt/appium/start.sh"]
