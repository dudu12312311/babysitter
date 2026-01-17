#!/usr/bin/env python3
"""
Railway 部署测试文件
用于验证部署配置是否正确
"""

import os
import sys
from flask import Flask, jsonify

print("=== Railway 部署测试 ===")
print(f"Python 版本: {sys.version}")
print(f"当前工作目录: {os.getcwd()}")
print(f"环境变量 PORT: {os.environ.get('PORT', '未设置')}")

# 列出当前目录文件
print("\n当前目录文件:")
for file in os.listdir('.'):
    print(f"  - {file}")

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': 'Railway 部署测试成功',
        'python_version': sys.version,
        'port': os.environ.get('PORT', '5000'),
        'files': os.listdir('.')
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n启动测试服务器，端口: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)