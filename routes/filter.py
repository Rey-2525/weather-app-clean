# routes/filter.py
from fastapi import APIRouter
from pydantic import BaseModel
import json
from pathlib import Path

router = APIRouter()

# ✅ ① 入力用のモデルを定義
class FilterRequest(BaseModel):
    keyword: str

def load_city_data():
        json_path = Path("data/japan_cities.json")
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)

city_data = load_city_data()

# ✅ ② request: Request → request: FilterRequest に変更
@router.post("/filter")
async def filter_location(request: FilterRequest):
    keyword = request.keyword


    if "涼" in keyword or "寒" in keyword:
        result = [c["name"] for c in city_data if c["temp"] <= 25 and c["humidity"] <= 60]
    elif "暖" in keyword or "暑" in keyword or "あたた" in keyword:
        result = [c["name"] for c in city_data if c["temp"] >= 28 and c["humidity"] >= 70]
    else:
        result = ["条件に合う都市が見つかりませんでした。"]

    return {"cities": result}
