#!/usr/bin/env python3
"""
简单的部署测试脚本
"""
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return {
        "message": "硬核育儿模拟器部署成功！",
        "status": "running",
        "port": os.environ.get("PORT", "5000")
    }

@app.route('/health')
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)