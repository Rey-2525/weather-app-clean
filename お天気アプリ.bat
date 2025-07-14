@echo off
cd /d C:\my-weather-app

REM 仮想環境をアクティベート
call venv\Scripts\activate.bat

REM Uvicornを起動
start cmd /k "uvicorn main:app --reload"

REM 少し待ってからブラウザを開く（ポート開くのに1秒くらい猶予）
timeout /t 2 > nul
start http://127.0.0.1:8000