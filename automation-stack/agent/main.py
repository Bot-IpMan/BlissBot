from fastapi import FastAPI
from langchain_community.chat_models import ChatOllama
from tools import click, type_text, wait, swipe, adb_shell, screenshot

app = FastAPI()
llm = ChatOllama(base_url="http://qwen:11434", model="qwen2.5-coder:7b-instruct")

@app.get("/health")
def health():
    return {"status": "ok"}

# 👉 Додайте реальні маршрути, що приймають завдання та запускають агента
