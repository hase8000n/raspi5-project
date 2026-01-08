#!/bin/bash
# 反射神経測定ゲーム起動スクリプト
# Reaction Time Test Game Launcher

# スクリプトのディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# プロジェクトディレクトリに移動
cd "$PROJECT_DIR" || exit 1

# 仮想環境が存在するか確認
if [ ! -d "venv" ]; then
    echo "仮想環境が見つかりません。作成中..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    # 仮想環境を有効化
    source venv/bin/activate
fi

# ゲームを起動
python examples/reaction_test.py

# 終了時に仮想環境を無効化
deactivate
