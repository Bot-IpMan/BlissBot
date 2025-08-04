FROM node:18-alpine

# Встановлення Android tools (ADB) та Java для UiAutomator2
RUN apk add --no-cache android-tools openjdk11-jre

# Встановлення Appium та UiAutomator2 драйвера
RUN npm install -g appium@next
RUN appium driver install uiautomator2

WORKDIR /opt/appium
COPY appium.conf.js .
COPY start.sh .
RUN chmod +x start.sh

# Створення директорій для логів та скріншотів
RUN mkdir -p /opt/appium/logs /opt/appium/screenshots /opt/appium/apks

EXPOSE 4723
ENTRYPOINT ["/opt/appium/start.sh"]
