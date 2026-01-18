#!/usr/bin/env python3
"""
背景音乐 API
为 Flask 应用添加音乐控制端点
"""

from flask import Blueprint, jsonify, request
from background_music import BackgroundMusicPlayer

# 创建 Blueprint
music_bp = Blueprint('music', __name__, url_prefix='/api/music')

# 创建全局音乐播放器
music_player = BackgroundMusicPlayer()


@music_bp.route('/status', methods=['GET'])
def get_status():
    """获取音乐播放状态"""
    status = music_player.get_status()
    return jsonify(status)


@music_bp.route('/play', methods=['POST'])
def play_music():
    """
    播放音乐
    
    请求体:
    {
        "track": "music.mp3",  // 可选，不指定则播放第一首
        "loop": true           // 可选，是否循环播放
    }
    """
    data = request.get_json() or {}
    track = data.get('track')
    loop = data.get('loop', True)
    
    result = music_player.play(track, loop)
    return jsonify(result)


@music_bp.route('/pause', methods=['POST'])
def pause_music():
    """暂停音乐"""
    result = music_player.pause()
    return jsonify(result)


@music_bp.route('/resume', methods=['POST'])
def resume_music():
    """恢复播放"""
    result = music_player.resume()
    return jsonify(result)


@music_bp.route('/stop', methods=['POST'])
def stop_music():
    """停止音乐"""
    result = music_player.stop()
    return jsonify(result)


@music_bp.route('/volume', methods=['POST'])
def set_volume():
    """
    设置音量
    
    请求体:
    {
        "volume": 0.5  // 0.0 - 1.0
    }
    """
    data = request.get_json() or {}
    volume = data.get('volume', 0.5)
    
    try:
        volume = float(volume)
    except ValueError:
        return jsonify({
            "success": False,
            "message": "音量必须是数字"
        }), 400
    
    result = music_player.set_volume(volume)
    return jsonify(result)


@music_bp.route('/tracks', methods=['GET'])
def get_tracks():
    """获取可用音乐列表"""
    tracks = music_player.get_music_files()
    return jsonify({
        "success": True,
        "tracks": tracks,
        "count": len(tracks)
    })


