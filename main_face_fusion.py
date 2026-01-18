#!/usr/bin/env python3
"""
宝宝面部融合 - 主应用
上传父母照片，生成宝宝照片
"""

from flask import Flask, render_template_string
import os

# 导入面部融合 API
try:
    from baby_face_fusion_api import baby_fusion_bp
    fusion_api_available = True
    print("✓ 成功导入宝宝面部融合模块")
except ImportError as e:
    print(f"✗ 导入面部融合模块失败: {e}")
    fusion_api_available = False

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上传文件大小为 16MB

# 注册面部融合 API
if fusion_api_available:
    app.register_blueprint(baby_fusion_bp)
    print("✓ 宝宝面部融合 API 已注册")

@app.route('/')
def home():
    """首页"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>宝宝面部融合生成器</title>
        <meta charset="utf-8">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 40px 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 10px;
            }
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
            }
            .feature-list {
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
            }
            .feature-list h3 {
                color: #667eea;
                margin-top: 0;
            }
            .feature-list ul {
                list-style: none;
                padding: 0;
            }
            .feature-list li {
                padding: 8px 0;
                padding-left: 25px;
                position: relative;
            }
            .feature-list li:before {
                content: "✓";
                position: absolute;
                left: 0;
                color: #667eea;
                font-weight: bold;
            }
            .api-list {
                background: #e3f2fd;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
            }
            .api-list h3 {
                color: #1976d2;
                margin-top: 0;
            }
            .api-list a {
                display: block;
                padding: 10px;
                margin: 5px 0;
                background: white;
                border-radius: 5px;
                text-decoration: none;
                color: #1976d2;
                transition: all 0.3s;
            }
            .api-list a:hover {
                background: #1976d2;
                color: white;
                transform: translateX(5px);
            }
            .status {
                text-align: center;
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
            }
            .status.success {
                background: #d4edda;
                color: #155724;
            }
            .status.error {
                background: #f8d7da;
                color: #721c24;
            }
            .btn {
                display: inline-block;
                padding: 12px 30px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 25px;
                margin: 10px 5px;
                transition: all 0.3s;
            }
            .btn:hover {
                background: #764ba2;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .btn-center {
                text-align: center;
                margin: 30px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🍼 宝宝面部融合生成器</h1>
            <p class="subtitle">上传父母照片，AI 预测宝宝长相</p>
            
            <div class="status ''' + ('success' if fusion_api_available else 'error') + '''">
                ''' + ('✓ 系统就绪，可以开始使用' if fusion_api_available else '✗ 面部融合模块未加载') + '''
            </div>
            
            <div class="feature-list">
                <h3>✨ 功能特点</h3>
                <ul>
                    <li>上传 1-2 张父母照片</li>
                    <li>AI 分析面部特征</li>
                    <li>生成预测的宝宝照片</li>
                    <li>支持不同年龄阶段（新生儿、6个月、1岁、2岁）</li>
                    <li>一次生成 1-4 张变体</li>
                    <li>纯正中国宝宝特征</li>
                </ul>
            </div>
            
            <div class="api-list">
                <h3>🔗 API 端点</h3>
                <a href="/api/baby-fusion/health">📊 健康检查</a>
                <a href="/api/baby-fusion/test-upload">🧪 测试上传表单</a>
            </div>
            
            <div class="btn-center">
                <a href="/api/baby-fusion/test-upload" class="btn">🎨 开始生成宝宝照片</a>
            </div>
            
            <div class="feature-list">
                <h3>📝 使用说明</h3>
                <ul>
                    <li>点击上方按钮进入上传页面</li>
                    <li>选择父母照片（建议正面清晰照片）</li>
                    <li>选择宝宝年龄和生成数量</li>
                    <li>点击生成，等待 10-20 秒</li>
                    <li>查看生成的宝宝照片</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("\n" + "=" * 60)
    print("宝宝面部融合生成器")
    print("=" * 60)
    print(f"启动应用，端口: {port}")
    print(f"访问: http://localhost:{port}")
    print(f"测试上传: http://localhost:{port}/api/baby-fusion/test-upload")
    print("=" * 60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)
