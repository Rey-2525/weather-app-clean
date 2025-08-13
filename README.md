# 天気情報取得アプリ（AI × FastAPI）

## 概要
rein-weatherは、現在地や国内の都市の天気情報を取得し、降水確率グラフ表示やAIによる解説・服装アドバイス
を提供するwebアプリです。

## 主な機能
- 現在地の天気予報を現在時刻から3時間ごと×4でグラフ表示する
- 全国の天気情報も併せて表示
- 自然言語によるフィルタで入力した気温、湿度に応じたおすすめ都市を表示する
- 

## 使用技術
- FastAPI
- OpenWeatherMap API
- OpenAI GPT-4 API
- JavaScript / HTML / CSS
- AWS EC2（ubuntu + nginx + systemd）

## AI利用について


## 今後の予定
- AWSへの本番デプロイ（ubuntu + nginx + systemd）
- READMEの整備
- Draw.ioで構成図作成
