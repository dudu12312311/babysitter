#!/usr/bin/env python3
"""
换尿布任务 - 带视觉反馈
点击任务显示哭脸，成功后显示笑脸
"""

from flask import Blueprint, render_template_string, request, jsonify
from hardcore_parenting_game import HardcoreParentingGame

# 创建 Blueprint
diaper_bp = Blueprint('diaper', __name__, url_prefix='/diaper')

# 创建游戏实例
game = HardcoreParentingGame()

# 换尿布任务HTML模板
DIAPER_TASK_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>换尿布任务 - 硬核育儿模拟器</title>
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
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 30px;
            padding: 40px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 32px;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
        }
        
        .baby-face {
            width: 200px;
            height: 200px;
            margin: 30px auto;
            font-size: 150px;
            line-height: 200px;
            transition: all 0.5s ease;
            animation: bounce 1s ease-in-out;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
        
        .crying {
            animation: shake 0.5s ease-in-out infinite;
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
        
        .status-text {
            font-size: 24px;
            font-weight: bold;
            margin: 20px 0;
            min-height: 30px;
        }
        
        .status-text.crying {
            color: #dc3545;
        }
        
        .status-text.happy {
            color: #28a745;
        }
        
        .task-controls {
            margin: 30px 0;
        }
        
        .control-group {
            margin: 20px 0;
            text-align: left;
        }
        
        .control-group label {
            display: block;
            margin-bottom: 10px;
            font-weight: bold;
            color: #333;
        }
        
        .slider-container {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        input[type="range"] {
            flex: 1;
            height: 8px;
            border-radius: 5px;
            background: #ddd;
            outline: none;
            -webkit-appearance: none;
        }
        
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #667eea;
            cursor: pointer;
        }
        
        input[type="range"]::-moz-range-thumb {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #667eea;
            cursor: pointer;
            border: none;
        }
        
        .value-display {
            min-width: 60px;
            text-align: center;
            font-weight: bold;
            color: #667eea;
        }
        
        select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
            background: white;
            cursor: pointer;
        }
        
        select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn {
            padding: 15px 40px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s;
            margin: 10px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5568d3;
        }
        
        .btn-success {
            background: #28a745;
            color: white;
        }
        
        .btn-success:hover {
            background: #218838;
        }
        
        .btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .result-message {
            margin: 20px 0;
            padding: 15px;
            border-radius: 10px;
            font-size: 16px;
            line-height: 1.6;
        }
        
        .result-message.success {
            background: #d4edda;
            color: #155724;
            border: 2px solid #c3e6cb;
        }
        
        .result-message.error {
            background: #f8d7da;
            color: #721c24;
            border: 2px solid #f5c6cb;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin: 20px 0;
        }
        
        .stat-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
        }
        
        .stat-label {
            font-size: 14px;
            color: #666;
            margin-bottom: 5px;
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }
        
        .hidden {
            display: none;
        }
        
        .instructions {
            background: #e3f2fd;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: left;
        }
        
        .instructions h3 {
            color: #1976d2;
            margin-bottom: 10px;
        }
        
        .instructions ol {
            margin-left: 20px;
        }
        
        .instructions li {
            margin: 8px 0;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🍼 换尿布任务</h1>
        <p class="subtitle">帮助宝宝换上干净的尿布</p>
        
        <!-- 宝宝表情 -->
        <div class="baby-face" id="babyFace">😭</div>
        <div class="status-text crying" id="statusText">宝宝不舒服，需要换尿布！</div>
        
        <!-- 说明 -->
        <div class="instructions" id="instructions">
            <h3>📝 任务说明</h3>
            <ol>
                <li>调整提腿速度（越快越好，但不要太慢）</li>
                <li>设置擦拭彻底度（至少5次以上）</li>
                <li>选择正确的尿布放置顺序</li>
                <li>点击"开始换尿布"完成任务</li>
            </ol>
        </div>
        
        <!-- 任务控制 -->
        <div class="task-controls" id="taskControls">
            <div class="control-group">
                <label>⏱️ 提腿速度（秒）</label>
                <div class="slider-container">
                    <input type="range" id="liftSpeed" min="1" max="10" value="3" step="0.5">
                    <span class="value-display" id="liftSpeedValue">3.0秒</span>
                </div>
                <small style="color: #666;">建议: 3-4秒（太慢可能触发喷射袭击！）</small>
            </div>
            
            <div class="control-group">
                <label>🧻 擦拭彻底度（次数）</label>
                <div class="slider-container">
                    <input type="range" id="wipeThoroughness" min="1" max="10" value="7">
                    <span class="value-display" id="wipeThoroughnessValue">7次</span>
                </div>
                <small style="color: #666;">建议: 7-9次（太少不干净，太多浪费时间）</small>
            </div>
            
            <div class="control-group">
                <label>👶 尿布放置顺序</label>
                <select id="diaperPlacement">
                    <option value="correct">✅ 正确：先擦拭再穿新尿布</option>
                    <option value="wrong_order">❌ 错误：没擦就穿新尿布</option>
                </select>
            </div>
            
            <button class="btn btn-primary" onclick="startDiaperChange()">
                🚀 开始换尿布
            </button>
        </div>
        
        <!-- 结果显示 -->
        <div id="resultContainer" class="hidden">
            <div class="result-message" id="resultMessage"></div>
            
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-label">清洁度变化</div>
                    <div class="stat-value" id="cleanlinessChange">+0</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">快乐度变化</div>
                    <div class="stat-value" id="happinessChange">+0</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">健康值变化</div>
                    <div class="stat-value" id="healthChange">+0</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">压力值变化</div>
                    <div class="stat-value" id="stressChange">+0</div>
                </div>
            </div>
            
            <button class="btn btn-success" onclick="resetTask()">
                🔄 再来一次
            </button>
        </div>
    </div>
    
    <script>
        // 更新滑块显示值
        document.getElementById('liftSpeed').addEventListener('input', function(e) {
            document.getElementById('liftSpeedValue').textContent = e.target.value + '秒';
        });
        
        document.getElementById('wipeThoroughness').addEventListener('input', function(e) {
            document.getElementById('wipeThoroughnessValue').textContent = e.target.value + '次';
        });
        
        // 开始换尿布
        async function startDiaperChange() {
            const liftSpeed = parseFloat(document.getElementById('liftSpeed').value);
            const wipeThoroughness = parseInt(document.getElementById('wipeThoroughness').value);
            const diaperPlacement = document.getElementById('diaperPlacement').value;
            
            // 隐藏控制面板
            document.getElementById('instructions').classList.add('hidden');
            document.getElementById('taskControls').classList.add('hidden');
            
            // 显示处理中
            document.getElementById('statusText').textContent = '正在换尿布...';
            document.getElementById('statusText').className = 'status-text';
            
            try {
                const response = await fetch('/diaper/execute', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        lift_speed: liftSpeed,
                        wipe_thoroughness: wipeThoroughness,
                        diaper_placement: diaperPlacement
                    })
                });
                
                const result = await response.json();
                
                // 更新宝宝表情
                const babyFace = document.getElementById('babyFace');
                const statusText = document.getElementById('statusText');
                
                if (result.success) {
                    // 成功 - 显示笑脸
                    babyFace.textContent = '😊';
                    babyFace.className = 'baby-face';
                    statusText.textContent = '太棒了！宝宝舒服多了！';
                    statusText.className = 'status-text happy';
                } else {
                    // 失败 - 继续哭脸
                    babyFace.textContent = '😭';
                    babyFace.className = 'baby-face crying';
                    statusText.textContent = '哎呀，出问题了...';
                    statusText.className = 'status-text crying';
                }
                
                // 显示结果
                displayResult(result);
                
            } catch (error) {
                console.error('Error:', error);
                alert('执行任务时出错: ' + error.message);
            }
        }
        
        // 显示结果
        function displayResult(result) {
            const resultContainer = document.getElementById('resultContainer');
            const resultMessage = document.getElementById('resultMessage');
            
            // 设置消息
            resultMessage.textContent = result.message;
            resultMessage.className = 'result-message ' + (result.success ? 'success' : 'error');
            
            // 更新数值变化
            const changes = result.state_changes || {};
            document.getElementById('cleanlinessChange').textContent = 
                (changes.cleanliness > 0 ? '+' : '') + (changes.cleanliness || 0);
            document.getElementById('happinessChange').textContent = 
                (changes.happiness > 0 ? '+' : '') + (changes.happiness || 0);
            document.getElementById('healthChange').textContent = 
                (changes.health > 0 ? '+' : '') + (changes.health || 0);
            document.getElementById('stressChange').textContent = 
                (changes.parent_stress > 0 ? '+' : '') + (changes.parent_stress || 0);
            
            // 显示结果容器
            resultContainer.classList.remove('hidden');
        }
        
        // 重置任务
        function resetTask() {
            // 重置表情
            document.getElementById('babyFace').textContent = '😭';
            document.getElementById('babyFace').className = 'baby-face crying';
            document.getElementById('statusText').textContent = '宝宝不舒服，需要换尿布！';
            document.getElementById('statusText').className = 'status-text crying';
            
            // 重置控制
            document.getElementById('liftSpeed').value = 3;
            document.getElementById('liftSpeedValue').textContent = '3.0秒';
            document.getElementById('wipeThoroughness').value = 7;
            document.getElementById('wipeThoroughnessValue').textContent = '7次';
            document.getElementById('diaperPlacement').value = 'correct';
            
            // 显示控制面板
            document.getElementById('instructions').classList.remove('hidden');
            document.getElementById('taskControls').classList.remove('hidden');
            document.getElementById('resultContainer').classList.add('hidden');
        }
    </script>
</body>
</html>
'''


@diaper_bp.route('/')
def diaper_task():
    """换尿布任务主页面"""
    return render_template_string(DIAPER_TASK_HTML)


@diaper_bp.route('/execute', methods=['POST'])
def execute_diaper_task():
    """执行换尿布任务"""
    try:
        data = request.get_json()
        
        lift_speed = data.get('lift_speed', 3.0)
        wipe_thoroughness = data.get('wipe_thoroughness', 7)
        diaper_placement = data.get('diaper_placement', 'correct')
        
        # 执行任务
        result = game.execute_diaper_task(
            lift_speed=lift_speed,
            wipe_thoroughness=wipe_thoroughness,
            diaper_placement=diaper_placement
        )
        
        # 返回结果
        return jsonify({
            'success': result.success,
            'message': result.message,
            'state_changes': result.state_changes,
            'special_effects': result.special_effects
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'执行失败: {str(e)}',
            'state_changes': {},
            'special_effects': []
        }), 500
