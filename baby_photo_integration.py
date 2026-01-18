#!/usr/bin/env python3
"""
宝宝照片生成集成模块
将中国宝宝照片生成功能集成到育儿模拟器中
"""

import os
from typing import Dict, Any, Optional
from chinese_baby_prompts import get_fal_ai_config, generate_prompt

# 尝试导入 fal_client
try:
    import fal_client
    FAL_AVAILABLE = True
except ImportError:
    FAL_AVAILABLE = False
    print("警告: fal_client 未安装，照片生成功能不可用")


class BabyPhotoGenerator:
    """宝宝照片生成器"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化照片生成器
        
        Args:
            api_key: fal.ai API密钥，如果不提供则从环境变量读取
        """
        self.api_key = api_key or os.environ.get("FAL_KEY")
        
        if not self.api_key:
            print("警告: 未设置 FAL_KEY 环境变量，照片生成功能不可用")
        
        if not FAL_AVAILABLE:
            print("提示: 请运行 'pip install fal-client' 安装依赖")
    
    def generate_baby_photo(
        self,
        age_months: int,
        gender: Optional[str] = None,
        expression: str = "happy",
        scene: str = "studio"
    ) -> Dict[str, Any]:
        """
        根据宝宝年龄生成照片
        
        Args:
            age_months: 宝宝月龄 (0-36)
            gender: 性别 ("boy" 或 "girl"，None表示随机)
            expression: 表情 ("happy", "sleeping", "curious", "crying", "neutral")
            scene: 场景 ("studio", "home", "outdoor")
        
        Returns:
            包含照片URL和元数据的字典
        """
        if not FAL_AVAILABLE or not self.api_key:
            return {
                "success": False,
                "error": "照片生成功能不可用",
                "message": "请安装 fal-client 并设置 FAL_KEY 环境变量"
            }
        
        # 根据月龄确定年龄阶段
        age_stage = self._get_age_stage(age_months)
        
        # 获取 fal.ai 配置
        config = get_fal_ai_config(age_stage, gender, expression, scene)
        
        try:
            # 调用 fal.ai API
            result = fal_client.subscribe(
                "fal-ai/flux/schnell",  # 使用快速模型
                arguments={
                    "prompt": config["prompt"],
                    "negative_prompt": config["negative_prompt"],
                    "image_size": config["image_size"],
                    "num_inference_steps": config["num_inference_steps"],
                    "guidance_scale": config["guidance_scale"],
                    "num_images": 1,
                    "enable_safety_checker": True
                }
            )
            
            # 提取图片URL
            if result and "images" in result and len(result["images"]) > 0:
                image_url = result["images"][0]["url"]
                
                return {
                    "success": True,
                    "image_url": image_url,
                    "metadata": {
                        "age_months": age_months,
                        "age_stage": age_stage,
                        "gender": gender,
                        "expression": expression,
                        "scene": scene,
                        "prompt": config["prompt"]
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "生成失败",
                    "message": "API返回结果为空"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"照片生成失败: {str(e)}"
            }
    
    def _get_age_stage(self, age_months: int) -> str:
        """根据月龄确定年龄阶段"""
        if age_months <= 3:
            return "newborn_0_3"
        elif age_months <= 12:
            return "infant_3_12"
        elif age_months <= 24:
            return "toddler_1_2"
        else:
            return "preschool_2_3"
    
    def generate_for_game_state(self, game_state: Any) -> Dict[str, Any]:
        """
        根据游戏状态生成宝宝照片
        
        Args:
            game_state: 游戏状态对象 (包含 baby_age_months, baby_personality 等)
        
        Returns:
            照片生成结果
        """
        # 根据游戏状态确定表情
        expression = self._determine_expression(game_state)
        
        # 生成照片
        return self.generate_baby_photo(
            age_months=game_state.baby_age_months,
            gender=None,  # 随机性别
            expression=expression,
            scene="studio"
        )
    
    def _determine_expression(self, game_state: Any) -> str:
        """根据游戏状态确定宝宝表情"""
        # 根据快乐度和健康值决定表情
        if game_state.happiness >= 80:
            return "happy"
        elif game_state.happiness <= 30:
            return "crying"
        elif game_state.is_sleeping:
            return "sleeping"
        elif game_state.health <= 50:
            return "neutral"
        else:
            return "curious"


# 使用示例
if __name__ == "__main__":
    # 创建照片生成器
    generator = BabyPhotoGenerator()
    
    # 示例1: 生成新生儿照片
    print("\n【示例1】生成新生儿男孩照片")
    result1 = generator.generate_baby_photo(
        age_months=1,
        gender="boy",
        expression="sleeping",
        scene="studio"
    )
    
    if result1["success"]:
        print(f"✅ 生成成功！")
        print(f"图片URL: {result1['image_url']}")
        print(f"元数据: {result1['metadata']}")
    else:
        print(f"❌ 生成失败: {result1.get('message', result1.get('error'))}")
    
    # 示例2: 生成6个月女孩照片
    print("\n【示例2】生成6个月女孩照片")
    result2 = generator.generate_baby_photo(
        age_months=6,
        gender="girl",
        expression="happy",
        scene="home"
    )
    
    if result2["success"]:
        print(f"✅ 生成成功！")
        print(f"图片URL: {result2['image_url']}")
    else:
        print(f"❌ 生成失败: {result2.get('message', result2.get('error'))}")
