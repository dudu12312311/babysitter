@echo off
echo ========================================
echo Railway 部署脚本
echo ========================================
echo.

echo [1/4] 检查 Git 状态...
git status
echo.

echo [2/4] 添加所有更改...
git add .
echo.

echo [3/4] 提交更改...
git commit -m "Fix Railway PORT issue - use gunicorn for production"
echo.

echo [4/4] 推送到 GitHub...
git push origin main
echo.

echo ========================================
echo 部署完成！
echo ========================================
echo.
echo Railway 正在自动部署您的应用...
echo 请访问 Railway 控制台查看部署进度。
echo.
echo 部署完成后，访问：
echo https://web-production-2aba.up.railway.app/diaper
echo.
echo 按任意键退出...
pause > nul
