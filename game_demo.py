#!/usr/bin/env python3
"""
硬核育儿模拟器完整演示
严格按照游戏设计文档实现
"""

from hardcore_parenting_game import (
    HardcoreParentingGame, 
    GameMode, 
    BabyPersonality, 
    TaskType
)
import random
import time


def demo_newborn_stage():
    """演示0-3月新生儿阶段"""
    print("👶 === 0-3月新生儿阶段演示 ===")
    
    game = HardcoreParentingGame()
    
    # 开始游戏：普通模式，高敏宝宝，0个月
    start_result = game.start_game(GameMode.NORMAL, BabyPersonality.FUSSY, 0)
    print(f"🎮 {start_result['message']}")
    
    # 显示初始状态
    status = game.get_game_status()
    print(f"📊 初始状态:")
    print(f"   健康值: {status['game_state']['health']}/100")
    print(f"   饥饿度: {status['game_state']['hunger']}/100")
    print(f"   清洁度: {status['game_state']['cleanliness']}/100")
    print(f"   快乐度: {status['game_state']['happiness']}/100")
    print(f"   亲密度: {status['game_state']['intimacy']}/100")
    
    # 场景1: 冲奶粉喂食任务
    print(f"\n🍼 场景1: 冲奶粉喂食任务")
    print("操作: 水温45°C(过高), 摇晃强度5, 倾斜角度45°")
    
    result = game.execute_feeding_task(
        water_temp=45.0,      # 过高温度
        shake_intensity=5,    # 正常摇晃
        tilt_angle=45        # 正常角度
    )
    
    print(f"结果: {result.message}")
    print(f"特效: {', '.join(result.special_effects)}")
    
    # 场景2: 摇晃哄睡任务
    print(f"\n😴 场景2: 摇晃哄睡任务")
    print("操作: 频率2.0Hz, 持续60秒, 未切出App")
    
    result = game.execute_sleep_task(
        shake_frequency=2.0,  # 理想频率
        duration=60,         # 足够时间
        app_switched=False   # 没有切出
    )
    
    print(f"结果: {result.message}")
    print(f"特效: {', '.join(result.special_effects)}")
    
    # 场景3: 换尿布任务
    print(f"\n💩 场景3: 换尿布任务")
    print("操作: 提腿速度6秒(慢), 擦拭彻底度8, 正确放置")
    
    result = game.execute_diaper_task(
        lift_speed=6.0,           # 动作慢，可能触发喷射
        wipe_thoroughness=8,      # 擦得很干净
        diaper_placement="correct" # 正确放置
    )
    
    print(f"结果: {result.message}")
    print(f"特效: {', '.join(result.special_effects)}")
    
    # 场景4: 选药任务
    print(f"\n💊 场景4: 选药任务 (宝宝发烧38.5°C)")
    print("操作: 选择退烧贴(正确)")
    
    result = game.execute_medicine_task("fever_patch")
    
    print(f"结果: {result.message}")
    print(f"特效: {', '.join(result.special_effects)}")
    
    # 场景5: 拥抱任务
    print(f"\n🤗 场景5: 拥抱任务")
    print("操作: 长按4.5秒")
    
    result = game.execute_hug_task(press_duration=4.5)
    
    print(f"结果: {result.message}")
    print(f"特效: {', '.join(result.special_effects)}")
    
    # 显示最终状态
    final_status = game.get_game_status()
    print(f"\n📊 最终状态:")
    print(f"   健康值: {final_status['game_state']['health']}/100")
    print(f"   饥饿度: {final_status['game_state']['hunger']}/100")
    print(f"   清洁度: {final_status['game_state']['cleanliness']}/100")
    print(f"   快乐度: {final_status['game_state']['happiness']}/100")
    print(f"   亲密度: {final_status['game_state']['intimacy']}/100")


