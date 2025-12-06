@echo off
title PicFinder AI Launcher
echo ==========================================
echo       Starting PicFinder AI...
echo ==========================================

:: 1. 启动后端 (强制使用 install.bat 创建的虚拟环境)
echo Starting Backend...
start "PicFinder Backend" cmd /k "cd backend && call venv\Scripts\activate && uvicorn api:app --reload --port 8000"

:: 2. 启动前端
echo Starting Frontend...
:: 等待一下让后端先跑
timeout /t 3 /nobreak >nul
start "PicFinder Frontend" cmd /k "npm run dev"

echo.
echo App is running! Close the windows to stop.
echo.