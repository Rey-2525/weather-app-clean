import json
import os
import asyncio
import httpx
import time
from dotenv import load_dotenv

load_dotenv()
OWM_KEY = os.getenv("OPENWEATHER_API_KEY")

INPUT_FILE = "data/japan_cities_expanded.json"
OUTPUT_FILE = "data/japan_city_weather.json"

# ✅ OpenWeatherMapの1分あたり無料枠は通常60回（無料APIキー）
API_RATE_LIMIT = 60  # calls per minute

async def fetch_weather(client, city):
    name = city.get("name")
    lat = city.get("lat")
    lon = city.get("lon")

    if not name or lat is None or lon is None:
        return None

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=ja&appid={OWM_KEY}"

    try:
        res = await client.get(url, timeout=5)
        res.raise_for_status()
        data = res.json()
        print(f"✅ {name} 成功")
        return {
            "name": name,
            "temp": round(data["main"]["temp"]),
            "humidity": round(data["main"]["humidity"])
        }
    except httpx.HTTPStatusError as e:
        print(f"❌ {name} HTTPエラー: {e.response.status_code} {e.response.text}")
        return None
    except Exception as e:
        print(f"❌ {name} 例外: {e}")
        return None

async def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    cities = data.get("cities", [])

    results = []
    async with httpx.AsyncClient() as client:
        for i in range(0, len(cities), API_RATE_LIMIT):
            batch = cities[i:i + API_RATE_LIMIT]
            tasks = [fetch_weather(client, city) for city in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend([r for r in batch_results if r])

            # ✅ レートリミット対策のスリープ（60秒）
            if i + API_RATE_LIMIT < len(cities):
                print(f"⏳ {i+API_RATE_LIMIT}件処理完了。60秒待機中...")
                await asyncio.sleep(60)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"✅ 完了: {len(results)} 件 → {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())
