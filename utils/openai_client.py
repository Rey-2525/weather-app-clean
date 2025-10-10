from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi import HTTPException
import logging

log = logging.getLogger("uvicorn.error")

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-5-nano")


def _first_text(resp) -> str:
    # 1) 最短経路
    t = getattr(resp, "output_text", None)
    if t:
        return t.strip()

    # 2) output 配列を総なめ
    try:
        parts = []
        for item in getattr(resp, "output", []) or []:
            # message にテキストがある場合を吸い上げ
            if getattr(item, "type", "") == "message":
                for c in getattr(item, "content", []) or []:
                    txt = getattr(c, "text", None)
                    if txt:
                        parts.append(txt)
        if parts:
            return " ".join(p.strip() for p in parts if p.strip())
    except Exception as e:
        log.exception("extract text fallback failed: %s", e)

    # 3) 不完全理由があればログ
    inc = getattr(resp, "incomplete_details", None)
    if inc:
        log.warning("LLM incomplete: reason=%s", getattr(inc, "reason", "?"))

    # 4) 最後の砦：空はUXが悪いので短いメッセージを返す
    return ""


async def generate_weather_explanation(data):
    location = data.get("location", "指定なし")
    weather = data.get("weather", "不明")
    temp = data.get("temp", 0)
    humidity = data.get("humidity", 0)
    pop = int(data.get("pop", 0) * 100)

    prompt = (
        "以下の天気データをもとに、日本語で200文字以内の天気解説文を作成してください。\n"
        f"場所:{location} 天気:{weather} 気温:{temp}℃ 湿度:{humidity}% 降水確率:{pop}%\n"
        "落ち着いた口調で、情緒を大切に。"
    )

    resp = client.responses.create(
        model=MODEL,
        input=prompt,
        max_output_tokens=512,
        reasoning={"effort": "low"},
        text={"verbosity": "low"},
        # temperature は固定(1.0)なので指定不要
    )
    text = _first_text(resp).strip()
    if not text:
        # 空で返すよりは明示的にエラー → フロントのconsoleに表示させて気づけるように
        log.warning(
            "OpenAI returned empty text (tokens=%s)", getattr(resp, "total_tokens", "?")
        )
        raise HTTPException(
            status_code=512,
            detail="LLM生成に失敗しました（空の応答）。再試行してください。",
        )
    return text


async def generate_clothing_advice(data):
    temp = data.get("temp", 0)
    humidity = data.get("humidity", 0)
    weather = data.get("weather", "不明")

    prompt = (
        "以下の天気データをもとに、日本語で200文字以内の服装アドバイスを作成してください。\n"
        f"天気:{weather} 気温:{temp}℃ 湿度:{humidity}%\n"
        "やさしい口調で、体調への気遣いも一言添えて。"
    )

    resp = client.responses.create(
        model=MODEL,
        input=prompt,
        max_output_tokens=768,
        reasoning={"effort": "low"},
        text={"verbosity": "low"},
        # temperature は固定(1.0)なので指定不要
    )
    text = _first_text(resp).strip()
    if not text:
        # 空で返すよりは明示的にエラー → フロントのconsoleに表示させて気づけるように
        log.warning(
            "OpenAI returned empty text (tokens=%s)", getattr(resp, "total_tokens", "?")
        )
        raise HTTPException(
            status_code=502,
            detail="LLM生成に失敗しました（空の応答）。再試行してください。",
        )
    return text
