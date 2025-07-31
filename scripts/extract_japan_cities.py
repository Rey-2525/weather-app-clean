import gzip
import json
import os

# 絶対パスでも可
input_path = 'scripts/city.list.json.gz'
output_path = 'scripts/japan_cities_raw.json'

# ファイル存在チェック
if not os.path.exists(input_path):
    print(f"❌ {input_path} が見つかりません")
    exit()

print(f"📦 {input_path} を読み込み中...")

with gzip.open(input_path, 'rt', encoding='utf-8') as f:
    cities = json.load(f)

# countryがJPの都市だけ抽出
japan_cities = [city for city in cities if city.get("country") == "JP"]

print(f"✅ 日本の都市: {len(japan_cities)} 件 抽出済み")

# 保存
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(japan_cities, f, ensure_ascii=False, indent=2)

print(f"📁 出力完了: {output_path}")
