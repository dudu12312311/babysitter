"""
特色任务模式专项演示
展示后备箱俄罗斯方块和挑食谈判专家的详细功能
"""

from hardcore_parenting_simulator import (
    StrollerTetrisTask, PickyEaterNegotiationTask,
    GameState, ActionType, PlayerAction, TetrisItem, NegotiationCard
)
import random


def demo_tetris_detailed():
    """详细演示俄罗斯方块任务"""
    print("🧩 后备箱俄罗斯方块 - 详细演示")
    print("=" * 50)
    
    task = StrollerTetrisTask()
    game_state = GameState()
    
    print("📦 出行打包挑战开始！")
    print(f"后备箱尺寸: {task.trunk_size[0]} x {task.trunk_size[1]}")
    print()
    
    print("📋 需要打包的物品清单:")
    for i, item in enumerate(task.items, 1):
        shape_size = sum(sum(row) for row in item.shape)
        print(f"{i:2d}. {item.name:<12} | 优先级: {item.priority} | 占用空间: {shape_size}格")
    print()
    
    print("🎮 开始打包操作演示...")
    
    # 演示1: 旋转婴儿车
    print("\n--- 操作1: 旋转婴儿车 ---")
    stroller = task.items[0]  # 婴儿车
    print(f"原始形状 (角度 {stroller.rotation}°):")
    for row in stroller.shape:
        print("  " + "".join("█" if cell else "·" for cell in row))
    
    # 旋转90度
    stroller.rotation = 90
    rotated_shape = task._get_rotated_shape(stroller)
    print(f"旋转后形状 (角度 {stroller.rotation}°):")
    for row in rotated_shape:
        print("  " + "".join("█" if cell else "·" for cell in row))
    
    # 演示2: 尝试放置物品
    print("\n--- 操作2: 尝试放置妈咪包 ---")
    mommy_bag = task.items[1]  # 妈咪包
    print(f"妈咪包形状:")
    for row in mommy_bag.shape:
        print("  " + "".join("█" if cell else "·" for cell in row))
    
    # 检查能否在(0,0)位置放置
    can_place = task._can_place_item(mommy_bag, 0, 0)
    print(f"能否在(0,0)位置放置: {'✅ 可以' if can_place else '❌ 不可以'}")
    
    if can_place:
        success = task._place_item(mommy_bag, 0, 0)
        if success:
            print("✅ 成功放置妈咪包！")
            task.items.remove(mommy_bag)
    
    # 演示3: 显示当前后备箱状态
    print("\n--- 当前后备箱状态 ---")
    print("后备箱布局 (0=空位, 数字=物品):")
    for i, row in enumerate(task.trunk_grid):
        print(f"{i}: " + " ".join(str(cell) if cell else "·" for cell in row))
    
    # 演示4: 获取进度信息
    progress = task.get_packing_progress()
    print(f"\n📊 打包进度: {progress['progress']:.1%}")
    print(f"剩余物品: {len(progress['remaining_items'])}件")
    print("剩余物品列表:", ", ".join(progress['remaining_items']))
    
    print("\n🎯 俄罗斯方块任务演示完成！")
    print("这个任务考验空间想象力和时间管理能力。")
    print()


