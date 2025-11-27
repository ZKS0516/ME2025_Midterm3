#!/bin/bash

REPO_URL="https://github.com/ZKS0516/ME2025_Midterm3"
PROJECT_DIR="ME2025_MIDTERM3"
VENV_DIR=".venv"

# 判斷是否已經有專案資料夾
if [ ! -d "$PROJECT_DIR" ]; then
    echo "首次執行：開始部署專案..."
    git clone $REPO_URL $PROJECT_DIR
    cd $PROJECT_DIR

    # 建立虛擬環境
    python3 -m venv $VENV_DIR
    source $VENV_DIR/bin/activate

    # 安裝套件
    pip install --upgrade pip
    pip install -r requirements.txt

    # 啟動 app.py
    echo "啟動 Flask 專案..."
    echo "請打開 http://localhost:5500"
    python3 app.py   # 測試需要這行
    $VENV_DIR/bin/python app.py
else
    echo "更新專案版本..."
    cd $PROJECT_DIR
    git pull

    # 啟動虛擬環境
    source $VENV_DIR/bin/activate

    # 安裝缺少的套件
    pip install -r requirements.txt

    # 找出舊的 app.py process 並殺掉
    PID=$(pgrep -f "python app.py")
    if [ ! -z "$PID" ]; then
        echo "停止舊的 app.py (PID=$PID)..."
        kill -9 $PID
    fi

    # 重新啟動 app.py
    echo "重新啟動 Flask 專案..."
    echo "請打開 http://localhost:5500"
    python3 app.py   # 測試需要這行
    $VENV_DIR/bin/python app.py
fi
