#!/usr/bin/env python3
"""
宝宝面部融合功能测试脚本
"""

import os
import sys

def test_imports():
    """测试模块导入"""
    print("=" * 60)
    print("测试 1: 检查模块导入")
    print("=" * 60)
    
    try:
        import baby_face_fusion
        print("✅ baby_face_fusion 导入成功")
    except ImportError as e:
        print(f"❌ baby_face_fusion 导入失败: {e}")
        return False
    
    try:
        import baby_face_fusion_api
        print("✅ baby_face_fusion_api 导入成功")
    except ImportError as e:
        print(f"❌ baby_face_fusion_api 导入失败: {e}")
        return False
    
    return True


def test_dependencies():
    """测试依赖安装"""
    print("\n" + "=" * 60)
    print("测试 2: 检查依赖安装")
    print("=" * 60)
    
    dependencies = {
        'fal_client': 'fal-client',
        'flask': 'Flask',
        'werkzeug': 'Werkzeug',
        'PIL': 'Pillow'
    }
    
    all_installed = True
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"❌ {package} 未安装")
            print(f"   请运行: pip install {package}")
            all_installed = False
    
    return all_installed


def test_api_keys():
    """测试 API 密钥配置"""
    print("\n" + "=" * 60)
    print("测试 3: 检查 API 密钥配置")
    print("=" * 60)
    
    fal_key = os.environ.get("FAL_KEY")
    replicate_key = os.environ.get("REPLICATE_API_TOKEN")
    
    if fal_key:
        print(f"✅ FAL_KEY 已配置 (长度: {len(fal_key)})")
        return True
    elif replicate_key:
        print(f"✅ REPLICATE_API_TOKEN 已配置 (长度: {len(replicate_key)})")
        return True
    else:
        print("❌ 未配置任何 API 密钥")
        print("   请设置以下环境变量之一：")
        print("   - set FAL_KEY=你的fal.ai密钥")
        print("   - set REPLICATE_API_TOKEN=你的replicate密钥")
        return False


def test_upload_folder():
    """测试上传文件夹"""
    print("\n" + "=" * 60)
    print("测试 4: 检查上传文件夹")
    print("=" * 60)
    
    upload_folder = 'uploads/parents'
    
    if os.path.exists(upload_folder):
        print(f"✅ 上传文件夹已存在: {upload_folder}")
    else:
        try:
            os.makedirs(upload_folder, exist_ok=True)
            print(f"✅ 创建上传文件夹: {upload_folder}")
        except Exception as e:
            print(f"❌ 创建上传文件夹失败: {e}")
            return False
    
    return True


def test_fusion_generator():
    """测试面部融合生成器初始化"""
    print("\n" + "=" * 60)
    print("测试 5: 测试面部融合生成器")
    print("=" * 60)
    
    try:
        from baby_face_fusion import BabyFaceFusion
        
        generator = BabyFaceFusion()
        print("✅ BabyFaceFusion 初始化成功")
        
        # 测试年龄选项
        ages = ["newborn", "6months", "1year", "2years"]
        print(f"\n支持的年龄阶段:")
        for age in ages:
            print(f"  - {age}")
        
        return True
    except Exception as e:
        print(f"❌ 面部融合生成器初始化失败: {e}")
        return False


def test_flask_app():
    """测试 Flask 应用"""
    print("\n" + "=" * 60)
    print("测试 6: 测试 Flask 应用")
    print("=" * 60)
    
    try:
        from baby_face_fusion_api import baby_fusion_bp
        
        print("✅ Blueprint 导入成功")
        print(f"   Blueprint 名称: {baby_fusion_bp.name}")
        print(f"   URL 前缀: {baby_fusion_bp.url_prefix}")
        
        return True
    except Exception as e:
        print(f"❌ Flask 应用测试失败: {e}")
        return False


def main():
    """运行所有测试"""
    print("\n" + "🧪" * 30)
    print("宝宝面部融合功能测试")
    print("🧪" * 30 + "\n")
    
    results = []
    
    # 运行所有测试
    results.append(("模块导入", test_imports()))
    results.append(("依赖安装", test_dependencies()))
    results.append(("API 密钥配置", test_api_keys()))
    results.append(("上传文件夹", test_upload_folder()))
    results.append(("面部融合生成器", test_fusion_generator()))
    results.append(("Flask 应用", test_flask_app()))
    
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
        print("\n🎉 所有测试通过！面部融合功能已就绪。")
        print("\n下一步:")
        print("1. 运行应用: python main_face_fusion.py")
        print("2. 访问: http://localhost:5000")
        print("3. 点击 '开始生成宝宝照片' 上传父母照片")
        return 0
    else:
        print(f"\n⚠️  有 {failed} 个测试失败，请检查上述错误信息。")
        
        if not results[1][1]:  # 依赖安装失败
            print("\n💡 快速修复:")
            print("   运行: install_face_fusion.bat")
        
        if not results[2][1]:  # API 密钥未配置
            print("\n💡 快速修复:")
            print("   运行: set FAL_KEY=你的fal.ai密钥")
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
