#!/usr/bin/env python3
"""
完整游戏界面 - 所有任务的 Web 实现
"""

from flask import Blueprint, render_template_string, request, jsonify
from hardcore_parenting_game import HardcoreParentingGame, GameMode, BabyPersonality

# 创建 Blueprint
game_bp = Blueprint('game', __name__, url_prefix='/game')

# 创建游戏实例
game = HardcoreParentingGame()

# 主游戏页面 HTML
GAME_MAIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>硬核育儿模拟器 - 完整版</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        h1 {
            color: #333;
            font-size: 36px;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #666;
            font-size: 18px;
        }
        
        .age-groups {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .age-group {
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .age-group h2 {
            color: #667eea;
            font-size: 24px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .task-list {
            list-style: none;
        }
        
        .task-item {
            margin: 10px 0;
        }
        
        .task-btn {
            display: block;
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s;
            text-align: left;
        }
        
        .task-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .task-icon {
            font-size: 24px;
            margin-right: 10px;
        }
        
        .game-status {
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 20px;
        }
        
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .status-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        
        .status-label {
            font-size: 14px;
            color: #666;
            margin-bottom: 5px;
        }
        
        .status-value {
            font-size: 28px;
            font-weight: bold;
            color: #667eea;
        }
        
        .footer {
            background: white;
            border-radius: 20px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🍼 硬核育儿模拟器</h1>
            <p class="subtitle">体验真实的育儿挑战</p>
        </div>
        
        <div class="game-status">
            <h2>📊 游戏状态</h2>
            <div class="status-grid">
                <div class="status-item">
                    <div class="status-label">宝宝年龄</div>
                    <div class="status-value" id="babyAge">0月</div>
                </div>
                <div class="status-item">
                    <div class="status-label">清洁度</div>
                    <div class="status-value" id="cleanliness">100</div>
                </div>
                <div class="status-item">
                    <div class="status-label">快乐度</div>
                    <div class="status-value" id="happiness">100</div>
                </div>
                <div class="status-item">
                    <div class="status-label">健康值</div>
                    <div class="status-value" id="health">100</div>
                </div>
                <div class="status-item">
                    <div class="status-label">压力值</div>
                    <div class="status-value" id="stress">0</div>
                </div>
            </div>
        </div>
        
        <div class="age-groups">
            <!-- 0-3月任务 -->
            <div class="age-group">
                <h2>👶 0-3月任务</h2>
                <ul class="task-list">
                    <li class="task-item">
                        <button class="task-btn" onclick="location.href='/game/feeding'">
                            <span class="task-icon">🍼</span>冲奶粉
                        </button>
                    </li>
                    <li class="task-item">
                        <button class="task-btn" onclick="location.href='/game/sleep'">
                            <span class="task-icon">😴</span>摇晃抱哄
                        </button>
                    </li>
                    <li class="task-item">
                        <button class="task-btn" onclick="location.href='/diaper'">
                            <span class="task-icon">🧷</span>换尿布
                        </button>
                    </li>
                    <li class="task-item">
                        <button class="task-btn" onclick="location.href='/game/medicine'">
                            <span class="task-icon">💊</span>选药任务
                        </button>
                    </li>
                    <li class="task-item">
                        <button class="task-btn" onclick="location.href='/game/hug'">
                            <span class="task-icon">🤗</span>拥抱安抚
                        </button>
                    </li>
                </ul>
            </div>
            
            <!-- 3-12月任务 -->
            <div class="age-group">
                <h2>👧 3-12月任务</h2>
                <ul class="task-list">
                    <li class="task-item">
                        <button class="task-btn" onclick="location.href='/game/talk'">
                            <span class="task-icon">🗣️</span>叽里咕噜对话
                        </button>
                    </li>
                    <li class="task-item">
                        <button class="task-btn" onclick="location.href='/game/food'">
                            <span class="task-icon">🥄</span>做辅食
                        </button>
                    </li>
                    <li class="task-item">
                        <button class="task-btn" onclick="location.href='/game/safety'">
                            <span class="task-icon">⚠️</span>防摔倒QTE
                        </button>
                    </li>
                    <li class="task-item">
                        <button class="task-btn" onclick="location.href='/game/first-word'">
                            <span class="task-icon">🎤</span>叫爹妈彩蛋
                        </button>
                    </li>
                </ul>
            </div>
            
            <!-- 1-2岁任务 -->
            <div class="age-group">
                <h2>🧒 1-2岁任务</h2>
                <ul class="task-list">
                    <li class="task-item">
                        <button class="task-btn" onclick="location.href='/game/danger-touch'">
                            <span class="task-icon">⚡</span>触摸禁区
                        </button>
                    </li>
                    <li class="task-item">
                        <button class="task-btn" onclick="location.href='/game/toy-conflict'">
                            <span class="task-icon">🧸</span>玩具断案
                        </button>
                    </li>
                    <li class="task-item">
                        <button class="task-btn" onclick="location.href='/game/bad-word'">
                            <span class="task-icon">🚫</span>词汇纠正
                        </button>
                    </li>
                </ul>
            </div>
            
            <!-- 2-3岁任务 -->
            <div class="age-group">
                <h2>👦 2-3岁任务</h2>
                <ul class="task-list">
                    <li class="task-item">
                        <button class="task-btn" onclick="location.href='/game/dressing'">
                            <span class="task-icon">👕</span>出门穿衣
                        </button>
                    </li>
                    <li class="task-item">
                        <button class="task-btn" onclick="location.href='/game/emotion-talk'">
                            <span class="task-icon">💭</span>情感对话
                        </button>
                    </li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p>💡 提示：每个任务都有独特的玩法和挑战</p>
            <p>🎮 完成任务可以提升宝宝的各项数值</p>
        </div>
    </div>
    
    <script>
        // 加载游戏状态
        async function loadGameStatus() {
            try {
                const response = await fetch('/game/status');
                const data = await response.json();
                
                if (data.baby_state) {
                    document.getElementById('babyAge').textContent = data.baby_state.age + '月';
                    document.getElementById('cleanliness').textContent = Math.round(data.baby_state.cleanliness);
                    document.getElementById('happiness').textContent = Math.round(data.baby_state.happiness);
                    document.getElementById('health').textContent = Math.round(data.baby_state.health);
                    document.getElementById('stress').textContent = Math.round(data.parent_state.stress);
                }
            } catch (error) {
                console.error('加载游戏状态失败:', error);
            }
        }
        
        // 页面加载时获取状态
        loadGameStatus();
        
        // 每10秒刷新一次状态
        setInterval(loadGameStatus, 10000);
    </script>
</body>
</html>
'''


@game_bp.route('/')
def game_main():
    """游戏主页面"""
    return render_template_string(GAME_MAIN_HTML)


@game_bp.route('/status')
def game_status():
    """获取游戏状态"""
    try:
        status = game.get_game_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

