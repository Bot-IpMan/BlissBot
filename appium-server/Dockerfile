FROM node:18-alpine

RUN npm install -g appium@next

WORKDIR /opt/appium
COPY appium.conf.js .
COPY start.sh .
RUN chmod +x start.sh

EXPOSE 4723
ENTRYPOINT ["/opt/appium/start.sh"]
