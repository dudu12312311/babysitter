# ⚡ Railway 部署 - 快速修复

## 🔴 问题

您的 Railway 部署失败，错误信息：
```
Error: Invalid value for '--port': '$PORT' is not a valid integer.
```

## ✅ 解决方案

**问题原因：** Flask 开发服务器无法正确处理 Railway 的 `$PORT` 环境变量。

**解决方法：** 使用 `gunicorn` 生产级 WSGI 服务器。

---

## 🚀 立即修复（3步）

### 步骤 1：确认文件已更新

已修复的文件：
- ✅ `requirements.txt` - 添加了 gunicorn
- ✅ `Procfile` - 使用 gunicorn 启动
- ✅ `railway.json` - 更新启动命令
- ✅ `nixpacks.toml` - 配置 gunicorn

### 步骤 2：部署到 Railway

**方法 A：使用批处理文件（最简单）**
```bash
# 双击运行
deploy_to_railway.bat
```

**方法 B：手动命令**
```bash
git add .
git commit -m "Fix Railway PORT issue - use gunicorn"
git push origin main
```

### 步骤 3：等待部署完成

1. 访问 Railway 控制台
2. 查看部署进度（2-5分钟）
3. 等待状态变为 "Active"

---

## 🔍 验证部署

### 测试健康检查
```
https://web-production-2aba.up.railway.app/health
```

**预期响应：**
```json
{
  "status": "healthy",
  "message": "应用运行正常",
  "game_available": true
}
```

### 测试换尿布任务
```
https://web-production-2aba.up.railway.app/diaper
```

**预期结果：** 看到换尿布任务页面，包含哭脸 😭

---

## 📋 修改内容

### requirements.txt
```diff
Flask==2.3.3
fal-client
+ gunicorn==21.2.0
```

### Procfile
```diff
- web: python main.py
+ web: gunicorn main:app --bind 0.0.0.0:$PORT
```

### railway.json
```diff
"deploy": {
-   "startCommand": "python main.py",
+   "startCommand": "gunicorn main:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120",
}
```

### nixpacks.toml
```diff
[start]
- cmd = "python main.py"
+ cmd = "gunicorn main:app --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120"
```

---

## 🎯 成功标志

部署成功后，Railway 日志应该显示：
```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:8000
[INFO] Using worker: sync
[INFO] Booting worker with pid: 123
```

---

## 🐛 如果仍然失败

### 检查清单

1. **确认文件已推送**
   ```bash
   git status
   # 应该显示 "nothing to commit, working tree clean"
   ```

2. **检查 Railway 日志**
   - 在 Railway 控制台查看 "Deploy Logs"
   - 查找错误信息

3. **手动触发重新部署**
   - 在 Railway 控制台点击 "Redeploy"

4. **检查环境变量**
   - 确认 Railway 设置了 PORT 变量
   - 通常 Railway 自动设置

---

## 💡 为什么这样修复？

### 问题分析

**之前（错误）：**
```bash
python main.py
# Flask 开发服务器尝试读取 $PORT
# 但 $PORT 被当作字符串 "$PORT" 而不是数字
```

**现在（正确）：**
```bash
gunicorn main:app --bind 0.0.0.0:$PORT
# Gunicorn 正确解析 $PORT 环境变量
# 将其转换为实际的端口号（如 8000）
```

### Gunicorn 优势

- ✅ 生产级服务器
- ✅ 正确处理环境变量
- ✅ 支持多进程
- ✅ 自动重启
- ✅ 更好的性能

---

## 📞 需要帮助？

查看详细文档：
- `Railway部署修复指南.md` - 完整说明
- `Railway网页版完整操作指南.md` - Railway 使用指南

---

**现在运行 `deploy_to_railway.bat` 或手动推送代码！** 🚀