def demo_infant_stage():
    """演示3-12月婴儿阶段"""
    print(f"\n👶 === 3-12月婴儿阶段演示 ===")
    
    game = HardcoreParentingGame()
    
    # 开始游戏：简单模式，天使宝宝，6个月
    start_result = game.start_game(GameMode.EASY, BabyPersonality.ANGEL, 6)
    print(f"🎮 {start_result['message']}")
    
    # 场景1: 叽里咕噜对话
    print(f"\n🗣️ 场景1: 叽里咕噜对话")
    print("操作: 说话包含关键词['宝宝', '乖'], 持续30秒")
    
    result = game.execute_talk_task(
        speech_keywords=["宝宝", "乖", "可爱"],
        voice_duration=30.0
    )
    
    print(f"结果: {result.message}")
    print(f"特效: {', '.join(result.special_effects)}")
    
    # 场景2: 做辅食任务 - 高敏宝宝胡萝卜陷阱
    print(f"\n🥕 场景2: 做辅食任务")
    print("操作: 选择胡萝卜(天使宝宝可以), 切菜技巧7")
    
    result = game.execute_food_task(
        food_choice="carrot",
        cutting_skill=7
    )
    
    print(f"结果: {result.message}")
    print(f"特效: {', '.join(result.special_effects)}")
    
    # 场景3: 防摔倒QTE
    print(f"\n🛡️ 场景3: 防摔倒QTE")
    print("操作: 反应时间1.5秒, 成功点击按钮")
    
    result = game.execute_safety_task(
        reaction_time=1.5,
        button_clicked=True
    )
    
    print(f"结果: {result.message}")
    print(f"特效: {', '.join(result.special_effects)}")
    
    # 场景4: 叫爹妈彩蛋
    print(f"\n🎉 场景4: 叫爹妈彩蛋")
    print("操作: 成功录制, 反应时间2.0秒")
    
    result = game.execute_first_word_task(
        recorded=True,
        reaction_time=2.0
    )
    
    print(f"结果: {result.message}")
    print(f"特效: {', '.join(result.special_effects)}")
    if result.unlock_achievements:
        print(f"🏆 解锁成就: {', '.join(result.unlock_achievements)}")


def demo_toddler_stage():
    """演示1-2岁幼儿阶段"""
    print(f"\n🚶 === 1-2岁幼儿阶段演示 ===")
    
    game = HardcoreParentingGame()
    
    # 开始游戏：普通模式，高敏宝宝，18个月
    start_result = game.start_game(GameMode.NORMAL, BabyPersonality.FUSSY, 18)
    print(f"🎮 {start_result['message']}")
    
    # 场景1: 触摸禁区任务
    print(f"\n⚡ 场景1: 触摸禁区任务")
    print("操作: 滑动方向away(正确), 危险物品插座")
    
    result = game.execute_danger_touch_task(
        swipe_direction="away",
        danger_type="插座"
    )
    
    print(f"结果: {result.message}")
    print(f"特效: {', '.join(result.special_effects)}")
    
    # 场景2: 玩具断案 - 高敏宝宝分享失败
    print(f"\n🧸 场景2: 玩具断案")
    print("操作: 选择B(引导分享) - 高敏宝宝会失败")
    
    result = game.execute_toy_conflict_task(solution_choice="B")
    
    print(f"结果: {result.message}")
    print(f"特效: {', '.join(result.special_effects)}")
    
    # 场景3: 词汇纠正任务
    print(f"\n🤬 场景3: 词汇纠正任务")
    print("操作: 孩子说'卧槽', 选择B(温和替换)")
    
    result = game.execute_bad_word_task(
        correction_method="B",
        bad_word="卧槽"
    )
    
    print(f"结果: {result.message}")
    print(f"特效: {', '.join(result.special_effects)}")


def demo_preschool_stage():
    """演示2-3岁学龄前阶段"""
    print(f"\n🎒 === 2-3岁学龄前阶段演示 ===")
    
    game = HardcoreParentingGame()
    
    # 开始游戏：简单模式，天使宝宝，30个月
    start_result = game.start_game(GameMode.EASY, BabyPersonality.ANGEL, 30)
    print(f"🎮 {start_result['message']}")
    
    # 场景1: 出门穿衣任务
    print(f"\n👕 场景1: 出门穿衣任务")
    print("操作: 完成时间45秒, 限制时间60秒")
    
    result = game.execute_dressing_task(
        completion_time=45,
        time_limit=60
    )
    
    print(f"结果: {result.message}")
    print(f"特效: {', '.join(result.special_effects)}")
    
    # 场景2: 情感对话任务
    print(f"\n💭 场景2: 情感对话任务")
    print("孩子: '妈妈，我梦见怪兽吃掉了月亮，我好怕。'")
    print("操作: 选择A(共情回应)")
    
    result = game.execute_emotion_talk_task(response_choice="A")
    
    print(f"结果: {result.message}")
    print(f"特效: {', '.join(result.special_effects)}")


