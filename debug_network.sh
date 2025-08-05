#!/bin/bash

echo "🔍 Діагностика мережевого підключення BlissBot"
echo "=" * 50

# Перевірка з хост-машини
echo "1. Перевірка з хост-машини:"
ping -c 3 192.168.1.218 2>/dev/null && echo "✅ Емулятор доступний з хосту" || echo "❌ Емулятор недоступний з хосту"

# Перевірка з контейнера Appium
echo -e "\n2. Перевірка з контейнера Appium:"
docker compose exec appium ping -c 3 192.168.1.218 2>/dev/null && echo "✅ Емулятор доступний з Appium" || echo "❌ Емулятор недоступний з Appium"

# Перевірка портів
echo -e "\n3. Перевірка портів:"
if command -v nmap >/dev/null 2>&1; then
    nmap -p 5555 192.168.1.218 2>/dev/null | grep -q "open" && echo "✅ Порт 5555 відкритий" || echo "❌ Порт 5555 закритий"
else
    echo "⚠️ nmap не встановлений, пропуск перевірки портів"
fi

# Перевірка ADB
echo -e "\n4. Перевірка ADB:"
if command -v adb >/dev/null 2>&1; then
    adb connect 192.168.1.218:5555 >/dev/null 2>&1
    adb devices | grep -q "192.168.1.218:5555" && echo "✅ ADB підключення працює" || echo "❌ ADB підключення не працює"
else
    echo "⚠️ ADB не встановлений"
fi

# Перевірка Docker мережі
echo -e "\n5. Перевірка Docker мережі:"
docker network ls | grep blissbot && echo "✅ Docker мережа створена" || echo "❌ Проблема з Docker мережею"

# Рекомендації
echo -e "\n💡 Рекомендації:"
echo "- Переконайтеся, що BlissOS емулятор запущений"
echo "- Увімкніть Developer Options в BlissOS"
echo "- Увімкніть USB Debugging"
echo "- Перевірте налаштування мережі Hyper-V"
echo "- Спробуйте перезапустити Docker Compose"

# Альтернативні IP адреси для перевірки
echo -e "\n🔄 Альтернативні варіанти IP:"
echo "- Якщо 192.168.1.218 не працює, спробуйте:"
echo "  - 10.0.2.2 (стандартний для емуляторів)"
echo "  - 192.168.1.X (IP в локальній мережі)"
echo "  - host.docker.internal (для Docker Desktop)"