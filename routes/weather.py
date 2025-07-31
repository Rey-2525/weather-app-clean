from fastapi import APIRouter, HTTPException
import requests
from utils.config import OPENWEATHER_API_KEY
from datetime import datetime, timedelta, timezone
import pytz

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
    try:
        url = f"https://api.openweathermap.org/data/3.0/onecall"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
            "exclude": "minutely,daily,alerts",
        }
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()

        print(f"緯度経度: {lat}, {lon}")
        print("取得したデータ keys:", data.keys())

        hourly = data.get("hourly", [])
        print("hourly の件数:", len(hourly))

        # 現在の日本時間（UTC+9）
        jst = pytz.timezone("Asia/Tokyo")
        now_jst = datetime.now(jst)
        now_timestamp = int(now_jst.timestamp())

        forecast = []
        future_hourly = [entry for entry in hourly if entry["dt"] > now_timestamp]
        # 3時間ごとにデータ抽出（0, 3, 6, 9番目）
        for i in range(0, min(12, len(future_hourly)), 3):  # 安全のため最大12件まで
            entry = future_hourly[i]
            dt_jst = datetime.fromtimestamp(entry["dt"], jst)
            forecast.append({
                "time": dt_jst.strftime("%Y-%m-%d %H:%M:%S"),
                "pop": round(entry.get("pop", 0) * 100)
            })
            if len(forecast) >= 4:
                break

        return {"forecast": forecast}

    except Exception as e:
        print("❌ エラー:", e)
        raise HTTPException(status_code=500, detail=f"降水確率の取得に失敗しました: {str(e)}")

