import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_weather_explanation(data):
    location = data.get("location", "指定なし")
    weather = data.get("weather", "不明")
    temp = data.get("temp", 0)
    humidity = data.get("humidity", 0)
    pop = int(data.get("pop", 0) * 100)

    prompt = (
    f"以下の天気データをもとに、少し大人びた、落ち着いた色気を感じさせる日本語で天気解説文を作成してください。\n"
    f"場所: {location}、天気: {weather}、気温: {temp}℃、湿度: {humidity}％、降水確率: {pop}％。\n"
    f"しっとりとした語り口で、情緒や雰囲気を大切にしながら、100文字以内で表現してください。"
)


    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=150
    )

    return response.choices[0].message.content.strip()


async def generate_clothing_advice(data):
    temp = data.get("temp", 0)
    humidity = data.get("humidity", 0)
    weather = data.get("weather", "不明")

    prompt = (
    f"以下の天気データをもとに、服装アドバイスを日本語で作成してください。\n"
    f"天気: {weather}、気温: {temp}℃、湿度: {humidity}％。\n"
    f"やさしく落ち着いた口調で、ほんのり色気と大人の余裕を感じさせる文章をお願いします。\n"
    f"気温や湿度の体感も含めて、体調を気遣うようなアドバイスを100文字以内で表現してください。"
)


    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=100
    )

    return response.choices[0].message.content.strip()
