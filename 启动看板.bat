@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 正在启动数据看板...
echo 请在浏览器中打开: http://localhost:8080
echo.
echo 按 Ctrl+C 停止服务器
python -m http.server 8080
