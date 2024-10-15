#!/bin/bash

# 仮想環境の作成
python3 -m venv venv

# 仮想環境の有効化
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

echo "仮想環境が作成され、必要なライブラリがインストールされました。"
echo "仮想環境を終了するには 'deactivate' と入力してください。"
