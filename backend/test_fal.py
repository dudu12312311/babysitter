"""测试 Fal.ai API 连接"""
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

FAL_API_KEY = os.getenv("FAL_API_KEY")
print(f"API Key: {FAL_API_KEY[:20]}..." if FAL_API_KEY else "API Key: 未设置")

# 测试简单的文本生成图像 API
url = "https://fal.run/fal-ai/fast-sdxl"

headers = {
    "Authorization": f"Key {FAL_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "prompt": "a cute baby, portrait photo",
    "image_size": "square",
    "num_images": 1
}

print(f"\n测试 Fal.ai API...")
print(f"URL: {url}")

try:
    # 显式禁用代理
    with httpx.Client(timeout=60.0, proxy=None, trust_env=False) as client:
        response = client.post(url, json=payload, headers=headers)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text[:500]}")
except Exception as e:
    import traceback
    print(f"错误: {type(e).__name__}: {e}")
    traceback.print_exc()
