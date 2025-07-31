from fastapi import APIRouter
from pydantic import BaseModel
import os
import openai
import json
import random
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()

CACHE_PATH = "data/reason_cache.json"

# ✅ OpenAI APIキー
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ モデル定義
class NLPFilterRequest(BaseModel):
    message: str

# ✅ few-shot付き条件抽出関数
def extract_conditions(message: str) -> dict:
    prompt = f"""
あなたは天気アシスタントです。
ユーザーの自然な表現から「temperature（気温）」と「humidity（湿度）」の条件を抽出してください。

出力形式（JSON）:
例: {{ "temperature": "<=25", "humidity": ">=70" }}
例: {{}}（条件が曖昧 or 条件なしの場合）

# Few-shot例:

リクエスト:「ひんやりする場所を教えて」
出力: {{"temperature": "<=25"}}

リクエスト:「ジメジメしてる場所を探したい」
出力: {{"humidity": ">=70"}}

リクエスト:「暑すぎる場所は避けたい」
出力: {{"temperature": "<=28"}}

リクエスト:「カラッとしてて暑い場所がいい」
出力: {{"temperature": ">=28", "humidity": "<=60"}}

リクエスト:「湿度が低くて気温が30度以上の都市」
出力: {{"temperature": ">=30", "humidity": "<=60"}}

リクエスト:「涼しいかつジメジメしてない場所」
出力: {{"temperature": "<=25", "humidity": "<=60"}}

リクエスト:「過ごしやすい場所」
出力: {{"temperature": "<=28", "humidity": "<=70"}}

リクエスト:「暑すぎず湿度も低いところ」
出力: {{"temperature": "<=30", "humidity": "<=60"}}

リクエスト: 「暑すぎず湿度も低いところ」
出力: {{"temperature": "<=30", "humidity": "<=60"}}

リクエスト: 「ジメジメしない場所がいい」
出力: {{"humidity": "<=60"}}

リクエスト: 「快適な気候のところ」
出力: {{"temperature": ">=20", "temperature": "<=28", "humidity": "<=65"}}

リクエスト: 「蒸し暑いのは苦手」
出力: {{"temperature": "<=30", "humidity": "<=60"}}

リクエスト: 「カラッとしてて暖かいところ」
出力: {{"temperature": ">=28", "humidity": "<=55"}}

リクエスト: 「乾燥しすぎないところがいい」
出力: {{"humidity": ">=40"}}

リクエスト: 「暑いところ」
出力: {{"temperature": ">=30"}}

リクエスト:「30度くらいの暑さが好き」
出力: {{"temperature": ">=28"}}

リクエスト:「涼しくてジメジメしない場所がいい」
出力: {{"temperature": "<=25", "humidity": "<=60"}}

リクエスト:「湿度は気にならないけど、寒いのは嫌だ」
出力: {{"temperature": ">=20"}}

リクエスト:「あたたかくてカラッとしてる場所」
出力: {{"temperature": ">=25", "humidity": "<=55"}}

リクエスト:「とにかく暑いところがいい！」
出力: {{"temperature": ">=32"}}

リクエスト:「寒くてもいいから湿度が低いところ」
出力: {{"humidity": "<=50"}}

リクエスト:「夏っぽい場所」
出力: {{"temperature": ">=30", "humidity": ">=60"}}

リクエスト:「秋っぽい涼しさ」
出力: {{"temperature": "<=24", "humidity": "<=65"}}

リクエスト:「春のような快適な気候」
出力: {{"temperature": ">=18", "temperature": "<=26", "humidity": "<=65"}}

リクエスト:「じめっとしてる場所を探してる」
出力: {{"humidity": ">=75"}}

リクエスト:「気温は低くてもOK。乾燥してる場所がいい」
出力: {{"humidity": "<=55"}}

リクエスト:「今の季節より暖かい場所」
出力: {{"temperature": ">=25"}}  # ※仮定値



リクエスト:「特に条件はない」
出力: {{}}

# ユーザーのリクエスト:
「{message}」
""".strip()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        json_text = response.choices[0].message.content.strip()
        print("抽出条件:", json_text)
        return json.loads(json_text)
    except Exception as e:
        print("❌ 条件抽出失敗:", e)
        return {}

import json
import os

CACHE_PATH = "data/reason_cache.json"

# キャッシュ読み込み
if os.path.exists(CACHE_PATH):
    with open(CACHE_PATH, "r", encoding="utf-8") as f:
        reason_cache = json.load(f)
else:
    reason_cache = {}

async def generate_reason(city_name, temp, humidity):
    # キャッシュに存在すればそれを返す
    if city_name in reason_cache:
        return reason_cache[city_name]

    # 存在しなければGPTから生成（↓ここにOpenAI API呼び出し）
    prompt = f"{city_name}は気温{temp}℃、湿度{humidity}%ですが、なぜおすすめですか？"
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "旅行者にわかりやすく短めに説明してください。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        reason = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ 理由生成失敗（{city_name}): {e}")
        return f"{city_name} は気温{temp}℃、湿度{humidity}%でおすすめです。"

    # キャッシュに保存
    reason_cache[city_name] = reason
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(reason_cache, f, ensure_ascii=False, indent=2)

    return reason



# ✅ NLPフィルターエンドポイント（静的JSONによるフィルター処理）
@router.post("/filter-nlp")
async def filter_nlp(request: NLPFilterRequest):
    conditions = extract_conditions(request.message)
    temp_cond = conditions.get("temperature")
    hum_cond = conditions.get("humidity")

    with open("data/japan_city_weather_limited_ja_extended.json", "r", encoding="utf-8") as f:
        cities = json.load(f)

    matched = []
    for city in cities:
        try:
            name = city["name"]
            temp = city["temp"]
            humidity = city["humidity"]

            # 条件に合わなければスキップ
            if temp_cond and not eval(f"{temp}{temp_cond}"):
                continue
            if hum_cond and not eval(f"{humidity}{hum_cond}"):
                continue

            matched.append({
                "name": name,
                "temp": temp,
                "humidity": humidity
            })

        except Exception as e:
            print(f"❌ {city['name']} のフィルタ処理でエラー: {e}")
            continue

    # ✅ 抽出＆理由生成（1件のみ）
    if matched:
        selected = random.choice(matched)
        try:
            reason = await generate_reason(selected["name"], selected["temp"], selected["humidity"])
            selected["reason"] = reason
        except Exception as e:
            print(f"❌ 理由生成失敗（{selected['name']}）: {e}")
            selected["reason"] = "理由の生成に失敗しました。"

        result = [selected]
    else:
        result = [{"message": "条件に合う都市が見つかりませんでした。"}]

    return {"cities": result}
