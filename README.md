# BlissBot

This project provides a Docker Compose setup for a local server that ties together:

- **qwen-agent**: a FastAPI service powered by the `Qwen/Qwen2.5-Coder-7B-Instruct` model.
- **appium**: an Appium server used to drive Android emulators or devices.

The Android emulator should run on Hyper-V with BlissOS 16.9.7 and be reachable by the Appium server.

## Usage

```bash
docker compose up --build
```

After the services start:

- Qwen agent listens on `http://localhost:8000`.
- Appium server listens on `http://localhost:4723`.

Shared folders (`shared`, `logs`, `screenshots`, `apks`) are mounted inside the containers for data exchange.
