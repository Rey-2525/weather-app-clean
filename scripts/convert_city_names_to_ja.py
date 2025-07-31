import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

# 環境変数を読み込み
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# OpenAIクライアントを初期化
client = OpenAI(api_key=api_key)

# 入出力ファイル
INPUT_FILE = "data/japan_city_weather.json"
OUTPUT_FILE = "data/japan_city_weather_ja.json"

# GPTで都市名を日本語に翻訳
def translate_name_gpt(name_en: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "あなたは地名翻訳のアシスタントです。英語の都市名を日本語に正確に翻訳してください。"
                },
                {
                    "role": "user",
                    "content": f"都市名: {name_en}\n日本語での地名:"
                }
            ],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ {name_en} の翻訳失敗: {e}")
        return name_en  # 失敗したら元の名前を返す

# メイン処理
def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        cities = json.load(f)

    translated = []
    for city in tqdm(cities[:100], desc="🌐 GPT翻訳テスト中"):
        name_en = city["name"]
        name_ja = translate_name_gpt(name_en)
        translated.append({
            "name": name_ja,
            "temp": city["temp"],
            "humidity": city["humidity"]
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(translated, f, ensure_ascii=False, indent=2)

    print(f"✅ 保存完了: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
