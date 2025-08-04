from fastapi import FastAPI
from transformers import AutoTokenizer, AutoModelForCausalLM
from pydantic import BaseModel
import torch

app = FastAPI()

_tokenizer = None
_model = None


def load_model():
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        _tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-7B-Instruct")
        _model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-Coder-7B-Instruct")


class Prompt(BaseModel):
    prompt: str


@app.post("/generate")
async def generate(data: Prompt):
    load_model()
    inputs = _tokenizer(data.prompt, return_tensors="pt")
    outputs = _model.generate(**inputs, max_new_tokens=128)
    text = _tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"response": text}
