#!/usr/bin/env bash
# Створює директорії та файли для LLM-агента + Appium стека
# Використання: ./init_stack.sh [назва_проєкту]  (за замовч. automation-stack)

set -euo pipefail
PROJECT_DIR="${1:-automation-stack}"

echo "[+] Creating project in $PROJECT_DIR …"
mkdir -p "$PROJECT_DIR"/{agent,ollama}                                   # каталоги

###############################################################################
# docker-compose.yml
###############################################################################
cat <<'EOF' > "$PROJECT_DIR/docker-compose.yml"
version: "3.9"
services:
  qwen:
    image: ollama/ollama:latest
    volumes:
      - ./ollama:/root/.ollama
    environment:
      - OLLAMA_MODELS=qwen2.5-coder:7b-instruct-q4_0
      - OLLAMA_MAX_CONTEXT=32768
    deploy:
      resources:
        reservations:
          devices: [{ capabilities: [gpu] }]
    ports: [ "11434:11434" ]

  agent:
    build: ./agent
    depends_on: [qwen]
    environment:
      - OLLAMA_BASE=http://qwen:11434
      - APPIUM_SERVER=http://appium:4723/wd/hub
      - ADB_HOST=blissvm
      - ADB_PORT=5555
    volumes:
      - ./agent/logs:/logs
    ports: [ "8000:8000" ]

  appium:
    image: appium/appium:latest
    ports: [ "4723:4723" ]
    command: >
      appium --use-plugins=element-wait
             --default-capabilities='{"newCommandTimeout":300}'

networks:
  default:
    name: automation-net
EOF

###############################################################################
# agent/Dockerfile
###############################################################################
cat <<'EOF' > "$PROJECT_DIR/agent/Dockerfile"
FROM python:3.11-slim
RUN pip install --no-cache-dir langchain==0.2.0 \
                               fastapi==0.111.0 \
                               uvicorn[standard]==0.30.0 \
                               appium-python-client==3.3.0 \
                               httpx==0.27.0
COPY . /app
WORKDIR /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

###############################################################################
# agent/main.py  – FastAPI + LangChain wrapper
###############################################################################
cat <<'EOF' > "$PROJECT_DIR/agent/main.py"
from fastapi import FastAPI
from langchain_community.chat_models import ChatOllama
from tools import click, type_text, wait, swipe, adb_shell, screenshot

app = FastAPI()
llm = ChatOllama(base_url="http://qwen:11434", model="qwen2.5-coder:7b-instruct")

@app.get("/health")
def health():
    return {"status": "ok"}

# 👉 Додайте реальні маршрути, що приймають завдання та запускають агента
EOF

###############################################################################
# agent/tools.py – шаблон функцій-інструментів
###############################################################################
cat <<'EOF' > "$PROJECT_DIR/agent/tools.py"
import httpx, os, base64, pathlib

APPIUM = os.getenv("APPIUM_SERVER", "http://appium:4723/wd/hub")
ADB_HOST = os.getenv("ADB_HOST", "blissvm")
ADB_PORT = os.getenv("ADB_PORT", "5555")

def _post(url, data=None):
    return httpx.post(url, json=data).json()

def click(selector):
    return _post(f"{APPIUM}/click", {"selector": selector})

def type_text(text, selector):
    return _post(f"{APPIUM}/type", {"selector": selector, "text": text})

def wait(selector, timeout=10):
    return _post(f"{APPIUM}/wait", {"selector": selector, "timeout": timeout})

def swipe(start, end, duration_ms=500):
    return _post(f"{APPIUM}/swipe", {"start": start, "end": end, "duration": duration_ms})

def adb_shell(cmd):
    return httpx.get(f"http://{ADB_HOST}:{ADB_PORT}/shell", params={"cmd": cmd}).text

def screenshot():
    raw = httpx.get(f"{APPIUM}/screenshot").text
    path = pathlib.Path("/logs") / "shot.png"
    path.write_bytes(base64.b64decode(raw))
    return str(path)
EOF

chmod +x "$PROJECT_DIR"/init_stack.sh
echo "[✓] Done!  Перейдіть у $PROJECT_DIR та запускайте:  docker compose up -d"
