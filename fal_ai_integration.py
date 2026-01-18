#!/usr/bin/env python3
"""
fal.ai 集成示例
展示如何使用 chinese_baby_prompts.py 生成中国宝宝照片
"""

import os
from typing import List, Dict, Any
from chinese_baby_prompts import get_fal_ai_config

# 尝试导入 fal_client
try:
    import fal_client
    FAL_AVAILABLE = True
except ImportError:
    FAL_AVAILABLE = False
    print("警告: fal_client 未安装")
    print("请运行: pip install fal-client")


def generate_single_photo(
    age_stage: str = "newborn_0_3",
    gender: str = None,
    expression: str = "happy",
    scene: str = "studio",
    api_key: str = None
) -> Dict[str, Any]:
    """
    生成单张中国宝宝照片
    
    Args:
        age_stage: 年龄阶段 ("newborn_0_3", "infant_3_12", "toddler_1_2", "preschool_2_3")
        gender: 性别 ("boy", "girl", None)
        expression: 表情 ("happy", "sleeping", "curious", "crying", "neutral")
        scene: 场景 ("studio", "home", "outdoor")
        api_key: fal.ai API 密钥（可选，默认从环境变量读取）
    
    Returns:
        dict: 包含图片URL和元数据的字典
    """
    if not FAL_AVAILABLE:
        return {
            "success": False,
            "error": "fal_client 未安装",
            "message": "请运行: pip install fal-client"
        }
    
    # 设置 API 密钥
    if api_key:
        os.environ["FAL_KEY"] = api_key
    elif not os.environ.get("FAL_KEY"):
        return {
            "success": False,
            "error": "API 密钥未设置",
            "message": "请设置 FAL_KEY 环境变量或传入 api_key 参数"
        }
    
    try:
        # 获取提示词配置
        config = get_fal_ai_config(age_stage, gender, expression, scene)
        
        print(f"正在生成照片...")
        print(f"年龄阶段: {age_stage}")
        print(f"性别: {gender or '随机'}")
        print(f"表情: {expression}")
        print(f"场景: {scene}")
        
        # 调用 fal.ai API
        result = fal_client.subscribe(
            "fal-ai/flux/schnell",  # 使用 Flux Schnell 快速模型
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
        
        # 提取结果
        if result and "images" in result and len(result["images"]) > 0:
            image_url = result["images"][0]["url"]
            
            return {
                "success": True,
                "image_url": image_url,
                "metadata": {
                    "age_stage": age_stage,
                    "gender": gender,
                    "expression": expression,
                    "scene": scene,
                    "prompt": config["prompt"],
                    "negative_prompt": config["negative_prompt"]
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
            "message": f"生成照片时出错: {str(e)}"
        }


def batch_generate_photos(
    configs: List[Dict[str, str]],
    api_key: str = None
) -> List[Dict[str, Any]]:
    """
    批量生成多张照片
    
    Args:
        configs: 配置列表，每个配置包含 age_stage, gender, expression, scene
        api_key: fal.ai API 密钥
    
    Returns:
        list: 生成结果列表
    
    Example:
        configs = [
            {"age_stage": "newborn_0_3", "gender": "boy", "expression": "sleeping", "scene": "studio"},
            {"age_stage": "infant_3_12", "gender": "girl", "expression": "happy", "scene": "home"},
        ]
        results = batch_generate_photos(configs)
    """
    results = []
    
    for i, config in enumerate(configs, 1):
        print(f"\n生成第 {i}/{len(configs)} 张照片...")
        
        result = generate_single_photo(
            age_stage=config.get("age_stage", "newborn_0_3"),
            gender=config.get("gender"),
            expression=config.get("expression", "happy"),
            scene=config.get("scene", "studio"),
            api_key=api_key
        )
        
        results.append(result)
        
        if result["success"]:
            print(f"✅ 成功: {result['image_url']}")
        else:
            print(f"❌ 失败: {result.get('message', result.get('error'))}")
    
    return results


# 使用示例
if __name__ == "__main__":
    print("=" * 60)
    print("fal.ai 中国宝宝照片生成示例")
    print("=" * 60)
    
    # 检查环境
    if not FAL_AVAILABLE:
        print("\n❌ fal_client 未安装，无法运行示例")
        print("请运行: pip install fal-client")
        exit(1)
    
    if not os.environ.get("FAL_KEY"):
        print("\n❌ FAL_KEY 环境变量未设置")
        print("请设置: set FAL_KEY=your_api_key")
        exit(1)
    
    # 示例1: 生成单张照片
    print("\n【示例1】生成新生儿男孩照片")
    print("-" * 60)
    
    result1 = generate_single_photo(
        age_stage="newborn_0_3",
        gender="boy",
        expression="sleeping",
        scene="studio"
    )
    
    if result1["success"]:
        print(f"\n✅ 生成成功！")
        print(f"图片URL: {result1['image_url']}")
        print(f"\n元数据:")
        for key, value in result1["metadata"].items():
            if key not in ["prompt", "negative_prompt"]:
                print(f"  {key}: {value}")
    else:
        print(f"\n❌ 生成失败: {result1.get('message', result1.get('error'))}")
    
    # 示例2: 批量生成
    print("\n\n【示例2】批量生成多张照片")
    print("-" * 60)
    
    configs = [
        {
            "age_stage": "infant_3_12",
            "gender": "girl",
            "expression": "happy",
            "scene": "home"
        },
        {
            "age_stage": "toddler_1_2",
            "gender": None,  # 随机性别
            "expression": "curious",
            "scene": "outdoor"
        }
    ]
    
    # 询问是否继续
    response = input("\n是否继续批量生成？(会消耗 API 配额) [y/N]: ")
    if response.lower() == 'y':
        results = batch_generate_photos(configs)
        
        print("\n" + "=" * 60)
        print("批量生成结果摘要")
        print("=" * 60)
        
        success_count = sum(1 for r in results if r["success"])
        print(f"\n成功: {success_count}/{len(results)}")
        
        for i, result in enumerate(results, 1):
            if result["success"]:
                print(f"\n照片 {i}: {result['image_url']}")
    else:
        print("\n已取消批量生成")
    
    print("\n" + "=" * 60)
    print("示例运行完成")
    print("=" * 60)
