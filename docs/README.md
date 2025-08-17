# rein-weather（AI × FastAPI）

## 概要
rein-weatherは、AIによる解説と服装アドバイスを提供する天気アプリです。

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

<img src="https://img.shields.io/badge/-Nginx-269539.svg?logo=nginx&style=for-the-badge"> <img src="https://img.shields.io/badge/-Amazon%20aws-232F3E.svg?logo=amazon-aws&style=for-the-badge"> <img src="https://img.shields.io/badge/-Ubuntu-E95420.svg?logo=ubuntu&logoColor=white&style=for-the-badge"> <img src="https://img.shields.io/badge/-Amazon%20EC2-232F3E.svg?logo=amazon-EC2&style=for-the-badge"> <img src="https://img.shields.io/badge/-Linux-FCC624.svg?logo=Linux&logoColor=black&style=for-the-badge">

## 技術構成

- **バックエンド**: FastAPI（python）, gunicorn
- **フロントエンド**: HTML, CSS, JavaScript, Chart.js
- **API**:
    - OpenWeatherMap API
    - OpenAI API
    - Google Maps API
- **インフラ**: AWS EC2 (Ubuntu), nginx, Let's Encrypt SSL, systemd

## 開発背景
課題：実務や資格ではweb開発からAWS構築まで経験できない
→なら自分ですべてやってしまおうと思った。
解決行動：自分で企画、設計し、Linux、AWS運用含めたアプリ開発を実施。
結果：AWS EC2の本番運用まで実施。

**成果**：
- AWS EC2本番運用（HTTPS化）
- OpenAI APIを用いた説明文生成
- Linuxサーバー構築・運用
- GitHubでのバージョン管理実践

## AI利用について
本アプリのコード生成はChatGPTを活用しました。

- APIの利用方法やルーティング処理の提案
- UI改善のためのHTMLやCSSコーディング

最終的な構成・機能設計・AWS構築はすべて自身で行い、  
AIからの提案はコードレビュー・修正を経て採用しています。

コーディングはAIに任せて、最終的に自分でそれらのコードを
統合させて開発・構築・運用していく形にしました。

## ディレクトリ構造

```
.
└── my-weather-app/
    ├── .vscode/
    │   └── settings.json
    ├── __pycache__/
    ├── data
    ├── docs/
    │   ├── AWS-architecture.drawio
    │   ├── AWS-config.drawio.png
    │   ├── ChatGPT image Aug 11, 2025,08_12_56 PM.png
    │   └── README.md
    ├── routes/
    │   ├── explanation.py
    │   ├── filter.py
    │   ├── generate_cities.py
    │   ├── geocode.py
    │   ├── nlp_filer.py
    │   ├── view.py
    │   └── weather.py
    ├── scripts
    ├── static/
    │   ├── android-chrome-192x192.png
    │   ├── android-chrome-512x512.png
    │   ├── apple-touch-icon.png
    │   ├── favicon-16x16.png
    │   ├── favicon-32x32.png
    │   ├── favicon.ico
    │   ├── site.webmanifest
    │   └── style-dark.css
    ├── templates/
    │   └── index.html
    ├── utils/
    │   ├── config.py
    │   └── openai_client.py
    ├── .gitattributes
    ├── .gitignore
    ├── 0.23.0
    ├── main.py
    └── requirements.txt
```

---

## セットアップ方法

### 1. 環境構築

```
git clone https://github.com/<yourname>/rein-weather.git
cd rein-weather
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

windowsの場合：
```
venv/scripts/activate
```

### 2. 環境変数設定（.env）

```
OPENWEATHER_API_KEY=xxxxx
OPENAI_API_KEY=xxxxx
```

### 3. ローカル実行

```
uvicorn main:app --reload
```

### 4. AWSデプロイ（簡易手順）

- EC2インスタンス作成（Ubuntu）
- 必要パッケージインストール（Python, nginx, certbot等）
- アプリ配置＆gunicorn + systemd設定
- nginxリバースプロキシ設定
- Let's EncryptでSSL化

---

## 構成図（/docsにソースあり）
<img width="1648" height="741" alt="AWS-config drawio" src="https://github.com/user-attachments/assets/b33c0f42-bf84-4b83-ab8d-c6ed90d7e614" />


---

## トラブルシュート

### 静的ファイル（CSS・favicon）が表示されない場合

- **症状**:

```
GET https://your-domain.com/static/style-dark.css 403 (Forbidden)
GET https://your-domain.com/favicon.ico 403 (Forbidden)
```

- **原因**: `/home/ubuntu` に `www-data` ユーザーが入れない（実行権限不足）
- **解決**:

```
sudo chmod 755 /home/ubuntu
sudo chmod 755 /home/ubuntu/weather-app-clean
sudo chmod 755 /home/ubuntu/weather-app-clean/static
sudo chmod 644 /home/ubuntu/weather-app-clean/static/style-dark.css
sudo chmod 644 /home/ubuntu/weather-app-clean/static/favicon.ico
sudo nginx -t && sudo systemctl reload nginx
```

---

## 今後の改善予定

- UI改善（カードレイアウト整理・検索バー固定）
- 監視設定の導入（CloudWatch Logs, メトリクス監視）
- TerraformでAWS環境構築 + Ansibleで構成管理
- GitHub Actionsで自動反映させる

---

## ライセンス

MIT License
