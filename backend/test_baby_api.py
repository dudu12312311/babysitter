"""直接测试 Fal.ai Baby Generator API - 同步模式"""
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

FAL_API_KEY = os.getenv("FAL_API_KEY")

# 使用一个公开的测试图片
test_image_url = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"

payload = {
    "age_group": "baby",
    "gender": "male",
    "prompt": "a cute adorable newborn baby",
    "image_size": {"height": 512, "width": 512},
    "num_images": 1,
    "output_format": "png",
    "mother_image_urls": [test_image_url],
    "father_image_urls": [test_image_url],
    "father_weight": 0.5
}

headers = {
    "Authorization": f"Key {FAL_API_KEY}",
    "Content-Type": "application/json"
}

print("测试 Baby Generator API (同步模式)...")

# 使用同步 API (fal.run 而不是 queue.fal.run)
url = "https://fal.run/half-moon-ai/ai-baby-and-aging-generator/multi"
print(f"URL: {url}")

with httpx.Client(timeout=120.0, proxy=None, trust_env=False) as client:
    response = client.post(url, json=payload, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text[:1000]}")
