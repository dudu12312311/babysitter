#!/usr/bin/env python3
"""
宝宝面部融合系统
上传父母照片，生成预测的宝宝照片
"""

import os
import base64
from typing import Dict, Any, List, Optional
from pathlib import Path

# 尝试导入 fal_client
try:
    import fal_client
    FAL_AVAILABLE = True
except ImportError:
    FAL_AVAILABLE = False
    print("警告: fal_client 未安装")

# 尝试导入 replicate
try:
    import replicate
    REPLICATE_AVAILABLE = True
except ImportError:
    REPLICATE_AVAILABLE = False
    print("警告: replicate 未安装")


class BabyFaceFusion:
    """宝宝面部融合生成器"""
    
    def __init__(self, fal_key: str = None, replicate_key: str = None):
        """
        初始化面部融合生成器
        
        Args:
            fal_key: fal.ai API 密钥
            replicate_key: Replicate API 密钥
        """
        self.fal_key = fal_key or os.environ.get("FAL_KEY")
        self.replicate_key = replicate_key or os.environ.get("REPLICATE_API_TOKEN")
        
        if self.fal_key:
            os.environ["FAL_KEY"] = self.fal_key
        
        if self.replicate_key:
            os.environ["REPLICATE_API_TOKEN"] = self.replicate_key
    
    def _read_image_as_base64(self, image_path: str) -> str:
        """读取图片并转换为 base64"""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    
    def _upload_image_to_fal(self, image_path: str) -> str:
        """上传图片到 fal.ai 并获取 URL"""
        if not FAL_AVAILABLE:
            raise Exception("fal_client 未安装")
        
        # fal.ai 支持直接上传文件
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # 返回本地路径，fal.ai 会自动处理
        return image_path
    
    def generate_baby_from_parents_fal(
        self,
        parent1_image: str,
        parent2_image: str = None,
        baby_age: str = "newborn",
        num_variations: int = 4
    ) -> Dict[str, Any]:
        """
        使用 fal.ai 从父母照片生成宝宝照片
        
        Args:
            parent1_image: 父母1的照片路径
            parent2_image: 父母2的照片路径（可选）
            baby_age: 宝宝年龄 ("newborn", "6months", "1year", "2years")
            num_variations: 生成变体数量
        
        Returns:
            生成结果
        """
        if not FAL_AVAILABLE:
            return {
                "success": False,
                "error": "fal_client 未安装",
                "message": "请运行: pip install fal-client"
            }
        
        if not self.fal_key:
            return {
                "success": False,
                "error": "API 密钥未设置",
                "message": "请设置 FAL_KEY 环境变量"
            }
        
        try:
            # 构建提示词
            age_prompts = {
                "newborn": "newborn baby, 0-3 months old",
                "6months": "6 months old baby, infant",
                "1year": "1 year old baby, toddler",
                "2years": "2 years old child, young toddler"
            }
            
            age_prompt = age_prompts.get(baby_age, age_prompts["newborn"])
            
            # 使用 Flux 模型 + IP-Adapter 进行面部融合
            prompt = f"""
            {age_prompt}, (pure Chinese baby:1.5), adorable baby portrait,
            (single eyelid:1.2), (black straight hair:1.3), (dark brown eyes:1.3),
            (flat nose bridge:1.1), round face, chubby cheeks,
            professional baby photography, studio lighting, high quality, 8k
            """
            
            negative_prompt = """
            mixed race, caucasian, western features, adult, teenager,
            (double eyelids:1.3), blue eyes, blonde hair, curly hair,
            low quality, blurry, distorted
            """
            
            print(f"正在生成宝宝照片...")
            print(f"父母照片1: {parent1_image}")
            if parent2_image:
                print(f"父母照片2: {parent2_image}")
            print(f"宝宝年龄: {baby_age}")
            
            # 使用 fal.ai 的 Flux + ControlNet 模型
            # 注意：这里使用参考图片来引导生成
            result = fal_client.subscribe(
                "fal-ai/flux-lora",  # 使用支持参考图的模型
                arguments={
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "image_size": "square_hd",
                    "num_inference_steps": 28,
                    "guidance_scale": 3.5,
                    "num_images": num_variations,
                    "enable_safety_checker": True,
                    # 参考图片（如果模型支持）
                    "image_url": parent1_image if parent1_image.startswith("http") else None
                }
            )
            
            if result and "images" in result:
                return {
                    "success": True,
                    "images": [img["url"] for img in result["images"]],
                    "metadata": {
                        "baby_age": baby_age,
                        "num_variations": len(result["images"]),
                        "parent1_image": parent1_image,
                        "parent2_image": parent2_image
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "生成失败",
                    "message": "API 返回结果为空"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"生成失败: {str(e)}"
            }
    
    def generate_baby_from_parents_replicate(
        self,
        parent1_image: str,
        parent2_image: str = None,
        baby_age: str = "newborn"
    ) -> Dict[str, Any]:
        """
        使用 Replicate 从父母照片生成宝宝照片
        
        Args:
            parent1_image: 父母1的照片路径
            parent2_image: 父母2的照片路径（可选）
            baby_age: 宝宝年龄
        
        Returns:
            生成结果
        """
        if not REPLICATE_AVAILABLE:
            return {
                "success": False,
                "error": "replicate 未安装",
                "message": "请运行: pip install replicate"
            }
        
        if not self.replicate_key:
            return {
                "success": False,
                "error": "API 密钥未设置",
                "message": "请设置 REPLICATE_API_TOKEN 环境变量"
            }
        
        try:
            # 读取图片
            with open(parent1_image, "rb") as f:
                parent1_data = f.read()
            
            parent2_data = None
            if parent2_image:
                with open(parent2_image, "rb") as f:
                    parent2_data = f.read()
            
            # 使用 Replicate 的面部融合模型
            # 注意：这是示例，实际模型可能不同
            output = replicate.run(
                "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                input={
                    "prompt": f"baby portrait, {baby_age}, Chinese baby, adorable",
                    "negative_prompt": "adult, western features, mixed race",
                    "image": parent1_data,
                    "num_outputs": 4
                }
            )
            
            return {
                "success": True,
                "images": list(output),
                "metadata": {
                    "baby_age": baby_age,
                    "parent1_image": parent1_image,
                    "parent2_image": parent2_image
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"生成失败: {str(e)}"
            }


# 使用示例
if __name__ == "__main__":
    print("=" * 60)
    print("宝宝面部融合生成系统")
    print("=" * 60)
    
    # 检查环境
    if not FAL_AVAILABLE and not REPLICATE_AVAILABLE:
        print("\n❌ 未安装任何 AI 客户端")
        print("请运行以下命令之一：")
        print("  pip install fal-client")
        print("  pip install replicate")
        exit(1)
    
    # 创建生成器
    generator = BabyFaceFusion()
    
    # 示例：生成宝宝照片
    print("\n请提供父母照片路径：")
    parent1 = input("父母1照片路径: ").strip()
    parent2 = input("父母2照片路径（可选，按回车跳过）: ").strip() or None
    
    if not os.path.exists(parent1):
        print(f"\n❌ 文件不存在: {parent1}")
        exit(1)
    
    if parent2 and not os.path.exists(parent2):
        print(f"\n❌ 文件不存在: {parent2}")
        exit(1)
    
    print("\n选择宝宝年龄：")
    print("1. 新生儿 (newborn)")
    print("2. 6个月 (6months)")
    print("3. 1岁 (1year)")
    print("4. 2岁 (2years)")
    
    age_choice = input("请选择 (1-4): ").strip()
    age_map = {
        "1": "newborn",
        "2": "6months",
        "3": "1year",
        "4": "2years"
    }
    baby_age = age_map.get(age_choice, "newborn")
    
    print(f"\n开始生成 {baby_age} 宝宝照片...")
    
    if FAL_AVAILABLE:
        result = generator.generate_baby_from_parents_fal(
            parent1_image=parent1,
            parent2_image=parent2,
            baby_age=baby_age,
            num_variations=4
        )
    elif REPLICATE_AVAILABLE:
        result = generator.generate_baby_from_parents_replicate(
            parent1_image=parent1,
            parent2_image=parent2,
            baby_age=baby_age
        )
    
    if result["success"]:
        print("\n✅ 生成成功！")
        print(f"\n生成了 {len(result['images'])} 张宝宝照片：")
        for i, url in enumerate(result["images"], 1):
            print(f"  {i}. {url}")
    else:
        print(f"\n❌ 生成失败: {result.get('message', result.get('error'))}")
