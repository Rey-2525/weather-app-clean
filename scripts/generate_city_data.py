import requests
import json
import time
from pathlib import Path
from dotenv import load_dotenv
import os

# .env から API キーを読み込む
load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# 都市名リスト（必要に応じて増やす）
city_list = [
    "札幌", "仙台", "東京", "横浜", "名古屋", "京都", "大阪", "神戸", "広島", "高松",
    "松山", "福岡", "熊本", "那覇"
]

# 出力ファイルのパス
output_path = Path("data/japan_cities_expanded.json")

# 都市ごとのデータを保存するリスト
city_data = []

# 都市ごとにAPIで取得
for city in city_list:
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city},Japan&key={API_KEY}"
    try:
        response = requests.get(url)
        result = response.json()

        if result["status"] == "OK":
            info = result["results"][0]
            lat = info["geometry"]["location"]["lat"]
            lon = info["geometry"]["location"]["lng"]

            # 都道府県名を住所コンポーネントから取得
            pref_name = None
            for comp in info["address_components"]:
                if "administrative_area_level_1" in comp["types"]:
                    pref_name = comp["long_name"]
                    break

            city_data.append({
                "city": city,
                "lat": lat,
                "lon": lon,
                "pref": pref_name or ""
            })
            print(f"✅ {city}: {lat}, {lon}, {pref_name}")
        else:
            print(f"❌ {city}: API Error - {result['status']}")

        time.sleep(0.5)  # Google APIのレート制限対策

    except Exception as e:
        print(f"❌ {city}: Exception occurred - {e}")

# 保存
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(city_data, f, ensure_ascii=False, indent=2)

print(f"\n🎉 {len(city_data)} 件の都市データを保存しました → {output_path}")
