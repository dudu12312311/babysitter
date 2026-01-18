# 修复 PORT 错误指南

## 问题
```
Error: Invalid value for '--port': '$PORT' is not a valid integer.
```

## 原因
Railway 的 PORT 环境变量没有正确传递给 Python 应用。

## 解决方案：使用 Gunicorn

### 步骤1：在 GitHub 上更新 requirements.txt

1. 访问：https://github.com/dudu12312311/babysitter
2. 点击 `requirements.txt` 文件
3. 点击铅笔图标编辑
4. 修改内容为：
```
Flask==2.3.3
gunicorn==21.2.0
```
5. 提交更改

### 步骤2：更新 nixpacks.toml

1. 点击 `nixpacks.toml` 文件
2. 点击铅笔图标编辑
3. 修改内容为：
```toml
[phases.setup]
nixPkgs = ["python311", "pip"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "gunicorn main:app --bind 0.0.0.0:$PORT"
```
4. 提交更改

### 步骤3：等待 Railway 重新部署

- GitHub 更新后，Railway 会自动检测
- 等待 1-2 分钟
- 查看部署日志

### 步骤4：验证

访问：
- `https://你的应用.railway.app/health`
- 应该返回：`{"status": "healthy"}`

## 为什么使用 Gunicorn？

- ✅ Gunicorn 是生产级 WSGI 服务器
- ✅ 正确处理 Railway 的 PORT 环境变量
- ✅ 比 Flask 内置服务器更稳定
- ✅ Railway 官方推荐

## 如果还是失败

尝试在 Railway 控制台直接设置启动命令：
```
gunicorn main:app --bind 0.0.0.0:$PORT
```
