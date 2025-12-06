# PicFinder AI 🔍

<div align="center">
  <img src="public/logo.png" width="120" height="120" alt="PicFinder AI Logo">
  
  <h1>PicFinder AI</h1>
  
  <p>
    <strong>Smart Local Image Search Engine powered by OpenAI CLIP</strong><br>
    基于 OpenAI CLIP 的本地语义图片搜索引擎<br>
    OpenAI CLIPを搭載したローカル意味的画像検索エンジン
  </p>

  <p>
    <a href="#-english">English</a> •
    <a href="#-中文">中文</a> •
    <a href="#-日本語">日本語</a>
  </p>

  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Electron-Vue3-green?logo=electron" alt="Electron">
  <img src="https://img.shields.io/badge/AI-CLIP%20Model-orange" alt="AI Model">
  <img src="https://img.shields.io/badge/Privacy-100%25%20Offline-red" alt="Privacy">
</div>

---

<a name="-english"></a>
## 🇬🇧 English

### Introduction
**PicFinder AI** is a desktop application that allows you to search through your local photo albums using natural language. Instead of filenames, simply search for *"A cat sleeping on the sofa"* or *"Red sports car"*. Powered by the **CLIP** model, it runs 100% offline, ensuring your photos never leave your device.

### ✨ Features
- **Semantic Search**: Search by content description, not just keywords.
- **Privacy First**: Completely offline. No cloud uploads.
- **Smart Indexing**: Incremental scanning that only processes new images.
- **Multilingual Support**: Supports queries in English, Chinese, and Japanese.

### 🚀 Quick Start

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/Breathinggg/PicFinder-AI.git](https://github.com/Breathinggg/PicFinder-AI.git)
   cd PicFinder-AI
One-Click Installation Run the installer script to set up the Python environment and dependencies.

DOS

install.bat
Run the App

DOS

run_app.bat
⚠️ Note: On the first run, the backend will automatically download the AI model (~1.5GB). Please wait patiently.

<a name="-中文"></a>

🇨🇳 中文
简介
PicFinder AI 是一款基于自然语言的本地桌面图片搜索工具。你不再需要记忆文件名，只需描述画面内容（如“睡在沙发上的猫”或“红色跑车”）即可找到图片。本应用内置 CLIP 模型，完全离线运行，确保你的照片隐私绝对安全，不会上传至云端。

✨ 功能亮点
语义搜索: 理解图片内容，用自然语言搜索。

隐私优先: 100% 本地运行，无需联网，无数据上传。

智能索引: 增量扫描模式，只处理新增图片，速度更快。

多语言支持: 支持中文、英文、日语搜索指令。

🚀 快速开始
克隆仓库

Bash

git clone [https://github.com/Breathinggg/PicFinder-AI.git](https://github.com/Breathinggg/PicFinder-AI.git)
cd PicFinder-AI
一键安装环境 双击运行安装脚本，自动配置 Python 虚拟环境和依赖。

DOS

install.bat
启动应用

DOS

run_app.bat
⚠️ 注意： 首次运行时，程序会自动从 Hugging Face 下载 AI 模型（约 1.5GB）。请耐心等待终端窗口中的下载进度完成。

<a name="-日本語"></a>

🇯🇵 日本語
はじめに
PicFinder AI は、自然言語を使ってローカルのフォトアルバムを検索できるデスクトップアプリです。ファイル名を覚える必要はなく、「ソファで寝ている猫」や「赤いスポーツカー」のように検索するだけで画像が見つかります。CLIP モデルを搭載しており、完全オフラインで動作するため、写真がクラウドにアップロードされることはなく、プライバシーは守られます。

✨ 特徴
意味的検索: キーワードだけでなく、画像の内容を理解して検索します。

プライバシー重視: 100% ローカル動作。インターネット接続は不要です。

スマートインデックス: 新しい画像のみをスキャンする増分処理機能。

多言語対応: 日本語、英語、中国語での検索に対応しています。

🚀 クイックスタート
リポジトリのクローン

Bash

git clone [https://github.com/Breathinggg/PicFinder-AI.git](https://github.com/Breathinggg/PicFinder-AI.git)
cd PicFinder-AI
ワンクリック・インストール インストーラースクリプトを実行して、環境構築を行います。

DOS

install.bat
アプリの起動

DOS

run_app.bat
⚠️ 注意: 初回起動時、AIモデル（約1.5GB）が自動的にダウンロードされます。完了するまでそのままお待ちください。

🛠️ Tech Stack / 技术栈 / 技術スタック
Frontend: Electron, Vue 3, Vite

Backend: Python (FastAPI, Uvicorn)

AI Core: sentence-transformers (clip-ViT-L-14)

Database: ChromaDB (Vector Store)

📄 License
Distributed under the MIT License.

<div align="center"> <p>Made with ❤️ by <a href="https://www.google.com/search?q=https://github.com/Breathinggg">Breathinggg</a></p> </div>