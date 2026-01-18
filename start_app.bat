@echo off
echo ========================================
echo 启动硬核育儿模拟器
echo ========================================
echo.

echo 检查 Python...
python --version
echo.

echo 检查依赖...
python -m pip show flask
echo.

echo 启动应用...
python main.py
