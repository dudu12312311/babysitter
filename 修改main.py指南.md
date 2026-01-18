# 修改 main.py 添加宝宝照片功能

## 🎯 目标

在现有的 `main.py` 中添加宝宝照片生成功能。

## 📝 修改步骤

### 步骤 1: 在 main.py 顶部添加导入

在 `main.py` 的导入部分添加：

```python
# 在现有导入后添加
try:
    from baby_photo_api import baby_photo_bp
    photo_api_available = True
    print("成功导入宝宝照片生成模块")
except ImportError as e:
    print(f"导入宝宝照片模块失败: {e}")
    photo_api_available = False
```

### 步骤 2: 注册 Blueprint

在创建 Flask app 后，添加 Blueprint 注册：

```python
app = Flask(__name__)

# 注册宝宝照片生成 API
if photo_api_available:
    app.register_blueprint(baby_photo_bp)
    print("宝宝照片生成 API 已注册")
```

### 步骤 3: 更新首页显示

修改 `home()` 函数，添加照片 API 端点：

```python
@app.route('/')
def home():
    api_endpoints = '''
    <h2>API 端点:</h2>
    <ul>
        <li><a href="/health">/health</a> - 健康检查</li>
        <li><a href="/game/status">/game/status</a> - 游戏状态</li>
        <li>/game/start - 开始游戏 (POST)</li>
    '''
    
    # 如果照片 API 可用，添加相关端点
    if photo_api_available:
        api_endpoints += '''
        <li><a href="/api/baby-photo/health">/api/baby-photo/health</a> - 照片功能状态</li>
        <li>/api/baby-photo/generate - 生成宝宝照片 (POST)</li>
        <li>/api/baby-photo/preview-prompt - 预览提示词 (POST)</li>
        '''
    
    api_endpoints += '</ul>'
    
    return f'''
    <h1>硬核育儿模拟器</h1>
    <p>游戏正在运行中...</p>
    <p>端口: {os.environ.get('PORT', '5000')}</p>
    <p>状态: 健康</p>
    <p>游戏模块: {"可用" if game_available else "不可用"}</p>
    <p>照片生成: {"可用" if photo_api_available else "不可用"}</p>
    <br>
    {api_endpoints}
    '''
```

## 📄 完整的修改后的 main.py

