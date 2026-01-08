# Raspberry Pi 5 Project

Raspberry Pi 5を使用したプログラミングと電子工作のプロジェクト用テンプレート

## 概要

このリポジトリは、Raspberry Pi 5での開発を始めるための基本的な構成とサンプルコードを含んでいます。

## 必要なもの

- Raspberry Pi 5
- Raspberry Pi OS (最新版推奨)
- Python 3.9以上

## セットアップ

1. リポジトリをクローン：
```bash
git clone https://github.com/YOUR_USERNAME/raspi5-project.git
cd raspi5-project
```

2. 必要なパッケージをインストール：
```bash
pip install -r requirements.txt
```

3. GPIO権限の設定（必要に応じて）：
```bash
sudo usermod -a -G gpio $USER
```

## ディレクトリ構成

```
raspi5-project/
├── examples/          # サンプルプログラム
├── scripts/           # ユーティリティスクリプト
├── docs/              # ドキュメント
├── README.md          # このファイル
└── requirements.txt   # Python依存パッケージ
```

## 使い方

サンプルプログラムは `examples/` ディレクトリにあります。

基本的なGPIO制御の例：
```bash
python examples/gpio_example.py
```

## 開発環境

- Raspberry Pi 5
- Python 3.x
- GPIO制御ライブラリ（gpiozero, RPi.GPIO等）

## ライセンス

MIT License

## 作成者

Your Name
