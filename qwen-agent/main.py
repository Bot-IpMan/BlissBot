from fastapi import FastAPI, HTTPException
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from pydantic import BaseModel
import torch
import logging
import os
import gc

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Qwen Agent", description="AI-powered Android automation agent")

# Глобальні змінні для моделі
_model_pipeline = None
_model_loaded = False

# Використовуємо модель Qwen2.5-Coder-7B-Instruct.
# Шлях до моделі можна задати через змінну оточення MODEL_PATH.
# За замовчуванням використовується репозиторій з HuggingFace.
MODEL_NAME = os.getenv("MODEL_PATH", "Qwen/Qwen2.5-Coder-7B-Instruct")

class Prompt(BaseModel):
    prompt: str
    max_tokens: int = 128
    temperature: float = 0.7

class AppiumCommand(BaseModel):
    instruction: str

@app.on_event("startup")
async def startup_event():
    """Завантаження моделі при старті сервера"""
    global _model_pipeline, _model_loaded
    try:
        logger.info(f"Завантаження моделі {MODEL_NAME}...")
        
        # Перевірка доступності GPU
        device = 0 if torch.cuda.is_available() else -1
        device_name = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Використовується пристрій: {device_name}")
        
        # Використовуємо pipeline для спрощення
        _model_pipeline = pipeline(
            "text-generation",
            model=MODEL_NAME,
            device=device,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            trust_remote_code=True,
            model_kwargs={
                "low_cpu_mem_usage": True,
                "use_cache": True
            }
        )
        
        _model_loaded = True
        logger.info("Модель успішно завантажена!")
        
        # Очищуємо пам'ять
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()
        
    except Exception as e:
        logger.error(f"Помилка завантаження моделі: {str(e)}")
        _model_loaded = False

@app.get("/")
async def root():
    return {
        "message": "Qwen Agent is running",
        "model": MODEL_NAME,
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
        # Генерація тексту через pipeline
        result = _model_pipeline(
            data.prompt,
            max_new_tokens=data.max_tokens,
            temperature=data.temperature,
            do_sample=True,
            return_full_text=False
        )
        
        response_text = result[0]['generated_text'] if result else ""
        
        return {
            "response": response_text,
            "prompt_length": len(data.prompt),
            "response_length": len(response_text)
        }
        
    except Exception as e:
        logger.error(f"Помилка генерації: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Помилка генерації: {str(e)}")

@app.post("/appium-command")
async def execute_appium_command(command_data: AppiumCommand):
    """Endpoint для виконання команд Appium через AI-асистента"""
    if not _model_loaded:
        raise HTTPException(
            status_code=503, 
            detail="Модель не завантажена."
        )
    
    try:
        # Створюємо промпт для генерації Appium коду
        system_prompt = """Ти - експерт з автоматизації Android через Appium. 
Створи Python код з використанням Appium WebDriver для виконання наступної інструкції.
Код повинен бути готовим до виконання та включати необхідні imports.
Використовуй capabilities для Android і UiAutomator2.

Інструкція: """
        
        full_prompt = system_prompt + command_data.instruction
        
        # Генеруємо код
        result = _model_pipeline(
            full_prompt,
            max_new_tokens=256,
            temperature=0.3,  # Нижча температура для більш точного коду
            do_sample=True,
            return_full_text=False
        )
        
        generated_code = result[0]['generated_text'] if result else ""
        
        return {
            "instruction": command_data.instruction,
            "generated_code": generated_code,
            "status": "code_generated"
        }
        
    except Exception as e:
        logger.error(f"Помилка генерації Appium коду: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Помилка генерації коду: {str(e)}"
        )
