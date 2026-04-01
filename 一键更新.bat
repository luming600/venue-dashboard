@echo off
chcp 65001 >nul
echo ========================================
echo   杆杆响天梯赛知识库 - 一键更新工具
echo ========================================
echo.

echo [1/2] 提取 .docx 文件内容...
python "%~dp0extract_docs.py"
if %errorlevel% neq 0 (
    echo 提取失败！请检查 Python 环境
    pause
    exit /b 1
)

echo.
echo [2/2] 更新网页内容...
python "%~dp0generate_web_content.py"
if %errorlevel% neq 0 (
    echo 更新失败！请检查 Python 环境
    pause
    exit /b 1
)

echo.
echo ========================================
echo   更新完成！请刷新网页查看
echo ========================================
echo.
pause
