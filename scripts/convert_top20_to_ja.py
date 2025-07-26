import json

# 英語→日本語の対応表（必要に応じて追加）
name_map = {
    "Tokyo": "東京",
    "Osaka": "大阪",
    "Yokohama": "横浜",
    "Nagoya": "名古屋",
    "Sapporo": "札幌",
    "Fukuoka": "福岡",
    "Kyoto": "京都",
    "Kobe": "神戸",
    "Hiroshima": "広島",
    "Sendai": "仙台",
    "Chiba": "千葉",
    "Saitama": "埼玉",
    "Kawasaki": "川崎",
    "Niigata": "新潟",
    "Okayama": "岡山",
    "Kagoshima": "鹿児島",
    "Naha": "那覇",
    "Shizuoka": "静岡",
    "Kanazawa": "金沢",
    "Nagasaki": "長崎"
}

# 元のファイルを読み込み
with open("data/japan_city_weather.json", "r", encoding="utf-8") as f:
    cities = json.load(f)

# 日本語化された都市だけ抽出
converted = []
for city in cities:
    if city["name"] in name_map:
        converted.append({
            "name": name_map[city["name"]],
            "temp": city["temp"],
            "humidity": city["humidity"]
        })

# 保存
with open("data/japan_city_weather_limited_ja.json", "w", encoding="utf-8") as f:
    json.dump(converted, f, ensure_ascii=False, indent=2)

print("✅ 上位20都市の日本語変換ファイルを保存しました")
