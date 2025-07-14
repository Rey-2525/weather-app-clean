from fastapi import APIRouter
from pydantic import BaseModel
import os
import openai
import json
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
ユーザーの要望から「temperature（気温）」と「humidity（湿度）」の条件を抽出してください。

出力形式（JSON）:
例1: {{ "temperature": "<=25", "humidity": "<=60" }}
例2: {{}} （条件が曖昧すぎる or 条件なしの場合）

# Few-shot例:
リクエスト:「ひんやりする場所を教えて」
出力: {{ "temperature": "<=25" }}

リクエスト:「湿度が高めの場所」
出力: {{ "humidity": ">=70" }}

リクエスト: 「暑すぎる場所は避けたい」
出力: {{"temperature": "<=28"}}

リクエスト: 「涼しい場所を教えて」
出力: {{"temperature": "<=25"}}

リクエスト: 「ジメジメしてる場所を探したい」
出力: {{"humidity": ">=70"}}

リクエスト: 「カラッとしてて暑い場所がいい」
出力: {{"temperature": ">=28", "humidity": "<=60"}}

リクエスト: 「ひんやりする場所」
出力: {{"temperature": "<=25"}}

リクエスト: 「湿度が低くて気温が30度以上の都市」
出力: {{"temperature": ">=30", "humidity": "<=60"}}

リクエスト:「条件は特にない」
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

# ✅ メイン処理
@router.post("/filter-nlp")
async def filter_nlp(request: NLPFilterRequest):
    # ⛏ 条件抽出
    conditions = extract_conditions(request.message)
    temp_cond = conditions.get("temperature")
    hum_cond = conditions.get("humidity")

    # 📥 JSONデータから都市情報を読み込む
    with open("data/japan_cities.json", "r", encoding="utf-8") as f:
        cities_data = json.load(f)

    result = []
    for c in cities_data:
        try:
            if temp_cond and not eval(f"{c['temp']}{temp_cond}"):
                continue
            if hum_cond and not eval(f"{c['humidity']}{hum_cond}"):
                continue
            result.append(c["name"])
        except Exception as e:
            print(f"{c['name']} に失敗:", e)
            continue

    if not result:
        result = ["条件に合う都市が見つかりませんでした。"]

    return {"cities": result}
