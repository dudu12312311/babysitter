#!/usr/bin/env python3
"""
宝宝照片生成 API 端点
为 Flask 应用添加照片生成功能
"""

from flask import Blueprint, jsonify, request
from baby_photo_integration import BabyPhotoGenerator

# 创建 Blueprint
baby_photo_bp = Blueprint('baby_photo', __name__, url_prefix='/api/baby-photo')

# 创建照片生成器实例
photo_generator = BabyPhotoGenerator()


@baby_photo_bp.route('/generate', methods=['POST'])
def generate_photo():
    """
    生成宝宝照片
    
    请求体示例:
    {
        "age_months": 6,
        "gender": "boy",  // 可选: "boy", "girl", null
        "expression": "happy",  // 可选: "happy", "sleeping", "curious", "crying", "neutral"
        "scene": "studio"  // 可选: "studio", "home", "outdoor"
    }
    """
    try:
        data = request.get_json() or {}
        
        # 获取参数
        age_months = data.get('age_months', 0)
        gender = data.get('gender')
        expression = data.get('expression', 'happy')
        scene = data.get('scene', 'studio')
        
        # 验证参数
        if not isinstance(age_months, int) or age_months < 0 or age_months > 36:
            return jsonify({
                'success': False,
                'error': '月龄必须在 0-36 之间'
            }), 400
        
        if gender and gender not in ['boy', 'girl']:
            return jsonify({
                'success': False,
                'error': '性别必须是 boy 或 girl'
            }), 400
        
        if expression not in ['happy', 'sleeping', 'curious', 'crying', 'neutral']:
            return jsonify({
                'success': False,
                'error': '表情必须是 happy, sleeping, curious, crying 或 neutral'
            }), 400
        
        if scene not in ['studio', 'home', 'outdoor']:
            return jsonify({
                'success': False,
                'error': '场景必须是 studio, home 或 outdoor'
            }), 400
        
        # 生成照片
        result = photo_generator.generate_baby_photo(
            age_months=age_months,
            gender=gender,
            expression=expression,
            scene=scene
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@baby_photo_bp.route('/generate-from-game', methods=['POST'])
def generate_from_game():
    """
    根据游戏状态生成宝宝照片
    
    请求体示例:
    {
        "baby_age_months": 6,
        "happiness": 80,
        "health": 90,
        "is_sleeping": false
    }
    """
    try:
        data = request.get_json() or {}
        
        # 创建简化的游戏状态对象
        class SimpleGameState:
            def __init__(self, data):
                self.baby_age_months = data.get('baby_age_months', 0)
                self.happiness = data.get('happiness', 50)
                self.health = data.get('health', 100)
                self.is_sleeping = data.get('is_sleeping', False)
        
        game_state = SimpleGameState(data)
        
        # 生成照片
        result = photo_generator.generate_for_game_state(game_state)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@baby_photo_bp.route('/preview-prompt', methods=['POST'])
def preview_prompt():
    """
    预览提示词（不生成图片）
    
    请求体示例:
    {
        "age_months": 6,
        "gender": "boy",
        "expression": "happy",
        "scene": "studio"
    }
    """
    try:
        from chinese_baby_prompts import get_fal_ai_config
        
        data = request.get_json() or {}
        
        age_months = data.get('age_months', 0)
        gender = data.get('gender')
        expression = data.get('expression', 'happy')
        scene = data.get('scene', 'studio')
        
        # 确定年龄阶段
        if age_months <= 3:
            age_stage = "newborn_0_3"
        elif age_months <= 12:
            age_stage = "infant_3_12"
        elif age_months <= 24:
            age_stage = "toddler_1_2"
        else:
            age_stage = "preschool_2_3"
        
        # 获取配置
        config = get_fal_ai_config(age_stage, gender, expression, scene)
        
        return jsonify({
            'success': True,
            'age_stage': age_stage,
            'prompt': config['prompt'],
            'negative_prompt': config['negative_prompt'],
            'config': {
                'image_size': config['image_size'],
                'num_inference_steps': config['num_inference_steps'],
                'guidance_scale': config['guidance_scale']
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@baby_photo_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    from baby_photo_integration import FAL_AVAILABLE
    import os
    
    return jsonify({
        'status': 'healthy',
        'fal_client_installed': FAL_AVAILABLE,
        'api_key_configured': bool(os.environ.get('FAL_KEY'))
    })
