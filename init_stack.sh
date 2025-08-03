#!/bin/bash

# Створення основних файлів і директорій
touch docker-compose.yml
touch README.md

# Створення директорії qwen-agent та її файлів
mkdir -p qwen-agent
touch qwen-agent/Dockerfile
touch qwen-agent/requirements.txt
touch qwen-agent/main.py

# Створення директорії appium-server та її файлів
mkdir -p appium-server
touch appium-server/Dockerfile
touch appium-server/appium.conf.js
touch appium-server/start.sh

# Створення спільних папок для даних, скріншотів, логів і APK
mkdir -p shared
mkdir -p screenshots
mkdir -p logs
mkdir -p apks
