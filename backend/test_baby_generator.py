"""
测试宝宝图片生成接口 - 多场景批量生成
返回格式: {场景描述: 图片链接}
"""
import asyncio
import base64
import os
import json
from dotenv import load_dotenv

load_dotenv()

from app.services.baby_generator import BabyImageGenerator

async def test_generate_scenes():
    """测试批量生成多场景婴儿图片"""
    
    generator = BabyImageGenerator()
    
    # 使用 zjm.jpg 测试
    test_image_path = "../public/sample-photos/zjm.jpg"
    
    if not os.path.exists(test_image_path):
        print(f"错误: 找不到测试图片 {test_image_path}")
        return
    
    with open(test_image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()
    
    photos = [{
        "data": image_data,
        "content_type": "image/jpeg"
    }]
    
    print("使用 zjm.jpg 测试批量场景生成...")
    print("="*50)
    
    # 只生成换尿布相关的两个场景
    scenes_to_generate = ["wet_diaper_crying", "diaper_change_happy"]
    
    results = await generator.generate_scenes(photos, "male", scenes_to_generate)
    
    print("\n" + "="*50)
    print("生成结果 (JSON格式):")
    print("="*50)
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    print("\n" + "="*50)
    print("图片链接:")
    print("="*50)
    for scene, url in results.items():
        print(f"\n{scene}:")
        print(f"  {url}")

if __name__ == "__main__":
    asyncio.run(test_generate_scenes())
