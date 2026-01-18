"""
测试婴儿初始化接口 - 生成3张场景图片
"""
import asyncio
import base64
import os
import json
from dotenv import load_dotenv

load_dotenv()

from app.services.baby_generator import BabyImageGenerator

async def test_init():
    """测试初始化生成3张图片"""
    
    generator = BabyImageGenerator()
    
    # 使用 wj.jpg 测试
    test_image_path = "../public/sample-photos/wj.jpg"
    
    if not os.path.exists(test_image_path):
        print(f"错误: 找不到测试图片 {test_image_path}")
        return
    
    with open(test_image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()
    
    photos = [{
        "data": image_data,
        "content_type": "image/jpeg"
    }]
    
    print("使用 zjm.jpg 测试初始化接口...")
    print("生成3张图片: normal, wet_diaper_crying, diaper_change_happy")
    print("="*50)
    
    # 初始化时固定生成这3个场景
    init_scenes = ["normal", "wet_diaper_crying", "diaper_change_happy"]
    
    results = await generator.generate_scenes(photos, "male", init_scenes)
    
    print("\n" + "="*50)
    print("生成结果 (JSON格式):")
    print("="*50)
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    print("\n" + "="*50)
    print("图片链接:")
    print("="*50)
    for scene, url in results.items():
        scene_names = {
            "normal": "普通状态",
            "wet_diaper_crying": "穿湿尿裤哭脸",
            "diaper_change_happy": "换好尿裤笑脸"
        }
        print(f"\n{scene} ({scene_names.get(scene, '')}):")
        print(f"  {url}")

if __name__ == "__main__":
    asyncio.run(test_init())
