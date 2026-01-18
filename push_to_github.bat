@echo off
echo ===================================
echo 推送修复到 GitHub
echo ===================================
echo.

echo 1. 添加文件...
git add nixpacks.toml railway.json main.py

echo 2. 提交更改...
git commit -m "修复Railway部署：更正启动命令为python main.py"

echo 3. 推送到 GitHub...
git push origin main

echo.
echo 完成！
pause