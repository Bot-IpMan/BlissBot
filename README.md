# BlissBot

Локальний стек для автоматизації Android, який поєднує штучний інтелект та керування мобільним інтерфейсом. Проєкт орієнтований на роботу з емулятором BlissOS 16.9.7 на Hyper‑V.

## Огляд

Стек складається з двох Docker‑контейнерів, що запускаються через `docker compose`:

- **qwen-agent** – FastAPI‑сервіс, який завантажує модель [`Qwen/Qwen2.5-Coder-7B-Instruct`](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct) і надає HTTP‑інтерфейс `/generate` для створення тексту або сценаріїв.
- **appium** – сервер [Appium](https://appium.io), через який агент взаємодіє з Android‑емулятором чи фізичним пристроєм.

Обидва контейнері звʼязуються між собою та спільними папками для логів, скріншотів та APK‑файлів.

## Вимоги

- встановлені Docker і Docker Compose;
- щонайменше 16 ГБ оперативної памʼяті для моделі 7B;
- Android‑емулятор, запущений на Hyper‑V з BlissOS 16.9.7 і доступний у мережі (наприклад, `192.168.1.10:5555`);
- доступ до Інтернету при першому старті для завантаження моделі.

## Структура проєкту

```
├── docker-compose.yml      # визначення сервісів
├── qwen-agent/             # код FastAPI‑агента
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── appium-server/          # конфігурація Appium
│   ├── Dockerfile
│   ├── appium.conf.js
│   └── start.sh
├── shared/                 # спільний обмін даними
├── logs/                   # журнали Appium
├── screenshots/            # скріншоти
└── apks/                   # APK для встановлення
```

## Запуск

1. Переконайтеся, що Android‑емулятор працює та доступний зсередини контейнера Appium (наприклад, виконайте `adb connect <IP>:5555` після запуску контейнера).
2. Запустіть стек:

This project provides a Docker Compose setup for a local server that ties together:

- **qwen-agent**: a FastAPI service powered by the `Qwen/Qwen2.5-Coder-7B-Instruct` model.
- **appium**: an Appium server used to drive Android emulators or devices.

The Android emulator should run on Hyper-V with BlissOS 16.9.7 and be reachable by the Appium server.

## Usage


```bash
docker compose up --build
```


Після успішного старту:

- **qwen-agent** доступний на `http://localhost:8000`;
- **appium** слухає `http://localhost:4723`.

## Перевірка роботи

### Qwen-agent

```bash
curl -X POST http://localhost:8000/generate \
     -H 'Content-Type: application/json' \
     -d '{"prompt": "print(1+1)"}'
```

У відповіді ви отримаєте текст, згенерований моделлю.

### Appium

```bash
curl http://localhost:4723/wd/hub/status
```

Якщо сервер працює, у відповіді буде `"status":0` та інформація про доступні драйвери.

## Спільні папки

- `shared/` – будь‑які файли для обміну між сервісами;
- `logs/` – журнали Appium;
- `screenshots/` – знімки екрана, зроблені під час тестів;
- `apks/` – APK, які встановлюються на пристрій.

Каталоги монтуються у контейнери й зберігаються після перезапуску.

## Зупинка й очищення

```bash
docker compose down
```

За потреби видаліть створені томи та образи:

```bash
docker compose down --volumes --rmi all
```

## Подальша робота

- інтегруйте додаткові маршрути у `qwen-agent` для складніших сценаріїв керування Appium;
- додайте автотести й CI/CD;
- адаптуйте конфігурацію Appium під конкретні пристрої та драйвери.

Ласкаво просимо до внеску та пропозицій!

=======
After the services start:

- Qwen agent listens on `http://localhost:8000`.
- Appium server listens on `http://localhost:4723`.

Shared folders (`shared`, `logs`, `screenshots`, `apks`) are mounted inside the containers for data exchange.
