# ── Dockerfile ──
FROM python:3.11-slim AS agent

# оновимо pip — нові пакунки вимагають ≥24.3
RUN pip install --no-cache-dir --upgrade pip

# встановлюємо потрібні пакети
RUN pip install --no-cache-dir \
      langchain==0.2.0 \
      fastapi==0.111.0 \
      "uvicorn[standard]==0.29.0" \
      appium-python-client==5.1.2 \
      httpx==0.27.0

# щоб можна було запускати сервіс командою `uvicorn main:app`
WORKDIR /app
COPY ./agent /app
EXPOSE 11434
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "11434"]
