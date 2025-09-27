from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routes import weather, explanation, geocode, filter, nlp_filter
import os


app = FastAPI()
load_dotenv()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(weather.router)
app.include_router(explanation.router)
app.include_router(geocode.router)
app.include_router(filter.router)
app.include_router(filter.router)
app.include_router(nlp_filter.router)  # /filter-nlp 用


# 静的ファイル（CSS等）
app.mount("/static", StaticFiles(directory="static"), name="static")


# Jinja2テンプレート
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "google_maps_api_key": os.getenv("MAPS_PLATFORM_API_KEY")},
    )


@app.get("/health")
def health():
    return {"ok": True}