@music_bp.route('/control-panel', methods=['GET'])
def control_panel():
    """音乐控制面板（HTML）"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>音乐控制面板</title>
        <meta charset="utf-8">
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 30px;
            }
            .status {
                background: #f8f9fa;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            .status-item {
                display: flex;
                justify-content: space-between;
                padding: 5px 0;
            }
            .controls {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
                margin-bottom: 20px;
            }
            button {
                padding: 15px;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                cursor: pointer;
                transition: all 0.3s;
            }
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .btn-play { background: #28a745; color: white; }
            .btn-pause { background: #ffc107; color: white; }
            .btn-stop { background: #dc3545; color: white; }
            .btn-resume { background: #17a2b8; color: white; }
            .volume-control {
                margin: 20px 0;
            }
            .volume-control label {
                display: block;
                margin-bottom: 10px;
                font-weight: bold;
            }
            input[type="range"] {
                width: 100%;
                height: 8px;
                border-radius: 5px;
                background: #ddd;
                outline: none;
            }
            .track-list {
                background: #f8f9fa;
                padding: 15px;
                border-radius: 10px;
                max-height: 200px;
                overflow-y: auto;
            }
            .track-item {
                padding: 10px;
                margin: 5px 0;
                background: white;
                border-radius: 5px;
                cursor: pointer;
                transition: all 0.3s;
            }
            .track-item:hover {
                background: #667eea;
                color: white;
            }
            .message {
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                text-align: center;
            }
            .message.success { background: #d4edda; color: #155724; }
            .message.error { background: #f8d7da; color: #721c24; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎵 音乐控制面板</h1>
            
            <div class="status" id="status">
                <div class="status-item">
                    <span>状态:</span>
                    <span id="playStatus">未播放</span>
                </div>
                <div class="status-item">
                    <span>当前曲目:</span>
                    <span id="currentTrack">无</span>
                </div>
                <div class="status-item">
                    <span>音量:</span>
                    <span id="volumeDisplay">50%</span>
                </div>
            </div>
            
            <div class="controls">
                <button class="btn-play" onclick="playMusic()">▶️ 播放</button>
                <button class="btn-pause" onclick="pauseMusic()">⏸️ 暂停</button>
                <button class="btn-resume" onclick="resumeMusic()">▶️ 恢复</button>
                <button class="btn-stop" onclick="stopMusic()">⏹️ 停止</button>
            </div>
            
            <div class="volume-control">
                <label>音量控制</label>
                <input type="range" min="0" max="100" value="50" id="volumeSlider" oninput="updateVolume(this.value)">
            </div>
            
            <div id="message"></div>
            
            <h3>可用音乐</h3>
            <div class="track-list" id="trackList">
                <p>加载中...</p>
            </div>
        </div>
        
        <script>
            // 更新状态
            async function updateStatus() {
                try {
                    const response = await fetch('/api/music/status');
                    const data = await response.json();
                    
                    document.getElementById('playStatus').textContent = data.is_playing ? '播放中' : '已暂停';
                    document.getElementById('currentTrack').textContent = data.current_track || '无';
                    document.getElementById('volumeDisplay').textContent = Math.round(data.volume * 100) + '%';
                    document.getElementById('volumeSlider').value = data.volume * 100;
                } catch (error) {
                    console.error('更新状态失败:', error);
                }
            }
            
            // 加载音乐列表
            async function loadTracks() {
                try {
                    const response = await fetch('/api/music/tracks');
                    const data = await response.json();
                    
                    const trackList = document.getElementById('trackList');
                    if (data.tracks.length === 0) {
                        trackList.innerHTML = '<p>没有找到音乐文件</p><p>请将音乐文件放入 music 文件夹</p>';
                    } else {
                        trackList.innerHTML = data.tracks.map(track => 
                            `<div class="track-item" onclick="playTrack('${track}')">${track}</div>`
                        ).join('');
                    }
                } catch (error) {
                    console.error('加载音乐列表失败:', error);
                }
            }
            
            // 显示消息
            function showMessage(message, type = 'success') {
                const messageDiv = document.getElementById('message');
                messageDiv.className = 'message ' + type;
                messageDiv.textContent = message;
                setTimeout(() => {
                    messageDiv.textContent = '';
                    messageDiv.className = 'message';
                }, 3000);
            }
            
            // 播放音乐
            async function playMusic(track = null) {
                try {
                    const response = await fetch('/api/music/play', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({track: track})
                    });
                    const data = await response.json();
                    showMessage(data.message, data.success ? 'success' : 'error');
                    updateStatus();
                } catch (error) {
                    showMessage('播放失败: ' + error.message, 'error');
                }
            }
            
            // 播放指定曲目
            function playTrack(track) {
                playMusic(track);
            }
            
            // 暂停音乐
            async function pauseMusic() {
                try {
                    const response = await fetch('/api/music/pause', {method: 'POST'});
                    const data = await response.json();
                    showMessage(data.message, data.success ? 'success' : 'error');
                    updateStatus();
                } catch (error) {
                    showMessage('暂停失败: ' + error.message, 'error');
                }
            }
            
            // 恢复播放
            async function resumeMusic() {
                try {
                    const response = await fetch('/api/music/resume', {method: 'POST'});
                    const data = await response.json();
                    showMessage(data.message, data.success ? 'success' : 'error');
                    updateStatus();
                } catch (error) {
                    showMessage('恢复失败: ' + error.message, 'error');
                }
            }
            
            // 停止音乐
            async function stopMusic() {
                try {
                    const response = await fetch('/api/music/stop', {method: 'POST'});
                    const data = await response.json();
                    showMessage(data.message, data.success ? 'success' : 'error');
                    updateStatus();
                } catch (error) {
                    showMessage('停止失败: ' + error.message, 'error');
                }
            }
            
            // 更新音量
            async function updateVolume(value) {
                const volume = value / 100;
                try {
                    const response = await fetch('/api/music/volume', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({volume: volume})
                    });
                    const data = await response.json();
                    document.getElementById('volumeDisplay').textContent = Math.round(volume * 100) + '%';
                } catch (error) {
                    console.error('设置音量失败:', error);
                }
            }
            
            // 初始化
            updateStatus();
            loadTracks();
            setInterval(updateStatus, 2000);  // 每2秒更新一次状态
        </script>
    </body>
    </html>
    '''
