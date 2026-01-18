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

# 导入换尿布任务
try:
    from diaper_change_task import diaper_bp
    diaper_task_available = True
    print("成功导入换尿布任务模块")
except ImportError as e:
    print(f"导入换尿布任务失败: {e}")
    diaper_task_available = False

print("开始启动应用...")
print(f"Python版本: {sys.version}")
print(f"当前工作目录: {os.getcwd()}")

app = Flask(__name__)

# 注册换尿布任务 Blueprint
if diaper_task_available:
    app.register_blueprint(diaper_bp)
    print("换尿布任务已注册")

# 创建游戏实例
if game_available:
    game = HardcoreParentingGame()
    print("游戏实例创建成功")
else:
    game = None

@app.route('/')
def home():
    diaper_link = '<li><a href="/diaper">🍼 换尿布任务</a> - 互动游戏</li>' if diaper_task_available else ''
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>硬核育儿模拟器</title>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }}
            .container {{
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }}
            h1 {{
                color: #333;
                text-align: center;
            }}
            .status {{
                background: #d4edda;
                color: #155724;
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
                text-align: center;
            }}
            ul {{
                list-style: none;
                padding: 0;
            }}
            li {{
                margin: 10px 0;
            }}
            a {{
                display: block;
                padding: 15px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 10px;
                transition: all 0.3s;
            }}
            a:hover {{
                background: #5568d3;
                transform: translateX(5px);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🍼 硬核育儿模拟器</h1>
            <div class="status">
                <p>✅ 应用运行正常</p>
                <p>端口: {os.environ.get('PORT', '5000')}</p>
                <p>游戏模块: {"可用" if game_available else "不可用"}</p>
                <p>换尿布任务: {"可用" if diaper_task_available else "不可用"}</p>
            </div>
            <h2>🎮 游戏任务</h2>
            <ul>
                {diaper_link}
            </ul>
            <h2>📡 API 端点</h2>
            <ul>
                <li><a href="/health">/health</a> - 健康检查</li>
                <li><a href="/game/status">/game/status</a> - 游戏状态</li>
            </ul>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'message': '应用运行正常',
        'game_available': game_available
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
        
        # 转换枚举
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
        # 演示游戏功能
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