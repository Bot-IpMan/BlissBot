#!/bin/sh
set -e

echo "Запуск Appium сервера..."

# Перевірка доступності Android емулятора
if [ -n "$ANDROID_EMULATOR_HOST" ] && [ -n "$ANDROID_EMULATOR_PORT" ]; then
    echo "Спроба підключення до Android емулятора: $ANDROID_EMULATOR_HOST:$ANDROID_EMULATOR_PORT"
    
    # Спроба підключення через ADB (з таймаутом)
    timeout=30
    counter=0
    
    while [ $counter -lt $timeout ]; do
        if adb connect "$ANDROID_EMULATOR_HOST:$ANDROID_EMULATOR_PORT" 2>/dev/null; then
            echo "Успішно підключено до емулятора"
            break
        fi
        counter=$((counter + 1))
        echo "Очікування підключення до емулятора... ($counter/$timeout)"
        sleep 2
    done
    
    if [ $counter -eq $timeout ]; then
        echo "ПОПЕРЕДЖЕННЯ: Не вдалося підключитися до емулятора за $timeout секунд"
        echo "Appium сервер все одно запуститься, але автотести можуть не працювати"
    fi
    
    # Показати підключені пристрої
    echo "Підключені Android пристрої:"
    adb devices
else
    echo "ANDROID_EMULATOR_HOST або ANDROID_EMULATOR_PORT не встановлені"
    echo "Appium запуститься без автоматичного підключення до емулятора"
fi

# Запуск Appium сервера
echo "Запуск Appium на порт 4723..."
appium --config /opt/appium/appium.conf.js
