@echo off
echo ========================================
echo 安装背景音乐系统依赖
echo ========================================
echo.

echo [1/1] 安装 pygame...
python -m pip install pygame
if %errorlevel% neq 0 (
    echo 错误: pygame 安装失败
    pause
    exit /b 1
)
echo ✓ pygame 安装成功
echo.

echo ========================================
echo ✓ 依赖安装完成！
echo ========================================
echo.
echo 下一步:
echo 1. 将音乐文件放入 music 文件夹
echo 2. 支持格式: MP3, WAV, OGG, FLAC
echo 3. 运行测试: python background_music.py
echo 4. 启动应用: python main.py
echo.
pause
