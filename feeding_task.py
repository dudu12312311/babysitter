#!/usr/bin/env python3
"""
冲奶粉任务 - Web 界面
"""

from flask import Blueprint, render_template_string, request, jsonify
from hardcore_parenting_game import HardcoreParentingGame

feeding_bp = Blueprint('feeding', __name__, url_prefix='/game/feeding')
game = HardcoreParentingGame()

FEEDING_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>🍼 冲奶粉任务</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
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
        }
        h1 { color: #333; text-align: center; margin-bottom: 30px; }
        .baby-face {
            width: 150px;
            height: 150px;
            margin: 20px auto;
            font-size: 120px;
            text-align: center;
            line-height: 150px;
        }
        .control-group {
            margin: 20px 0;
        }
        label {
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
        }
        .value-display {
            min-width: 80px;
            text-align: center;
            font-weight: bold;
            color: #667eea;
            font-size: 18px;
        }
        .btn {
            width: 100%;
            padding: 15px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s;
            margin: 10px 0;
        }
        .btn-primary {
            background: #667eea;
            color: white;
        }
        .btn-primary:hover {
            background: #5568d3;
            transform: translateY(-2px);
        }
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        .result-message {
            margin: 20px 0;
            padding: 15px;
            border-radius: 10px;
            display: none;
        }
        .result-message.success {
            background: #d4edda;
            color: #155724;
        }
        .result-message.error {
            background: #f8d7da;
            color: #721c24;
        }
        .hidden { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🍼 冲奶粉任务</h1>
        <div class="baby-face" id="babyFace">😭</div>
        
        <div id="controls">
            <div class="control-group">
                <label>🌡️ 水温（°C）</label>
                <div class="slider-container">
                    <input type="range" id="waterTemp" min="30" max="60" value="40" step="1">
                    <span class="value-display" id="waterTempValue">40°C</span>
                </div>
                <small>建议：37-42°C</small>
            </div>
            
            <div class="control-group">
                <label>🔄 摇晃强度（次）</label>
                <div class="slider-container">
                    <input type="range" id="shakeIntensity" min="1" max="20" value="10">
                    <span class="value-display" id="shakeIntensityValue">10次</span>
                </div>
                <small>建议：8-12次</small>
            </div>
            
            <div class="control-group">
                <label>📐 倾斜角度（度）</label>
                <div class="slider-container">
                    <input type="range" id="tiltAngle" min="0" max="90" value="45">
                    <span class="value-display" id="tiltAngleValue">45°</span>
                </div>
                <small>建议：40-50度</small>
            </div>
            
            <button class="btn btn-primary" onclick="startFeeding()">🚀 开始冲奶</button>
            <button class="btn btn-secondary" onclick="location.href='/game'">返回主页</button>
        </div>
        
        <div id="result" class="hidden">
            <div class="result-message" id="resultMessage"></div>
            <button class="btn btn-primary" onclick="resetTask()">🔄 再来一次</button>
            <button class="btn btn-secondary" onclick="location.href='/game'">返回主页</button>
        </div>
    </div>
    
    <script>
        document.getElementById('waterTemp').addEventListener('input', function(e) {
            document.getElementById('waterTempValue').textContent = e.target.value + '°C';
        });
        
        document.getElementById('shakeIntensity').addEventListener('input', function(e) {
            document.getElementById('shakeIntensityValue').textContent = e.target.value + '次';
        });
        
        document.getElementById('tiltAngle').addEventListener('input', function(e) {
            document.getElementById('tiltAngleValue').textContent = e.target.value + '°';
        });
        
        async function startFeeding() {
            const waterTemp = parseFloat(document.getElementById('waterTemp').value);
            const shakeIntensity = parseInt(document.getElementById('shakeIntensity').value);
            const tiltAngle = parseInt(document.getElementById('tiltAngle').value);
            
            try {
                const response = await fetch('/game/feeding/execute', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ water_temp: waterTemp, shake_intensity: shakeIntensity, tilt_angle: tiltAngle })
                });
                
                const result = await response.json();
                
                document.getElementById('babyFace').textContent = result.success ? '😊' : '😭';
                document.getElementById('resultMessage').textContent = result.message;
                document.getElementById('resultMessage').className = 'result-message ' + (result.success ? 'success' : 'error');
                document.getElementById('resultMessage').style.display = 'block';
                
                document.getElementById('controls').classList.add('hidden');
                document.getElementById('result').classList.remove('hidden');
            } catch (error) {
                alert('执行任务时出错: ' + error.message);
            }
        }
        
        function resetTask() {
            document.getElementById('babyFace').textContent = '😭';
            document.getElementById('waterTemp').value = 40;
            document.getElementById('waterTempValue').textContent = '40°C';
            document.getElementById('shakeIntensity').value = 10;
            document.getElementById('shakeIntensityValue').textContent = '10次';
            document.getElementById('tiltAngle').value = 45;
            document.getElementById('tiltAngleValue').textContent = '45°';
            document.getElementById('controls').classList.remove('hidden');
            document.getElementById('result').classList.add('hidden');
        }
    </script>
</body>
</html>
'''

@feeding_bp.route('/')
def feeding_task():
    return render_template_string(FEEDING_HTML)

@feeding_bp.route('/execute', methods=['POST'])
def execute_feeding():
    try:
        data = request.get_json()
        result = game.execute_feeding_task(
            water_temp=data.get('water_temp', 40),
            shake_intensity=data.get('shake_intensity', 10),
            tilt_angle=data.get('tilt_angle', 45)
        )
        return jsonify({
            'success': result.success,
            'message': result.message,
            'state_changes': result.state_changes
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
