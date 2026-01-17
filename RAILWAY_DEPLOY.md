# Railway 部署指南

## 当前配置

### 文件结构
- `main.py` - 主应用入口
- `start.py` - 备用启动脚本
- `test_deploy.py` - 部署测试脚本
- `requirements.txt` - Python 依赖
- `runtime.txt` - Python 版本
- `Procfile` - Heroku 兼容启动配置
- `railway.json` - Railway 特定配置
- `nixpacks.toml` - Nixpacks 构建配置

### 启动命令优先级
1. `railway.json` 中的 `startCommand`
2. `nixpacks.toml` 中的 `[start].cmd`
3. `Procfile` 中的 `web` 命令

### 健康检查
- 路径: `/health`
- 超时: 300秒
- 重试: 最多10次

## 部署步骤

1. **连接 GitHub 仓库**
   - 仓库: `https://github.com/dudu12312311/babysitter.git`
   - 分支: `main`

2. **Railway 配置**
   - 构建器: Nixpacks
   - 启动命令: `python main.py`
   - 健康检查: `/health`

3. **环境变量**
   - `PORT` - 自动设置
   - 其他变量根据需要添加

## 故障排除

### 如果 main.py 启动失败
1. 修改 `railway.json` 中的 `startCommand` 为 `python start.py`
2. 或修改 `nixpacks.toml` 中的启动命令

### 如果健康检查失败
1. 检查 `/health` 端点是否正常响应
2. 增加健康检查超时时间
3. 查看部署日志

### 调试命令
```bash
# 本地测试
python main.py
python start.py
python test_deploy.py

# 检查依赖
pip install -r requirements.txt
```

## 当前状态
- ✅ 配置文件已更新
- ✅ 启动命令已修正
- ✅ 健康检查已配置
- ⏳ 等待推送到 GitHub
- ⏳ 等待 Railway 重新部署