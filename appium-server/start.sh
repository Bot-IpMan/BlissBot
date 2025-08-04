#!/bin/bash
set -e

echo "=== Запуск Appium сервера ==="

# Показати версію Appium та встановлені драйвери
echo "Версія Appium: $(appium --version)"
echo "Встановлені драйвери:"
appium driver list --installed

# Перевірка підключення до емулятора
if [ -n "$ANDROID_EMULATOR_HOST" ] && [ -n "$ANDROID_EMULATOR_PORT" ]; then
    echo "Спроба підключення до Android емулятора: $ANDROID_EMULATOR_HOST:$ANDROID_EMULATOR_PORT"
    
    # Спроба підключення через ADB з обмеженим таймаутом
    timeout=30
    counter=0
    connected=false
    
    while [ $counter -lt $timeout ]; do
        echo "Спроба підключення ADB... ($((counter + 1))/$timeout)"
        
        if timeout 5 adb connect "$ANDROID_EMULATOR_HOST:$ANDROID_EMULATOR_PORT" 2>/dev/null | grep -q "connected"; then
            echo "✅ Успішно підключено до емулятора"
            connected=true
            break
        fi
        
        counter=$((counter + 1))
        sleep 2
    done
    
    if [ "$connected" = false ]; then
        echo "⚠️ ПОПЕРЕДЖЕННЯ: Не вдалося підключитися до емулятора за $timeout секунд"
        echo "Appium сервер запуститься без підключення до пристрою"
    fi
    
    # Показати підключені пристрої
    echo "Підключені Android пристрої:"
    adb devices
else
    echo "⚠️ ANDROID_EMULATOR_HOST або ANDROID_EMULATOR_PORT не встановлені"
    echo "Встановіть змінні середовища для автоматичного підключення"
fi

echo ""
echo "🚀 Запуск Appium сервера на порт 4723..."
echo "Конфігурація: /opt/appium/appium.conf.js"

# Запуск Appium з додатковими параметрами
exec appium server \
    --config /opt/appium/appium.conf.js \
    --log-timestamp \
    --local-timezone
