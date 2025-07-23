from fastapi import APIRouter
from pydantic import BaseModel
import os
import openai
import json
import random
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()

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

# 仮の理由を返す関数
async def generate_reason(name: str, temp: float, humidity: float) -> str:
    response = await openai.ChatCompletion.acreate(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "以下の都市の気候情報をもとに、おすすめ理由を一言で教えてください。"},
            {"role": "user", "content": f"{name} の気温は {temp}℃、湿度は {humidity}% です。"}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()



#async def generate_reason(city_name, temp, humidity): ←コメントアウトでダミー化
    prompt = f"""
都市名：{city_name}
気温：{temp}℃
湿度：{humidity}%
これらの条件をもとに、この都市をおすすめする理由を80文字以内で説明してください。
"""
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            request_timeout=10  # 最大10秒でタイムアウトする
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ 理由生成失敗（{city_name}): {e}")
        return "気候条件によりおすすめです。"


# ✅ NLPフィルターエンドポイント（静的JSONによるフィルター処理）
@router.post("/filter-nlp")
async def filter_nlp(request: NLPFilterRequest):
    conditions = extract_conditions(request.message)
    temp_cond = conditions.get("temperature")
    hum_cond = conditions.get("humidity")

    with open("data/japan_city_weather.json", "r", encoding="utf-8") as f:
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
