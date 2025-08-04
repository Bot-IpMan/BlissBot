#!/bin/bash
set -e

echo "=== Запуск Appium сервера ==="

# Показати версію Appium та встановлені драйвери
echo "Версія Appium: $(appium --version)"
echo "Встановлені драйвери:"
appium driver list --installed 2>/dev/null || echo "Не вдалося отримати список драйверів"

# Перевірка підключення до емулятора (опціонально)
if [ -n "$ANDROID_EMULATOR_HOST" ] && [ -n "$ANDROID_EMULATOR_PORT" ]; then
    echo "Перевірка доступності емулятора: $ANDROID_EMULATOR_HOST:$ANDROID_EMULATOR_PORT"
    
    # Простіша перевірка доступності без ADB підключення
    if timeout 5 nc -z "$ANDROID_EMULATOR_HOST" "$ANDROID_EMULATOR_PORT" 2>/dev/null; then
        echo "✅ Емулятор доступний за адресою $ANDROID_EMULATOR_HOST:$ANDROID_EMULATOR_PORT"
    else
        echo "⚠️ Емулятор може бути недоступний"
    fi
else
    echo "💡 Для автоматичної перевірки емулятора встановіть ANDROID_EMULATOR_HOST та ANDROID_EMULATOR_PORT"
fi

echo ""
echo "🚀 Запуск Appium сервера на порт 4723..."

# Запуск Appium сервера
exec appium server \
    --address 0.0.0.0 \
    --port 4723 \
    --log-level info \
    --log-timestamp \
    --local-timezone \
    --allow-insecure adb_shell \
    --relaxed-security
