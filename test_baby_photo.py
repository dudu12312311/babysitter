#!/usr/bin/env python3
"""
宝宝照片生成功能测试脚本
用于验证照片生成功能是否正常工作
"""

import os
import sys

def test_imports():
    """测试模块导入"""
    print("=" * 60)
    print("测试 1: 检查模块导入")
    print("=" * 60)
    
    try:
        import chinese_baby_prompts
        print("✅ chinese_baby_prompts 导入成功")
    except ImportError as e:
        print(f"❌ chinese_baby_prompts 导入失败: {e}")
        return False
    
    try:
        import baby_photo_integration
        print("✅ baby_photo_integration 导入成功")
    except ImportError as e:
        print(f"❌ baby_photo_integration 导入失败: {e}")
        return False
    
    try:
        import baby_photo_api
        print("✅ baby_photo_api 导入成功")
    except ImportError as e:
        print(f"❌ baby_photo_api 导入失败: {e}")
        return False
    
    return True


def test_fal_client():
    """测试 fal_client 安装"""
    print("\n" + "=" * 60)
    print("测试 2: 检查 fal_client 安装")
    print("=" * 60)
    
    try:
        import fal_client
        print("✅ fal_client 已安装")
        return True
    except ImportError:
        print("❌ fal_client 未安装")
        print("   请运行: pip install fal-client")
        return False


def test_api_key():
    """测试 API 密钥配置"""
    print("\n" + "=" * 60)
    print("测试 3: 检查 API 密钥配置")
    print("=" * 60)
    
    api_key = os.environ.get("FAL_KEY")
    if api_key:
        print(f"✅ FAL_KEY 已配置 (长度: {len(api_key)})")
        return True
    else:
        print("❌ FAL_KEY 未配置")
        print("   请设置环境变量: set FAL_KEY=your_api_key")
        return False


def test_prompt_generation():
    """测试提示词生成"""
    print("\n" + "=" * 60)
    print("测试 4: 测试提示词生成")
    print("=" * 60)
    
    try:
        from chinese_baby_prompts import generate_prompt, get_fal_ai_config
        
        # 测试生成提示词
        prompts = generate_prompt("newborn_0_3", "boy", "sleeping", "studio")
        print("✅ 提示词生成成功")
        print(f"\n正面提示词预览:")
        print(prompts["positive"][:200] + "...")
        print(f"\n负面提示词预览:")
        print(prompts["negative"][:200] + "...")
        
        # 测试获取配置
        config = get_fal_ai_config("infant_3_12", "girl", "happy", "home")
        print(f"\n✅ 配置生成成功")
        print(f"   图片尺寸: {config['image_size']}")
        print(f"   推理步数: {config['num_inference_steps']}")
        print(f"   引导强度: {config['guidance_scale']}")
        
        return True
    except Exception as e:
        print(f"❌ 提示词生成失败: {e}")
        return False


def test_photo_generator():
    """测试照片生成器初始化"""
    print("\n" + "=" * 60)
    print("测试 5: 测试照片生成器初始化")
    print("=" * 60)
    
    try:
        from baby_photo_integration import BabyPhotoGenerator
        
        generator = BabyPhotoGenerator()
        print("✅ BabyPhotoGenerator 初始化成功")
        
        # 测试年龄阶段映射
        test_ages = [1, 6, 18, 30]
        for age in test_ages:
            stage = generator._get_age_stage(age)
            print(f"   {age}个月 -> {stage}")
        
        return True
    except Exception as e:
        print(f"❌ 照片生成器初始化失败: {e}")
        return False


def test_flask_blueprint():
    """测试 Flask Blueprint"""
    print("\n" + "=" * 60)
    print("测试 6: 测试 Flask Blueprint")
    print("=" * 60)
    
    try:
        from baby_photo_api import baby_photo_bp
        
        print("✅ Blueprint 导入成功")
        print(f"   Blueprint 名称: {baby_photo_bp.name}")
        print(f"   URL 前缀: {baby_photo_bp.url_prefix}")
        
        # 列出所有路由
        print("\n   注册的路由:")
        for rule in baby_photo_bp.deferred_functions:
            print(f"   - {rule}")
        
        return True
    except Exception as e:
        print(f"❌ Blueprint 测试失败: {e}")
        return False


def test_full_generation():
    """测试完整照片生成流程（需要 API 密钥）"""
    print("\n" + "=" * 60)
    print("测试 7: 测试完整照片生成（可选）")
    print("=" * 60)
    
    # 检查是否有 API 密钥
    if not os.environ.get("FAL_KEY"):
        print("⚠️  跳过：未配置 FAL_KEY")
        return True
    
    try:
        from baby_photo_integration import BabyPhotoGenerator, FAL_AVAILABLE
        
        if not FAL_AVAILABLE:
            print("⚠️  跳过：fal_client 未安装")
            return True
        
        print("🔄 开始生成测试照片...")
        print("   (这可能需要 10-20 秒)")
        
        generator = BabyPhotoGenerator()
        result = generator.generate_baby_photo(
            age_months=6,
            gender="boy",
            expression="happy",
            scene="studio"
        )
        
        if result["success"]:
            print("✅ 照片生成成功！")
            print(f"   图片URL: {result['image_url']}")
            print(f"   年龄阶段: {result['metadata']['age_stage']}")
            print(f"   表情: {result['metadata']['expression']}")
            return True
        else:
            print(f"❌ 照片生成失败: {result.get('message', result.get('error'))}")
            return False
            
    except Exception as e:
        print(f"❌ 完整生成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("\n" + "🧪" * 30)
    print("宝宝照片生成功能测试")
    print("🧪" * 30 + "\n")
    
    results = []
    
    # 运行所有测试
    results.append(("模块导入", test_imports()))
    results.append(("fal_client 安装", test_fal_client()))
    results.append(("API 密钥配置", test_api_key()))
    results.append(("提示词生成", test_prompt_generation()))
    results.append(("照片生成器", test_photo_generator()))
    results.append(("Flask Blueprint", test_flask_blueprint()))
    
    # 询问是否运行完整生成测试
    print("\n" + "=" * 60)
    if os.environ.get("FAL_KEY"):
        response = input("是否运行完整照片生成测试？(会消耗 API 配额) [y/N]: ")
        if response.lower() == 'y':
            results.append(("完整照片生成", test_full_generation()))
    
    # 显示测试结果摘要
    print("\n" + "=" * 60)
    print("测试结果摘要")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name:20s} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"总计: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    if failed == 0:
        print("\n🎉 所有测试通过！照片生成功能已就绪。")
        return 0
    else:
        print(f"\n⚠️  有 {failed} 个测试失败，请检查上述错误信息。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
