#!/usr/bin/env python3
"""测试环境设置"""

print("=" * 50)
print("测试环境设置")
print("=" * 50)

# 测试 Flask
try:
    import flask
    print("✅ Flask 已安装:", flask.__version__)
except ImportError as e:
    print("❌ Flask 未安装:", e)

# 测试游戏模块
try:
    from hardcore_parenting_game import HardcoreParentingGame
    print("✅ 游戏模块可用")
except ImportError as e:
    print("❌ 游戏模块不可用:", e)

# 测试换尿布任务
try:
    from diaper_change_task import diaper_bp
    print("✅ 换尿布任务模块可用")
except ImportError as e:
    print("❌ 换尿布任务模块不可用:", e)

print("=" * 50)
print("测试完成")
print("=" * 50)
