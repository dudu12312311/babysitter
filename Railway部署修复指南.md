# 🚀 Railway 部署修复指南

## ❌ 问题诊断

您遇到的错误：
```
Error: Invalid value for '--port': '$PORT' is not a valid integer.
```

**原因：** `$PORT` 环境变量没有被正确解析，被当作字符串传递给了应用。

---

## ✅ 已修复的文件

### 1. requirements.txt
添加了 `gunicorn` 作为生产环境 WSGI 服务器：
```
Flask==2.3.3
fal-client
gunicorn==21.2.0
```

### 2. Procfile
使用 gunicorn 启动应用：
```
web: gunicorn main:app --bind 0.0.0.0:$PORT
```

### 3. railway.json
更新启动命令：
```json
{
  "deploy": {
    "startCommand": "gunicorn main:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120"
  }
}
```

### 4. nixpacks.toml
使用 gunicorn 启动：
```toml
[start]
cmd = "gunicorn main:app --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120"
```

---

## 🚀 部署步骤

### 方法 1：通过 Git 推送（推荐）

```bash
# 1. 提交更改
git add .
git commit -m "Fix Railway PORT variable issue - use gunicorn"

# 2. 推送到 GitHub
git push origin main

# 3. Railway 会自动检测并重新部署
```

### 方法 2：手动触发重新部署

1. 访问 Railway 控制台
2. 找到您的项目
3. 点击 "Deploy" 按钮
4. 等待部署完成

---

## 🔍 验证部署

### 检查部署日志

在 Railway 控制台查看：
1. **Build Logs** - 应该显示成功安装 gunicorn
2. **Deploy Logs** - 应该显示 gunicorn 启动信息

**成功的日志应该类似：**
```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:8000
[INFO] Using worker: sync
[INFO] Booting worker with pid: 123
```

### 测试端点

部署成功后，访问：
```
https://web-production-2aba.up.railway.app/health
```

应该返回：
```json
{
  "status": "healthy",
  "message": "应用运行正常",
  "game_available": true
}
```

### 测试换尿布任务

访问：
```
https://web-production-2aba.up.railway.app/diaper
```

应该看到换尿布任务页面。

---

## 🔧 Gunicorn 配置说明

### 当前配置

```bash
gunicorn main:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

**参数说明：**
- `main:app` - 指向 main.py 中的 Flask app 对象
- `--bind 0.0.0.0:$PORT` - 绑定到所有网络接口，使用 Railway 提供的端口
- `--workers 2` - 使用 2 个工作进程（适合免费套餐）
- `--timeout 120` - 请求超时时间 120 秒

### 可选优化

如果需要更高性能，可以调整：

```bash
# 更多工作进程（需要更多内存）
--workers 4

# 使用异步工作模式
--worker-class gevent --workers 2

# 调整超时时间
--timeout 300
```

---

## 🐛 常见问题

### 问题 1：部署后仍然报错

**解决方案：**
1. 确保所有文件都已提交并推送
2. 在 Railway 控制台手动触发重新部署
3. 检查 Railway 环境变量中是否有 PORT 变量

### 问题 2：应用启动但无法访问

**检查清单：**
- [ ] Railway 域名是否正确
- [ ] 应用是否监听 0.0.0.0（不是 127.0.0.1）
- [ ] 端口是否使用 $PORT 环境变量
- [ ] 防火墙设置

### 问题 3：Worker 超时

**解决方案：**
```bash
# 增加超时时间
--timeout 300

# 或使用异步 worker
--worker-class gevent
```

### 问题 4：内存不足

**解决方案：**
```bash
# 减少 worker 数量
--workers 1

# 或升级 Railway 套餐
```

---

## 📊 性能监控

### 查看应用状态

在 Railway 控制台：
1. **Metrics** - CPU、内存使用情况
2. **Logs** - 实时日志
3. **Deployments** - 部署历史

### 推荐监控指标

- **响应时间** - 应该 < 1秒
- **内存使用** - 应该 < 512MB（免费套餐限制）
- **CPU 使用** - 应该 < 80%
- **错误率** - 应该 < 1%

---

## 🎯 下一步

### 1. 立即部署

```bash
git add .
git commit -m "Fix Railway deployment - use gunicorn"
git push origin main
```

### 2. 等待部署完成

- 通常需要 2-5 分钟
- 在 Railway 控制台查看进度

### 3. 测试应用

```bash
# 健康检查
curl https://web-production-2aba.up.railway.app/health

# 换尿布任务
# 在浏览器打开
https://web-production-2aba.up.railway.app/diaper
```

### 4. 监控日志

在 Railway 控制台查看实时日志，确保没有错误。

---

## 💡 为什么使用 Gunicorn？

### Python 直接运行的问题

```bash
python main.py
```

**缺点：**
- ❌ Flask 开发服务器不适合生产环境
- ❌ 单进程，无法处理并发
- ❌ 性能差
- ❌ 不稳定

### Gunicorn 的优势

```bash
gunicorn main:app
```

**优点：**
- ✅ 生产级 WSGI 服务器
- ✅ 多进程，支持并发
- ✅ 性能好
- ✅ 稳定可靠
- ✅ 自动重启失败的 worker
- ✅ 正确处理环境变量

---

## 📚 相关文档

- [Gunicorn 官方文档](https://docs.gunicorn.org/)
- [Railway 部署指南](https://docs.railway.app/)
- [Flask 生产部署](https://flask.palletsprojects.com/en/2.3.x/deploying/)

---

## ✅ 检查清单

部署前确认：
- [x] requirements.txt 包含 gunicorn
- [x] Procfile 使用 gunicorn 启动
- [x] railway.json 配置正确
- [x] nixpacks.toml 配置正确
- [x] main.py 中有 `app = Flask(__name__)`
- [x] 所有更改已提交到 Git

部署后确认：
- [ ] Build 成功
- [ ] Deploy 成功
- [ ] /health 端点返回正常
- [ ] /diaper 页面可以访问
- [ ] 换尿布功能正常工作

---

**现在可以推送代码并重新部署了！** 🚀

```bash
git add .
git commit -m "Fix Railway PORT issue - use gunicorn"
git push origin main
```

Railway 会自动检测更改并重新部署。大约 2-5 分钟后，您的应用就可以正常访问了！