def demo_negotiation_detailed():
    """详细演示谈判任务"""
    print("🥦 挑食谈判专家 - 详细演示")
    print("=" * 50)
    
    task = PickyEaterNegotiationTask()
    game_state = GameState()
    
    print(f"🎯 任务目标: 让孩子吃 {task.target_food}")
    print()
    
    print("👶 孩子初始状态:")
    print(f"  抗拒值: {task.child_resistance}/100")
    print(f"  注意力: {task.child_attention}/100") 
    print(f"  饥饿度: {task.child_hunger}/100")
    print()
    
    print("👨‍👩‍👧‍👦 父母状态:")
    print(f"  耐心值: {task.parent_patience}/100")
    print(f"  最大回合数: {task.max_rounds}")
    print()
    
    print("🃏 可用卡牌详情:")
    for i, card in enumerate(task.cards_deck, 1):
        print(f"{i:2d}. {card.name:<12} | 类型: {card.card_type:<12} | 有效性: {card.effectiveness:2d}/10")
        print(f"     效果: {card.description}")
        if card.side_effects:
            effects = ", ".join(f"{k}: {v:+d}" for k, v in card.side_effects.items())
            print(f"     副作用: {effects}")
        print()
    
    print("🎮 开始谈判演示...")
    
    # 演示谈判回合
    round_num = 1
    while task.child_resistance > 20 and task.negotiation_rounds < 3:  # 只演示3回合
        print(f"\n--- 第 {round_num} 回合 ---")
        
        # 随机选择一张卡牌
        available_cards = [c for c in task.cards_deck if c not in task.used_cards]
        if not available_cards:
            break
            
        chosen_card = random.choice(available_cards[:5])  # 从前5张中选择
        print(f"选择卡牌: {chosen_card.name}")
        print(f"卡牌描述: {chosen_card.description}")
        
        # 计算有效性
        effectiveness = task._calculate_card_effectiveness(chosen_card)
        success_rate = min(0.9, effectiveness / 10.0)
        print(f"当前有效性: {effectiveness}/10 (成功率: {success_rate:.1%})")
        
        # 模拟卡牌使用
        task.used_cards.append(chosen_card)
        task.negotiation_rounds += 1
        
        if random.random() < success_rate:
            print("✅ 卡牌成功！")
            for effect, value in chosen_card.side_effects.items():
                if effect == "resistance":
                    old_resistance = task.child_resistance
                    task.child_resistance = max(0, min(100, task.child_resistance + value))
                    print(f"   孩子抗拒值: {old_resistance} → {task.child_resistance}")
                elif effect == "attention":
                    old_attention = task.child_attention
                    task.child_attention = max(0, min(100, task.child_attention + value))
                    print(f"   孩子注意力: {old_attention} → {task.child_attention}")
        else:
            print("❌ 卡牌失败！孩子更加抗拒了...")
            task.child_resistance = min(100, task.child_resistance + 15)
        
        # 父母耐心消耗
        task.parent_patience = max(0, task.parent_patience - 5)
        
        # 显示当前状态
        status = task.get_negotiation_status()
        print(f"回合后状态:")
        print(f"  孩子抗拒值: {status['child_resistance']}/100")
        print(f"  父母耐心值: {status['parent_patience']}/100")
        print(f"  成功概率: {status['success_probability']:.1%}")
        
        round_num += 1
    
    # 最终结果
    print(f"\n🏁 谈判结果:")
    if task.child_resistance <= 20:
        print("🎉 谈判成功！孩子同意吃西兰花了！")
        print("父母获得了宝贵的育儿经验和成就感。")
    elif task.parent_patience <= 0:
        print("😤 父母耐心耗尽，谈判失败...")
        print("有时候放弃也是一种智慧。")
    else:
        print("⏰ 演示结束，实际谈判可能还会继续...")
    
    print(f"\n📊 最终统计:")
    print(f"使用卡牌数: {len(task.used_cards)}")
    print(f"谈判回合数: {task.negotiation_rounds}")
    print(f"剩余可用卡牌: {len([c for c in task.cards_deck if c not in task.used_cards])}")
    
    print("\n🎯 谈判任务演示完成！")
    print("这个任务考验心理学知识和策略思维。")
    print("记住：好的教育方式比强制更有效！")
    print()


def demo_task_comparison():
    """对比两个特色任务的特点"""
    print("⚖️ 特色任务对比分析")
    print("=" * 50)
    
    print("🧩 后备箱俄罗斯方块 vs 🥦 挑食谈判专家")
    print()
    
    comparison = [
        ("任务类型", "空间解谜", "心理博弈"),
        ("主要技能", "空间想象力", "沟通谈判"),
        ("时间压力", "高 (出发倒计时)", "中 (孩子耐心)"),
        ("协作需求", "高 (双人配合)", "低 (单人为主)"),
        ("失败后果", "行程取消", "营养不良"),
        ("教育价值", "物理空间认知", "儿童心理学"),
        ("难度等级", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"),
        ("趣味性", "直观有趣", "策略深度"),
        ("现实相关度", "极高", "极高")
    ]
    
    print(f"{'维度':<12} | {'俄罗斯方块':<20} | {'谈判专家':<20}")
    print("-" * 60)
    for dimension, tetris, negotiation in comparison:
        print(f"{dimension:<12} | {tetris:<20} | {negotiation:<20}")
    
    print()
    print("💡 设计理念:")
    print("• 俄罗斯方块: 模拟带娃出门的物理挑战，考验空间规划能力")
    print("• 谈判专家: 模拟育儿中的心理博弈，传授科学教育方法")
    print("• 两个任务互补，覆盖育儿的物理和心理两个维度")
    print()


def main():
    """主演示函数"""
    print("🎮 特色任务模式专项演示")
    print("硬核父母岗前特训 - 高级挑战")
    print("=" * 60)
    print()
    
    demo_tetris_detailed()
    demo_negotiation_detailed()
    demo_task_comparison()
    
    print("🎊 所有特色任务演示完成！")
    print()
    print("现在你已经了解了全部四种特色任务模式：")
    print("1. 💥 生化危机：换尿布炸弹 - 非对称信息博弈")
    print("2. 🌙 午夜凶铃：睡眠剥夺战 - 极限理智挑战")
    print("3. 🧩 后备箱俄罗斯方块 - 空间解谜挑战")
    print("4. 🥦 挑食谈判专家 - 心理博弈大师")
    print()
    print("每个任务都有独特的机制和教育价值，")
    print("组合起来提供全方位的育儿技能训练！")
    print()
    print("准备好成为硬核父母了吗？ 💪")


if __name__ == "__main__":
    main()