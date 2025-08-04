from fastapi import FastAPI, HTTPException
from transformers import AutoTokenizer, AutoModelForCausalLM
from pydantic import BaseModel
import torch
import logging
import os

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Qwen Agent", description="AI-powered Android automation agent")

# Глобальні змінні для моделі
_tokenizer = None
_model = None
_model_loaded = False

class Prompt(BaseModel):
    prompt: str
    max_tokens: int = 128
    temperature: float = 0.7

@app.on_event("startup")
async def startup_event():
    """Завантаження моделі при старті сервера"""
    global _tokenizer, _model, _model_loaded
    try:
        logger.info("Завантаження моделі Qwen2.5-Coder-7B-Instruct...")
        
        # Перевірка доступності GPU
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Використовується пристрій: {device}")
        
        # Завантаження токенізатора
        _tokenizer = AutoTokenizer.from_pretrained(
            "Qwen/Qwen2.5-Coder-7B-Instruct",
            trust_remote_code=True
        )
        
        # Завантаження моделі з оптимізацією для CPU якщо GPU недоступний
        if device == "cpu":
            logger.warning("GPU недоступний, використовується CPU (буде повільно)")
            _model = AutoModelForCausalLM.from_pretrained(
                "Qwen/Qwen2.5-Coder-7B-Instruct",
                torch_dtype=torch.float32,  # Для CPU
                trust_remote_code=True
            )
        else:
            _model = AutoModelForCausalLM.from_pretrained(
                "Qwen/Qwen2.5-Coder-7B-Instruct",
                torch_dtype=torch.float16,  # Для GPU
                device_map="auto",
                trust_remote_code=True
            )
        
        _model_loaded = True
        logger.info("Модель успішно завантажена!")
        
    except Exception as e:
        logger.error(f"Помилка завантаження моделі: {str(e)}")
        _model_loaded = False

@app.get("/")
async def root():
    return {
        "message": "Qwen Agent is running",
        "model_loaded": _model_loaded,
        "gpu_available": torch.cuda.is_available()
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if _model_loaded else "model_not_loaded",
        "model_loaded": _model_loaded
    }

@app.post("/generate")
async def generate(data: Prompt):
    if not _model_loaded:
        raise HTTPException(
            status_code=503, 
            detail="Модель не завантажена. Перевірте логи сервера."
        )
    
    try:
        # Підготовка промпту для чат-моделі
        messages = [
            {"role": "user", "content": data.prompt}
        ]
        
        # Застосування чат-шаблону
        text = _tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        # Токенізація
        inputs = _tokenizer(text, return_tensors="pt")
        
        # Генерація з покращеними параметрами
        with torch.no_grad():
            outputs = _model.generate(
                **inputs,
                max_new_tokens=data.max_tokens,
                temperature=data.temperature,
                do_sample=True,
                pad_token_id=_tokenizer.eos_token_id,
                eos_token_id=_tokenizer.eos_token_id
            )
        
        # Декодування тільки нових токенів
        new_tokens = outputs[0][inputs['input_ids'].shape[1]:]
        response = _tokenizer.decode(new_tokens, skip_special_tokens=True)
        
        return {
            "response": response,
            "prompt_length": len(data.prompt),
            "response_length": len(response)
        }
        
    except Exception as e:
        logger.error(f"Помилка генерації: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Помилка генерації: {str(e)}")

@app.post("/appium-command")
async def execute_appium_command(command_data: dict):
    """Endpoint для виконання команд Appium через AI-асистента"""
    # Тут можна додати логіку для генерації та виконання Appium команд
    # На основі природномовних запитів
    pass
