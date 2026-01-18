#!/usr/bin/env python3
"""
中国宝宝照片生成 - fal.ai 提示词配置
确保生成纯正的中国宝宝特征
"""

# 基础正面提示词 - 强化中国宝宝特征
POSITIVE_PROMPT_BASE = """
(pure Chinese baby:1.5), (single eyelid:1.2), (monolid:1.2),
(black straight hair:1.3), (dark brown eyes:1.3), (dark eyes:1.3),
(flat nose bridge:1.1), (shallow eye socket:1.2), (epicanthic fold:1.1),
round face, chubby cheeks, smooth skin, fair skin tone,
soft baby skin, natural lighting, warm tones,
high quality, 8k resolution, highly detailed, photorealistic,
studio photography, professional baby portrait
"""

# 基础负面提示词 - 排除西方特征
NEGATIVE_PROMPT_BASE = """
mixed race, caucasian, western features, european features,
blonde hair, light hair, brown hair, red hair,
blue eyes, green eyes, hazel eyes, light colored eyes,
(double eyelids:1.3), (deep eye socket:1.3), (prominent eye socket:1.2),
curly hair, wavy hair, high nose bridge, prominent nose,
freckles, dimples, cleft chin,
low quality, blurry, distorted, deformed, ugly,
cartoon, anime, illustration, painting, drawing
"""

# 年龄阶段特定提示词
AGE_STAGE_PROMPTS = {
    "newborn_0_3": {
        "positive": "newborn baby, 0-3 months old, tiny infant, very young baby, delicate features, soft skin, peaceful expression",
        "negative": "older baby, toddler, child"
    },
    "infant_3_12": {
        "positive": "infant baby, 3-12 months old, sitting baby, curious baby, bright eyes, developing features",
        "negative": "newborn, toddler, child, walking"
    },
    "toddler_1_2": {
        "positive": "toddler, 1-2 years old, young child, playful expression, active pose, developing personality",
        "negative": "newborn, infant, older child, teenager"
    },
    "preschool_2_3": {
        "positive": "preschool child, 2-3 years old, young kid, expressive face, clear features, confident pose",
        "negative": "baby, infant, older child, school age"
    }
}

# 性别特定提示词
GENDER_PROMPTS = {
    "boy": {
        "positive": "baby boy, male infant, boy features",
        "negative": "girl, female"
    },
    "girl": {
        "positive": "baby girl, female infant, girl features",
        "negative": "boy, male"
    }
}

# 表情提示词
EXPRESSION_PROMPTS = {
    "happy": {
        "positive": "happy smile, joyful expression, bright eyes, cheerful, laughing",
        "negative": "crying, sad, angry, scared, upset"
    },
    "sleeping": {
        "positive": "sleeping peacefully, eyes closed, calm expression, relaxed face, serene",
        "negative": "eyes open, awake, crying, active"
    },
    "curious": {
        "positive": "curious expression, wide eyes, interested look, exploring, attentive",
        "negative": "crying, sleeping, bored, disinterested"
    },
    "crying": {
        "positive": "crying, tears, upset expression, open mouth, emotional",
        "negative": "happy, smiling, sleeping, calm"
    },
    "neutral": {
        "positive": "neutral expression, calm face, peaceful look, gentle expression",
        "negative": "extreme emotion, crying, laughing"
    }
}

# 场景提示词
SCENE_PROMPTS = {
    "studio": {
        "positive": "studio photography, professional lighting, clean background, white backdrop, soft lighting setup",
        "negative": "outdoor, messy background, cluttered, dark"
    },
    "home": {
        "positive": "home environment, cozy setting, warm atmosphere, indoor scene, family setting",
        "negative": "studio, outdoor, professional setup"
    },
    "outdoor": {
        "positive": "outdoor scene, natural light, garden setting, park environment, fresh air",
        "negative": "indoor, studio, artificial lighting"
    }
}


def generate_prompt(age_stage="newborn_0_3", gender=None, expression="happy", scene="studio"):
    """
    生成完整的提示词
    
    Args:
        age_stage: 年龄阶段 ("newborn_0_3", "infant_3_12", "toddler_1_2", "preschool_2_3")
        gender: 性别 ("boy", "girl", None)
        expression: 表情 ("happy", "sleeping", "curious", "crying", "neutral")
        scene: 场景 ("studio", "home", "outdoor")
    
    Returns:
        dict: {"positive": str, "negative": str}
    """
    # 组合正面提示词
    positive_parts = [
        POSITIVE_PROMPT_BASE.strip(),
        AGE_STAGE_PROMPTS.get(age_stage, AGE_STAGE_PROMPTS["newborn_0_3"])["positive"],
        EXPRESSION_PROMPTS.get(expression, EXPRESSION_PROMPTS["happy"])["positive"],
        SCENE_PROMPTS.get(scene, SCENE_PROMPTS["studio"])["positive"]
    ]
    
    if gender and gender in GENDER_PROMPTS:
        positive_parts.append(GENDER_PROMPTS[gender]["positive"])
    
    positive_prompt = ", ".join(positive_parts)
    
    # 组合负面提示词
    negative_parts = [
        NEGATIVE_PROMPT_BASE.strip(),
        AGE_STAGE_PROMPTS.get(age_stage, AGE_STAGE_PROMPTS["newborn_0_3"])["negative"],
        EXPRESSION_PROMPTS.get(expression, EXPRESSION_PROMPTS["happy"])["negative"],
        SCENE_PROMPTS.get(scene, SCENE_PROMPTS["studio"])["negative"]
    ]
    
    if gender and gender in GENDER_PROMPTS:
        negative_parts.append(GENDER_PROMPTS[gender]["negative"])
    
    negative_prompt = ", ".join(negative_parts)
    
    return {
        "positive": positive_prompt,
        "negative": negative_prompt
    }


def get_fal_ai_config(age_stage="newborn_0_3", gender=None, expression="happy", scene="studio"):
    """
    获取 fal.ai API 的完整配置
    
    Returns:
        dict: fal.ai API 参数
    """
    prompts = generate_prompt(age_stage, gender, expression, scene)
    
    return {
        "prompt": prompts["positive"],
        "negative_prompt": prompts["negative"],
        "image_size": "square_hd",  # 1024x1024
        "num_inference_steps": 4,    # Flux Schnell 推荐 4 步
        "guidance_scale": 3.5,       # 引导强度
        "num_images": 1,
        "enable_safety_checker": True
    }


# 测试示例
if __name__ == "__main__":
    print("=" * 60)
    print("中国宝宝照片生成 - 提示词示例")
    print("=" * 60)
    
    # 示例1: 新生儿男孩
    print("\n【示例1】新生儿男孩，睡觉，工作室")
    config1 = get_fal_ai_config("newborn_0_3", "boy", "sleeping", "studio")
    print(f"\n正面提示词:\n{config1['prompt']}")
    print(f"\n负面提示词:\n{config1['negative_prompt']}")
    
    # 示例2: 6个月女孩
    print("\n" + "=" * 60)
    print("【示例2】6个月女孩，开心，家庭环境")
    config2 = get_fal_ai_config("infant_3_12", "girl", "happy", "home")
    print(f"\n正面提示词:\n{config2['prompt']}")
    
    # 示例3: 2岁幼儿
    print("\n" + "=" * 60)
    print("【示例3】2岁幼儿，好奇，户外")
    config3 = get_fal_ai_config("toddler_1_2", None, "curious", "outdoor")
    print(f"\n正面提示词:\n{config3['prompt']}")