def demo_hard_mode():
    """演示困难模式专属机制"""
    print(f"\n💀 === 困难模式：地狱特训演示 ===")
    
    game = HardcoreParentingGame()
    
    # 开始游戏：困难模式，高敏宝宝，1个月
    start_result = game.start_game(GameMode.HARD, BabyPersonality.FUSSY, 1)
    print(f"🎮 {start_result['message']}")
    print(f"地狱特训第{game.state.hell_week_day}天")
    
    # 场景1: 午夜凶铃
    print(f"\n🌙 场景1: 午夜凶铃")
    
    result = game.trigger_midnight_alarm()
    
    print(f"结果: {result.message}")
    print(f"特效: {', '.join(result.special_effects)}")
    
    # 场景2: 幻听系统
    print(f"\n👻 场景2: 幻听系统")
    
    # 先让孩子睡觉
    game.state.is_sleeping = True
    
    result = game.trigger_phantom_cry()
    
    print(f"结果: {result.message}")
    print(f"特效: {', '.join(result.special_effects)}")
    
    # 场景3: 幻听响应检查
    print(f"\n😰 场景3: 幻听响应检查")
    print("操作: 频繁检查屏幕6次")
    
    result = game.check_phantom_cry_response(screen_checks=6)
    
    print(f"结果: {result.message}")
    print(f"特效: {', '.join(result.special_effects)}")


def demo_personality_comparison():
    """演示性格对比"""
    print(f"\n👼 vs 😤 === 性格对比演示 ===")
    
    personalities = [
        (BabyPersonality.ANGEL, "天使宝宝"),
        (BabyPersonality.FUSSY, "高敏宝宝")
    ]
    
    for personality, name in personalities:
        print(f"\n--- {name} 辅食测试 ---")
        
        game = HardcoreParentingGame()
        game.start_game(GameMode.NORMAL, personality, 6)
        
        # 都选择胡萝卜
        result = game.execute_food_task(
            food_choice="carrot",
            cutting_skill=7
        )
        
        print(f"结果: {result.message}")
        if result.special_effects:
            print(f"特效: {', '.join(result.special_effects)}")


def demo_random_events():
    """演示随机事件系统"""
    print(f"\n🎲 === 随机事件系统演示 ===")
    
    game = HardcoreParentingGame()
    
    # 测试不同性格的事件权重
    personalities = [
        (BabyPersonality.ANGEL, "天使宝宝 (负面30%, 正面70%)"),
        (BabyPersonality.FUSSY, "高敏宝宝 (负面70%, 正面30%)")
    ]
    
    for personality, desc in personalities:
        print(f"\n--- {desc} ---")
        
        game.start_game(GameMode.NORMAL, personality, 6)
        
        # 生成10个随机事件
        events = []
        for _ in range(10):
            event = game.get_random_event()
            if event:
                events.append(event.value)
        
        print(f"随机事件: {', '.join(events)}")
        
        # 统计正负面事件比例
        positive_events = ["hug_happy", "talk_play", "first_word"]
        positive_count = sum(1 for e in events if e in positive_events)
        negative_count = len(events) - positive_count
        
        print(f"正面事件: {positive_count}/10 ({positive_count*10}%)")
        print(f"负面事件: {negative_count}/10 ({negative_count*10}%)")


def main():
    """主演示程序"""
    print("🍼 硬核育儿模拟器：完整游戏演示")
    print("严格按照游戏设计文档实现")
    print("=" * 60)
    
    # 演示各个年龄阶段
    demo_newborn_stage()
    demo_infant_stage()
    demo_toddler_stage()
    demo_preschool_stage()
    
    # 演示困难模式
    demo_hard_mode()
    
    # 演示性格对比
    demo_personality_comparison()
    
    # 演示随机事件
    demo_random_events()
    
    print(f"\n🎉 演示完成！")
    print("游戏包含:")
    print("✅ 三种游戏模式 (云养娃/实习父母/地狱特训)")
    print("✅ 两种宝宝性格 (天使宝宝/高敏宝宝)")
    print("✅ 四个年龄阶段 (0-3月/3-12月/1-2岁/2-3岁)")
    print("✅ 完整的任务系统和交互玩法")
    print("✅ 困难模式专属机制 (午夜凶铃/幻听系统)")
    print("✅ 详细的状态变化和特效系统")


if __name__ == "__main__":
    main()