```python
from flask import Flask, jsonify, request
import os
import sys

# 导入游戏逻辑
try:
    from hardcore_parenting_game import HardcoreParentingGame, GameMode, BabyPersonality
    game_available = True
    print("成功导入游戏模块")
except ImportError as e:
    print(f"导入游戏模块失败: {e}")
    game_available = False

# 导入宝宝照片生成模块
try:
    from baby_photo_api import baby_photo_bp
    photo_api_available = True
    print("成功导入宝宝照片生成模块")
except ImportError as e:
    print(f"导入宝宝照片模块失败: {e}")
    photo_api_available = False

print("开始启动应用...")
print(f"Python版本: {sys.version}")
print(f"当前工作目录: {os.getcwd()}")

app = Flask(__name__)

# 注册宝宝照片生成 API
if photo_api_available:
    app.register_blueprint(baby_photo_bp)
    print("宝宝照片生成 API 已注册")

# 创建游戏实例
if game_available:
    game = HardcoreParentingGame()
    print("游戏实例创建成功")
else:
    game = None

@app.route('/')
def home():
    api_endpoints = '''
    <h2>API 端点:</h2>
    <ul>
        <li><a href="/health">/health</a> - 健康检查</li>
        <li><a href="/game/status">/game/status</a> - 游戏状态</li>
        <li>/game/start - 开始游戏 (POST)</li>
    '''
    
    if photo_api_available:
        api_endpoints += '''
        <li><a href="/api/baby-photo/health">/api/baby-photo/health</a> - 照片功能状态</li>
        <li>/api/baby-photo/generate - 生成宝宝照片 (POST)</li>
        <li>/api/baby-photo/preview-prompt - 预览提示词 (POST)</li>
        '''
    
    api_endpoints += '</ul>'
    
    return f'''
    <h1>硬核育儿模拟器</h1>
    <p>游戏正在运行中...</p>
    <p>端口: {os.environ.get('PORT', '5000')}</p>
    <p>状态: 健康</p>
    <p>游戏模块: {"可用" if game_available else "不可用"}</p>
    <p>照片生成: {"可用" if photo_api_available else "不可用"}</p>
    <br>
    {api_endpoints}
    '''

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'message': '应用运行正常',
        'game_available': game_available,
        'photo_api_available': photo_api_available
    })

@app.route('/game/status')
def game_status():
    if not game_available:
        return jsonify({'error': '游戏模块不可用'})
    
    try:
        status = game.get_game_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': f'获取游戏状态失败: {str(e)}'})

@app.route('/game/start', methods=['POST'])
def start_game():
    if not game_available:
        return jsonify({'error': '游戏模块不可用'})
    
    try:
        data = request.get_json() or {}
        mode_str = data.get('mode', 'intern_parent')
        personality_str = data.get('personality', 'chill_angel')
        age = data.get('age', 0)
        
        mode = GameMode(mode_str)
        personality = BabyPersonality(personality_str)
        
        result = game.start_game(mode, personality, age)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'开始游戏失败: {str(e)}'})

@app.route('/game/demo')
def game_demo():
    if not game_available:
        return jsonify({'error': '游戏模块不可用'})
    
    try:
        result = game.start_game(GameMode.NORMAL, BabyPersonality.ANGEL, 0)
        status = game.get_game_status()
        
        return jsonify({
            'demo': '游戏演示',
            'start_result': result,
            'current_status': status
        })
    except Exception as e:
        return jsonify({'error': f'游戏演示失败: {str(e)}'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"启动应用，端口: {port}")
    print("应用启动完成，等待请求...")
    app.run(host='0.0.0.0', port=port, debug=False)
```

## 🧪 测试步骤

### 1. 本地测试

```bash
# 设置 API 密钥
set FAL_KEY=your_api_key_here

# 启动应用
python main.py
```

### 2. 访问首页

打开浏览器访问 `http://localhost:5000`，应该看到：
- 照片生成: 可用

### 3. 测试照片功能状态

访问 `http://localhost:5000/api/baby-photo/health`

应该返回：
```json
{
  "status": "healthy",
  "fal_client_installed": true,
  "api_key_configured": true
}
```

### 4. 测试生成照片

使用 Postman 或 curl：

```bash
curl -X POST http://localhost:5000/api/baby-photo/generate ^
  -H "Content-Type: application/json" ^
  -d "{\"age_months\": 6, \"gender\": \"boy\", \"expression\": \"happy\", \"scene\": \"studio\"}"
```

## ⚠️ 注意事项

1. **确保已安装依赖**
   ```bash
   pip install fal-client
   ```

2. **设置环境变量**
   - 必须设置 `FAL_KEY` 环境变量
   - 或在代码中直接传入 API 密钥

3. **文件位置**
   - 确保所有新文件与 `main.py` 在同一目录
   - `chinese_baby_prompts.py`
   - `baby_photo_integration.py`
   - `baby_photo_api.py`

4. **错误处理**
   - 如果照片模块导入失败，应用仍可正常运行
   - 只是照片功能不可用

## 🚀 部署到 Railway

如果要部署到 Railway，需要：

1. **更新 requirements.txt**
   ```
   Flask==2.3.3
   fal-client
   ```

2. **在 Railway 设置环境变量**
   - 在 Railway 项目设置中添加 `FAL_KEY`

3. **推送代码到 GitHub**
   ```bash
   git add .
   git commit -m "添加宝宝照片生成功能"
   git push
   ```

---

**完成！现在你的应用已经集成了中国宝宝照片生成功能。** 🎉
