from fastapi import APIRouter, HTTPException
import requests
from utils.config import OPENWEATHER_API_KEY

router = APIRouter()

@router.get("/weather")
def get_weather(lat: float = 35.6895, lon: float = 139.6917):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "ja"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return {
            "location": data.get("name", "不明"),
            "weather": data["weather"][0]["description"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "icon": data["weather"][0]["icon"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"天気情報の取得に失敗しました: {str(e)}")


@router.get("/weather-forecast")
def get_forecast(lat: float = 35.6895, lon: float = 139.6917):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        forecast = []
        for entry in data.get("list", [])[:4]:  # 3時間ごと × 4件 = 12時間分
            forecast.append({
                "time": entry.get("dt_txt", "不明な時刻"),
                "pop": round(entry.get("pop", 0) * 100)  # 降水確率（%に変換）
            })

        return {"forecast": forecast}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"降水確率の取得に失敗しました: {str(e)}")

