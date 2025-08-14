# 天気情報取得アプリ（AI × FastAPI）

## 概要
rein-weatherは、現在地や国内の都市の天気情報を取得し、降水確率グラフ表示やAIによる解説・服装アドバイス
を提供するwebアプリです。
FastAPI + OpenWeatherMap API + OpenAI API(gpt-4) + Chart.js を使用し、AWS（EC2 + nginx + gunicorn + systemd + Let's Encrypt）上で運用しています。

## 主な機能
- 現在地の天気取得（気温・湿度・天気アイコン）
- 降水確率グラフ（3時間ごと）
- GPTによる天気解説と服装アドバイス
- 自然文による都市フィルター（例：「涼しい場所を教えて」）
- ダークモード対応 / レスポンシブUI
- 推薦理由キャッシュ（reason_cache.json）

## 使用技術一覧

<img src="https://img.shields.io/badge/-JavaScript-F7DF1E.svg?logo=javascript&logoColor=black&style=for-the-badge"> <img src="https://img.shields.io/badge/-Css-purple.svg?logo=css&style=for-the-badge"> <img src="https://img.shields.io/badge/-Html5-E34F26.svg?logo=html5&logoColor=white&style=for-the-badge">
<img src="https://img.shields.io/badge/-FastAPI-000000.svg?logo=fastapi&style=for-the-badge">
<img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
<img src="https://img.shields.io/badge/-gunicorn-000000.svg?logo=gunicorn&style=for-the-badge">

<img src="https://img.shields.io/badge/-Nginx-269539.svg?logo=nginx&style=for-the-badge"> <img src="https://img.shields.io/badge/-Amazon%20aws-232F3E.svg?logo=amazon-aws&style=for-the-badge"> <img src="https://img.shields.io/badge/-Ubuntu-E95420.svg?logo=ubuntu&logoColor=white&style=for-the-badge"> <img src="https://img.shields.io/badge/-Amazon%20EC2-232F3E.svg?logo=amazon-EC2&style=for-the-badge">

## 技術構成

- **バックエンド**: FastAPI（python）, gunicorn
- **フロントエンド**: HTML, CSS, JavaScript, Chart.js
- **API**:
    - OpenWeatherMap API
    - OpenAI API
    - Google Maps API
- **インフラ**: AWS EC2 (Ubuntu), nginx, Let's Encrypt SSL, systemd

## AI利用について

## 📷 スクリーンショット

（ここにアプリのスクショを貼る）

---

## 📂 ディレクトリ構造

```
csharp
CopyEdit
weather-app-clean/
├── app/                # FastAPIアプリケーション
├── static/             # CSS / 画像 / favicon
├── templates/          # HTMLテンプレート
├── data/               # キャッシュ・データファイル
├── main.py
└── requirements.txt

```

---

## ⚙️ セットアップ方法

### 1. 環境構築

```bash
bash
CopyEdit
git clone https://github.com/<yourname>/rein-weather.git
cd rein-weather
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

### 2. 環境変数設定（.env）

```
ini
CopyEdit
OPENWEATHER_API_KEY=xxxxx
OPENAI_API_KEY=xxxxx

```

### 3. ローカル実行

```bash
bash
CopyEdit
uvicorn main:app --reload

```

### 4. AWSデプロイ（簡易手順）

- EC2インスタンス作成（Ubuntu）
- 必要パッケージインストール（Python, nginx, certbot等）
- アプリ配置＆gunicorn + systemd設定
- nginxリバースプロキシ設定
- Let's EncryptでSSL化

詳細手順は Qiita記事 に記載。

---

## 📊 構成図

（Draw.io等で作成したAWS構成図をここに貼る）

---

## 🧩 トラブルシュート

### 静的ファイル（CSS・favicon）が表示されない場合

- **症状**:

```
pgsql
CopyEdit
GET https://your-domain.com/static/style-dark.css 403 (Forbidden)
GET https://your-domain.com/favicon.ico 403 (Forbidden)

```

- **原因**: `/home/ubuntu` に `www-data` ユーザーが入れない（実行権限不足）
- **解決**:

```bash
sudo chmod 755 /home/ubuntu
sudo chmod 755 /home/ubuntu/weather-app-clean
sudo chmod 755 /home/ubuntu/weather-app-clean/static
sudo chmod 644 /home/ubuntu/weather-app-clean/static/style-dark.css
sudo chmod 644 /home/ubuntu/weather-app-clean/static/favicon.ico
sudo nginx -t && sudo systemctl reload nginx

```

---

## 📌 今後の改善予定

- UIデザインのブラッシュアップ
- 監視設定（CloudWatchなど）
- 国際化対応
- キャッシュ戦略最適化

---

## 📜 ライセンス

MIT License
