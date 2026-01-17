#!/usr/bin/env python3
"""
备用启动脚本
如果 main.py 有问题，可以使用这个文件
"""

from flask import Flask, jsonify
import os
import sys

print("=== 备用启动脚本 ===")
print(f"Python版本: {sys.version}")
print(f"当前目录: {os.getcwd()}")
print(f"PORT: {os.environ.get('PORT', '5000')}")

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': '硬核育儿模拟器 - 备用服务器',
        'status': 'running',
        'python_version': sys.version,
        'port': os.environ.get('PORT', '5000')
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'server': 'backup'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"启动备用服务器，端口: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)