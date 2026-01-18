@echo off
echo ========================================
echo 安装宝宝面部融合依赖
echo ========================================
echo.

echo [1/3] 安装 fal-client...
pip install fal-client
if %errorlevel% neq 0 (
    echo 错误: fal-client 安装失败
    pause
    exit /b 1
)
echo ✓ fal-client 安装成功
echo.

echo [2/3] 安装 Flask 文件上传支持...
pip install Flask Werkzeug
if %errorlevel% neq 0 (
    echo 错误: Flask 安装失败
    pause
    exit /b 1
)
echo ✓ Flask 安装成功
echo.

echo [3/3] 安装 Pillow (图片处理)...
pip install Pillow
if %errorlevel% neq 0 (
    echo 错误: Pillow 安装失败
    pause
    exit /b 1
)
echo ✓ Pillow 安装成功
echo.

echo ========================================
echo ✓ 所有依赖安装完成！
echo ========================================
echo.
echo 下一步:
echo 1. 设置 API 密钥: set FAL_KEY=你的密钥
echo 2. 运行测试: python test_face_fusion.py
echo 3. 启动应用: python main_face_fusion.py
echo.
pause
