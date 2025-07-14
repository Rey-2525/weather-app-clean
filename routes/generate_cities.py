import os
import requests
import json
from dotenv import load_dotenv

# .env から API キーを読み込む
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# ✅ 日本語名 → ローマ字の辞書
CITY_NAME_MAP = {
    "札幌": "Sapporo",
    "仙台": "Sendai",
    "東京": "Tokyo",
    "名古屋": "Nagoya",
    "大阪": "Osaka",
    "広島": "Hiroshima",
    "福岡": "Fukuoka",
    "那覇": "Naha",
    "金沢": "Kanazawa",
    "松本": "Matsumoto",
    "熊谷": "Kumagaya",
    "軽井沢": "Karuizawa",
    "函館": "Hakodate",
    "高松": "Takamatsu",
    "鹿児島": "Kagoshima"
}

# 出力先
OUTPUT_FILE = "data/japan_cities.json"


def fetch_city_weather(japanese_name, roman_name):
    # Geocoding
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    geo_params = {
        "q": f"{roman_name},JP",
        "limit": 1,
        "appid": API_KEY
    }
    geo_res = requests.get(geo_url, params=geo_params)
    geo_data = geo_res.json()

    print(f"🌍 {japanese_name} のgeo_data: {geo_data}")  # ← 一時的にデバッグ

    if not geo_data:
        print(f"⚠️ {japanese_name} の緯度経度が見つかりません")
        return None

    try:
        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]
    except (KeyError, IndexError) as e:
        print(f"⚠️ {japanese_name} の座標抽出に失敗: {e}")
        return None


    # 天気情報取得
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    weather_params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ja"
    }
    weather_res = requests.get(weather_url, params=weather_params)
    if weather_res.status_code == 200:
        weather_data = weather_res.json()
        return {
            "name": japanese_name,
            "temp": round(weather_data["main"]["temp"]),
            "humidity": weather_data["main"]["humidity"]
        }
    else:
        print(f"⚠️ {japanese_name} の天気取得に失敗: {weather_res.status_code}")
        return None


def generate_city_data():
    result = []
    for jp_name, roman_name in CITY_NAME_MAP.items():
        info = fetch_city_weather(jp_name, roman_name)
        if info:
            result.append(info)

    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(result)} 都市のデータを {OUTPUT_FILE} に保存しました")


if __name__ == "__main__":
    generate_city_data()
