from fastapi import APIRouter, Request
import requests
from utils.config import GOOGLE_MAPS_API_KEY

router = APIRouter()

@router.post("/geocode")
async def geocode(request: Request):
    body = await request.json()
    city = body.get("city", "")

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": city,
        "language": "ja",
        "region": "jp",
        "key": GOOGLE_MAPS_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] == "OK" and data["results"]:
        location = data["results"][0]["geometry"]["location"]
        return {"lat": location["lat"], "lon": location["lng"]}
    else:
        return {"error": "都市が見つかりませんでした。"}