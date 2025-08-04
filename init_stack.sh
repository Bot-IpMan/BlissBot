#!/bin/bash

echo "=== BlissBot Health Check ==="

# Перевірка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не встановлений"
    exit 1
else
    echo "✅ Docker встановлений: $(docker --version)"
fi

# Перевірка Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose не встановлений"
    exit 1
else
    echo "✅ Docker Compose доступний"
fi

# Перевірка доступної пам'яті
total_memory=$(free -g | awk '/^Mem:/{print $2}')
if [ "$total_memory" -lt 16 ]; then
    echo "⚠️  Попередження: Доступно ${total_memory}GB RAM. Рекомендується 16GB+ для моделі 7B"
else
    echo "✅ Достатньо пам'яті: ${total_memory}GB RAM"
fi

# Перевірка GPU
if command -v nvidia-smi &> /dev/null; then
    gpu_memory=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1)
    if [ "$gpu_memory" -gt 12000 ]; then
        echo "✅ GPU доступний з ${gpu_memory}MB пам'яті"
    else
        echo "⚠️  GPU доступний, але може бути недостатньо пам'яті (${gpu_memory}MB)"
    fi
else
    echo "⚠️  GPU не виявлений, буде використано CPU (повільно)"
fi

# Перевірка мережевого підключення до емулятора
if [ -n "$ANDROID_EMULATOR_HOST" ]; then
    if ping -c 1 "$ANDROID_EMULATOR_HOST" &> /dev/null; then
        echo "✅ Емулятор доступний за адресою $ANDROID_EMULATOR_HOST"
        
        # Перевірка ADB підключення
        if command -v adb &> /dev/null; then
            if adb connect "$ANDROID_EMULATOR_HOST:${ANDROID_EMULATOR_PORT:-5555}" &> /dev/null; then
                echo "✅ ADB підключення до емулятора успішне"
            else
                echo "⚠️  Не вдалося підключитися через ADB"
            fi
        else
            echo "⚠️  ADB не встановлений локально"
        fi
    else
        echo "❌ Емулятор недоступний за адресою $ANDROID_EMULATOR_HOST"
    fi
else
    echo "⚠️  ANDROID_EMULATOR_HOST не встановлений"
fi

# Перевірка портів
for port in 8000 4723; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null; then
        echo "⚠️  Порт $port вже зайнятий"
    else
        echo "✅ Порт $port вільний"
    fi
done

echo ""
echo "=== Рекомендації ==="
echo "1. Переконайтеся, що емулятор BlissOS запущений і доступний"
echo "2. Встановіть ANDROID_EMULATOR_HOST у .env файлі"
echo "3. При першому запуску дочекайтеся завантаження моделі (може зайняти 10-20 хвилин)"
echo "4. Використовуйте 'docker-compose up --build' для запуску"
