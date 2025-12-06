@echo off
echo [1/3] Cleaning old environment...
if exist backend\venv rmdir /s /q backend\venv

echo [2/3] Creating new virtual environment...
cd backend
python -m venv venv
call venv\Scripts\activate

echo [3/3] Installing CLEAN dependencies...
python -m pip install --upgrade pip
:: 使用清华源加速下载，防止网络超时
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo ==========================================
echo      Fixed! Now try running run_app.bat
echo ==========================================
pause