print("✅ explanation router loaded")
from fastapi import APIRouter, Request
from utils.openai_client import generate_weather_explanation, generate_clothing_advice

router = APIRouter()

@router.post("/explanation")
async def explanation(request: Request):
    data = await request.json()
    result = await generate_weather_explanation(data)
    return {"explanation": result}

@router.post("/clothing_advice")
async def clothing_advice(request: Request):
    data = await request.json()
    result = await generate_clothing_advice(data)
    return {"advice": result}