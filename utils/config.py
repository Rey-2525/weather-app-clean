import os
from dotenv import load_dotenv

load_dotenv()

# OpenWeatherMapのAPIキーを環境変数から取得
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
# Google Maps API 用
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")