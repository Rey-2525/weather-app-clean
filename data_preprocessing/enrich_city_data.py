import json
import os

INPUT_FILE = os.path.join("data", "japan_cities_raw.json")
OUTPUT_FILE = os.path.join("data", "japan_cities_expanded.json")

def enrich_city_data():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    enriched = []

    for entry in raw_data:
        if entry.get("country") != "JP":
            continue  # 🇯🇵 日本の都市のみ対象

        name = entry.get("name")
        lat = entry.get("coord", {}).get("lat")
        lon = entry.get("coord", {}).get("lon")

        if not name or lat is None or lon is None:
            continue

        enriched.append({
            "name": name,
            "name_en": name,
            "pref": "不明",  # 都道府県名は不明なため仮で
            "lat": lat,
            "lon": lon
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"cities": enriched}, f, indent=2, ensure_ascii=False)

    print(f"✅ Done! {len(enriched)} 件の都市データを保存しました → {OUTPUT_FILE}")

if __name__ == "__main__":
    enrich_city_data()
