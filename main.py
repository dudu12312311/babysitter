from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>硬核育儿模拟器</h1>
    <p>游戏正在运行中...</p>
    <p>端口: {}</p>
    <p>状态: 健康</p>
    '''.format(os.environ.get('PORT', '5000'))

@app.route('/health')
def health():
    return {'status': 'healthy', 'message': '应用运行正常'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"启动应用，端口: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)