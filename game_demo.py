#!/usr/bin/env python3
"""
硬核育儿模拟器完整演示
严格按照游戏设计文档实现
支持用户交互输入
"""

from hardcore_parenting_game import (
    HardcoreParentingGame, 
    GameMode, 
    BabyPersonality, 
    TaskType
)
import random
import time


def get_user_input(prompt, input_type="str", min_val=None, max_val=None, options=None):
    """
    获取用户输入
    
    Args:
        prompt: 提示信息
        input_type: 输入类型 ("str", "int", "float", "choice")
        min_val: 最小值
        max_val: 最大值
        options: 选项列表（用于choice类型）
    """
    while True:
        try:
            if input_type == "choice":
                print(f"\n{prompt}")
                for i, option in enumerate(options, 1):
                    print(f"  {i}. {option}")
                user_input = input("请输入选项编号 (直接回车使用默认): ")
                if user_input.strip() == "":
                    return None  # 使用默认值
                choice = int(user_input)
                if 1 <= choice <= len(options):
                    return choice - 1
                print("❌ 无效选择，请重新输入")
                
            elif input_type == "int":
                user_input = input(f"{prompt} (直接回车使用默认): ")
                if user_input.strip() == "":
                    return None  # 使用默认值
                value = int(user_input)
                if min_val is not None and value < min_val:
                    print(f"❌ 值不能小于 {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"❌ 值不能大于 {max_val}")
                    continue
                return value
                
            elif input_type == "float":
                user_input = input(f"{prompt} (直接回车使用默认): ")
                if user_input.strip() == "":
                    return None  # 使用默认值
                value = float(user_input)
                if min_val is not None and value < min_val:
                    print(f"❌ 值不能小于 {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"❌ 值不能大于 {max_val}")
                    continue
                return value
                
            else:  # str
                user_input = input(f"{prompt} (直接回车使用默认): ")
                if user_input.strip() == "":
                    return None
                return user_input
                
        except ValueError:
            print("❌ 输入格式错误，请重新输入")
        except KeyboardInterrupt:
            print("\n\n👋 用户取消操作")
            return None


def demo_newborn_stage():
    """演示0-3月新生儿阶段"""
    print("\n" + "="*60)
    print("👶 === 0-3月新生儿阶段演示 ===")
    print("="*60)
    
    game = HardcoreParentingGame()
    
    # 开始游戏：普通模式，高敏宝宝，0个月
    start_result = game.start_game(GameMode.NORMAL, BabyPersonality.FUSSY, 0)
    print(f"🎮 {start_result['message']}")
    
    # 显示初始状态
    status = game.get_game_status()
    print(f"\n📊 初始状态:")
    print(f"   ❤️  健康值: {status['game_state']['health']}/100")
    print(f"   🍼 饥饿度: {status['game_state']['hunger']}/100")
    print(f"   🛁 清洁度: {status['game_state']['cleanliness']}/100")
    print(f"   😊 快乐度: {status['game_state']['happiness']}/100")
    print(f"   💕 亲密度: {status['game_state']['intimacy']}/100")
    
    # 场景1: 冲奶粉喂食任务
    print(f"\n{'='*60}")
    print("🍼 场景1: 冲奶粉喂食任务")
    print("="*60)
    print("💡 提示: 理想水温 37-40°C，摇晃强度 3-7，倾斜角度 30-60°")
    
    # 用户输入
    water_temp = get_user_input(
        "请输入水温 (°C, 建议37-40)", 
        "float", 20, 60
    )
    if water_temp is None:
        water_temp = 45.0  # 默认值（过高）
        print(f"使用默认值: {water_temp}°C (过高)")
    
    shake_intensity = get_user_input(
        "请输入摇晃强度 (1-10, 建议3-7)", 
        "int", 1, 10
    )
    if shake_intensity is None:
        shake_intensity = 5
        print(f"使用默认值: {shake_intensity}")
    
    tilt_angle = get_user_input(
        "请输入倾斜角度 (度, 建议30-60)", 
        "int", 0, 90
    )
    if tilt_angle is None:
        tilt_angle = 45
        print(f"使用默认值: {tilt_angle}°")
    
    result = game.execute_feeding_task(
        water_temp=water_temp,
        shake_intensity=shake_intensity,
        tilt_angle=tilt_angle
    )
    
    print(f"\n� 结果: {result.message}")
    if result.special_effects:
        print(f"✨ 特效: {', '.join(result.special_effects)}")
    
    # 场景2: 摇晃哄睡任务
    print(f"\n{'='*60}")
    print("😴 场景2: 摇晃哄睡任务")
    print("="*60)
    print("💡 提示: 理想频率 1.5-2.5Hz，持续时间 30-120秒")
    
    shake_frequency = get_user_input(
        "请输入摇晃频率 (Hz, 建议1.5-2.5)", 
        "float", 0.5, 5.0
    )
    if shake_frequency is None:
        shake_frequency = 2.0
        print(f"使用默认值: {shake_frequency}Hz")
    
    duration = get_user_input(
        "请输入持续时间 (秒, 建议30-120)", 
        "int", 10, 300
    )
    if duration is None:
        duration = 60
        print(f"使用默认值: {duration}秒")
    
    app_switched_choice = get_user_input(
        "是否切出过App？",
        "choice",
        options=["否 (专心哄睡)", "是 (分心了)"]
    )
    app_switched = False if app_switched_choice is None else (app_switched_choice == 1)
    print(f"选择: {'是' if app_switched else '否'}")
    
    result = game.execute_sleep_task(
        shake_frequency=shake_frequency,
        duration=duration,
        app_switched=app_switched
    )
    
    print(f"\n📊 结果: {result.message}")
    if result.special_effects:
        print(f"✨ 特效: {', '.join(result.special_effects)}")
    
    # 场景3: 换尿布任务
    print(f"\n{'='*60}")
    print("💩 场景3: 换尿布任务")
    print("="*60)
    print("💡 提示: 提腿速度 < 5秒最佳，擦拭彻底度 7-10")
    
    lift_speed = get_user_input(
        "请输入提腿速度 (秒, 越快越好)", 
        "float", 1.0, 10.0
    )
    if lift_speed is None:
        lift_speed = 6.0
        print(f"使用默认值: {lift_speed}秒 (慢)")
    
    wipe_thoroughness = get_user_input(
        "请输入擦拭彻底度 (1-10)", 
        "int", 1, 10
    )
    if wipe_thoroughness is None:
        wipe_thoroughness = 8
        print(f"使用默认值: {wipe_thoroughness}")
    
    placement_choice = get_user_input(
        "尿布放置方式",
        "choice",
        options=["正确放置", "放反了", "太松了"]
    )
    placement_map = ["correct", "reversed", "loose"]
    diaper_placement = placement_map[placement_choice] if placement_choice is not None else "correct"
    print(f"选择: {['正确放置', '放反了', '太松了'][placement_choice if placement_choice is not None else 0]}")
    
    result = game.execute_diaper_task(
        lift_speed=lift_speed,
        wipe_thoroughness=wipe_thoroughness,
        diaper_placement=diaper_placement
    )
    
    print(f"\n📊 结果: {result.message}")
    if result.special_effects:
        print(f"✨ 特效: {', '.join(result.special_effects)}")
    
    # 场景4: 选药任务
    print(f"\n{'='*60}")
    print("💊 场景4: 选药任务 (宝宝发烧38.5°C)")
    print("="*60)
    
    medicine_choice = get_user_input(
        "请选择药物",
        "choice",
        options=["退烧贴 (正确)", "退烧药 (错误，太小)", "物理降温 (可以但不够)"]
    )
    medicine_map = ["fever_patch", "fever_medicine", "physical_cooling"]
    medicine = medicine_map[medicine_choice] if medicine_choice is not None else "fever_patch"
    print(f"选择: {['退烧贴', '退烧药', '物理降温'][medicine_choice if medicine_choice is not None else 0]}")
    
    result = game.execute_medicine_task(medicine)
    
    print(f"\n📊 结果: {result.message}")
    if result.special_effects:
        print(f"✨ 特效: {', '.join(result.special_effects)}")
    
    # 场景5: 拥抱任务
    print(f"\n{'='*60}")
    print("🤗 场景5: 拥抱任务")
    print("="*60)
    print("💡 提示: 长按 3-5秒 效果最佳")
    
    press_duration = get_user_input(
        "请输入长按时间 (秒)", 
        "float", 0.5, 10.0
    )
    if press_duration is None:
        press_duration = 4.5
        print(f"使用默认值: {press_duration}秒")
    
    result = game.execute_hug_task(press_duration=press_duration)
    
    print(f"\n📊 结果: {result.message}")
    if result.special_effects:
        print(f"✨ 特效: {', '.join(result.special_effects)}")
    
    # 显示最终状态
    final_status = game.get_game_status()
    print(f"\n{'='*60}")
    print("📊 最终状态:")
    print("="*60)
    print(f"   ❤️  健康值: {final_status['game_state']['health']}/100")
    print(f"   🍼 饥饿度: {final_status['game_state']['hunger']}/100")
    print(f"   🛁 清洁度: {final_status['game_state']['cleanliness']}/100")
    print(f"   😊 快乐度: {final_status['game_state']['happiness']}/100")
    print(f"   💕 亲密度: {final_status['game_state']['intimacy']}/100")


def demo_infant_stage():
    """演示3-12月婴儿阶段"""
    print(f"\n{'='*60}")
    print("👶 === 3-12月婴儿阶段演示 ===")
    print("="*60)
    
    game = HardcoreParentingGame()
    
    # 开始游戏：简单模式，天使宝宝，6个月
    start_result = game.start_game(GameMode.EASY, BabyPersonality.ANGEL, 6)
    print(f"🎮 {start_result['message']}")
    
    # 场景1: 叽里咕噜对话
    print(f"\n{'='*60}")
    print("🗣️ 场景1: 叽里咕噜对话")
    print("="*60)
    print("💡 提示: 包含关键词 '宝宝'、'乖'、'可爱' 等，持续 20-60秒")
    
    keywords_input = get_user_input(
        "请输入说话内容中包含的关键词 (用空格分隔，如: 宝宝 乖 可爱)",
        "str"
    )
    if keywords_input:
        speech_keywords = keywords_input.split()
    else:
        speech_keywords = ["宝宝", "乖", "可爱"]
        print(f"使用默认关键词: {speech_keywords}")
    
    voice_duration = get_user_input(
        "请输入说话持续时间 (秒, 建议20-60)",
        "float", 5, 120
    )
    if voice_duration is None:
        voice_duration = 30.0
        print(f"使用默认值: {voice_duration}秒")
    
    result = game.execute_talk_task(
        speech_keywords=speech_keywords,
        voice_duration=voice_duration
    )
    
    print(f"\n📊 结果: {result.message}")
    if result.special_effects:
        print(f"✨ 特效: {', '.join(result.special_effects)}")
    
    # 场景2: 做辅食任务
    print(f"\n{'='*60}")
    print("🥕 场景2: 做辅食任务")
    print("="*60)
    print("💡 提示: 天使宝宝对所有食材都友好")
    
    food_choice_idx = get_user_input(
        "请选择食材",
        "choice",
        options=["南瓜 (安全)", "胡萝卜 (天使宝宝可以)", "土豆 (安全)"]
    )
    food_map = ["pumpkin", "carrot", "potato"]
    food_choice = food_map[food_choice_idx] if food_choice_idx is not None else "carrot"
    print(f"选择: {['南瓜', '胡萝卜', '土豆'][food_choice_idx if food_choice_idx is not None else 1]}")
    
    cutting_skill = get_user_input(
        "请输入切菜技巧 (1-10)",
        "int", 1, 10
    )
    if cutting_skill is None:
        cutting_skill = 7
        print(f"使用默认值: {cutting_skill}")
    
    result = game.execute_food_task(
        food_choice=food_choice,
        cutting_skill=cutting_skill
    )
    
    print(f"\n📊 结果: {result.message}")
    if result.special_effects:
        print(f"✨ 特效: {', '.join(result.special_effects)}")
    
    # 场景3: 防摔倒QTE
    print(f"\n{'='*60}")
    print("🛡️ 场景3: 防摔倒QTE")
    print("="*60)
    print("💡 提示: 反应时间 < 2秒最佳")
    
    reaction_time = get_user_input(
        "请输入你的反应时间 (秒, 越快越好)",
        "float", 0.1, 5.0
    )
    if reaction_time is None:
        reaction_time = 1.5
        print(f"使用默认值: {reaction_time}秒")
    
    button_clicked_choice = get_user_input(
        "是否成功点击按钮？",
        "choice",
        options=["是 (成功接住)", "否 (没反应过来)"]
    )
    button_clicked = True if button_clicked_choice is None else (button_clicked_choice == 0)
    print(f"选择: {'是' if button_clicked else '否'}")
    
    result = game.execute_safety_task(
        reaction_time=reaction_time,
        button_clicked=button_clicked
    )
    
    print(f"\n📊 结果: {result.message}")
    if result.special_effects:
        print(f"✨ 特效: {', '.join(result.special_effects)}")
    
    # 场景4: 叫爹妈彩蛋
    print(f"\n{'='*60}")
    print("🎉 场景4: 叫爹妈彩蛋")
    print("="*60)
    print("💡 提示: 快速反应并录制")
    
    recorded_choice = get_user_input(
        "是否成功录制？",
        "choice",
        options=["是 (成功录制)", "否 (错过了)"]
    )
    recorded = True if recorded_choice is None else (recorded_choice == 0)
    print(f"选择: {'是' if recorded else '否'}")
    
    reaction_time = get_user_input(
        "请输入反应时间 (秒)",
        "float", 0.1, 5.0
    )
    if reaction_time is None:
        reaction_time = 2.0
        print(f"使用默认值: {reaction_time}秒")
    
    result = game.execute_first_word_task(
        recorded=recorded,
        reaction_time=reaction_time
    )
    
    print(f"\n📊 结果: {result.message}")
    if result.special_effects:
        print(f"✨ 特效: {', '.join(result.special_effects)}")
    if result.unlock_achievements:
        print(f"🏆 解锁成就: {', '.join(result.unlock_achievements)}")


def demo_toddler_stage():
    """演示1-2岁幼儿阶段"""
    print(f"\n{'='*60}")
    print("🚶 === 1-2岁幼儿阶段演示 ===")
    print("="*60)
    
    game = HardcoreParentingGame()
    
    # 开始游戏：普通模式，高敏宝宝，18个月
    start_result = game.start_game(GameMode.NORMAL, BabyPersonality.FUSSY, 18)
    print(f"🎮 {start_result['message']}")
    
    # 场景1: 触摸禁区任务
    print(f"\n{'='*60}")
    print("⚡ 场景1: 触摸禁区任务")
    print("="*60)
    print("💡 提示: 向外滑动可以拉开宝宝")
    
    danger_choice = get_user_input(
        "宝宝要摸什么危险物品？",
        "choice",
        options=["插座", "刀具", "热水壶"]
    )
    danger_map = ["插座", "刀具", "热水壶"]
    danger_type = danger_map[danger_choice] if danger_choice is not None else "插座"
    print(f"选择: {danger_type}")
    
    swipe_choice = get_user_input(
        "你的操作",
        "choice",
        options=["向外滑动 (正确，拉开宝宝)", "向内滑动 (错误，推向危险)"]
    )
    swipe_direction = "away" if (swipe_choice is None or swipe_choice == 0) else "toward"
    print(f"选择: {'向外滑动' if swipe_direction == 'away' else '向内滑动'}")
    
    result = game.execute_danger_touch_task(
        swipe_direction=swipe_direction,
        danger_type=danger_type
    )
    
    print(f"\n📊 结果: {result.message}")
    if result.special_effects:
        print(f"✨ 特效: {', '.join(result.special_effects)}")
    
    # 场景2: 玩具断案
    print(f"\n{'='*60}")
    print("🧸 场景2: 玩具断案")
    print("="*60)
    print("💡 提示: 高敏宝宝不容易分享")
    
    solution_choice_idx = get_user_input(
        "请选择解决方案",
        "choice",
        options=["A: 强制分享", "B: 引导分享", "C: 转移注意力"]
    )
    solution_map = ["A", "B", "C"]
    solution_choice = solution_map[solution_choice_idx] if solution_choice_idx is not None else "B"
    print(f"选择: {solution_choice}")
    
    result = game.execute_toy_conflict_task(solution_choice=solution_choice)
    
    print(f"\n📊 结果: {result.message}")
    if result.special_effects:
        print(f"✨ 特效: {', '.join(result.special_effects)}")
    
    # 场景3: 词汇纠正任务
    print(f"\n{'='*60}")
    print("🤬 场景3: 词汇纠正任务")
    print("="*60)
    print("孩子说了不当词汇: '卧槽'")
    
    correction_choice_idx = get_user_input(
        "请选择纠正方法",
        "choice",
        options=["A: 严厉批评", "B: 温和替换", "C: 忽略不管"]
    )
    correction_map = ["A", "B", "C"]
    correction_method = correction_map[correction_choice_idx] if correction_choice_idx is not None else "B"
    print(f"选择: {correction_method}")
    
    result = game.execute_bad_word_task(
        correction_method=correction_method,
        bad_word="卧槽"
    )
    
    print(f"\n📊 结果: {result.message}")
    if result.special_effects:
        print(f"✨ 特效: {', '.join(result.special_effects)}")


def demo_preschool_stage():
    """演示2-3岁学龄前阶段"""
    print(f"\n{'='*60}")
    print("🎒 === 2-3岁学龄前阶段演示 ===")
    print("="*60)
    
    game = HardcoreParentingGame()
    
    # 开始游戏：简单模式，天使宝宝，30个月
    start_result = game.start_game(GameMode.EASY, BabyPersonality.ANGEL, 30)
    print(f"🎮 {start_result['message']}")
    
    # 场景1: 出门穿衣任务
    print(f"\n{'='*60}")
    print("👕 场景1: 出门穿衣任务")
    print("="*60)
    print("💡 提示: 在限制时间内完成，越快越好")
    
    time_limit = get_user_input(
        "请输入限制时间 (秒)",
        "int", 30, 120
    )
    if time_limit is None:
        time_limit = 60
        print(f"使用默认值: {time_limit}秒")
    
    completion_time = get_user_input(
        f"请输入实际完成时间 (秒, 不超过{time_limit})",
        "int", 10, time_limit
    )
    if completion_time is None:
        completion_time = 45
        print(f"使用默认值: {completion_time}秒")
    
    result = game.execute_dressing_task(
        completion_time=completion_time,
        time_limit=time_limit
    )
    
    print(f"\n📊 结果: {result.message}")
    if result.special_effects:
        print(f"✨ 特效: {', '.join(result.special_effects)}")
    
    # 场景2: 情感对话任务
    print(f"\n{'='*60}")
    print("💭 场景2: 情感对话任务")
    print("="*60)
    print("孩子说: '妈妈，我梦见怪兽吃掉了月亮，我好怕。'")
    
    response_choice_idx = get_user_input(
        "请选择回应方式",
        "choice",
        options=[
            "A: 共情回应 ('宝宝害怕了对吗？妈妈抱抱')",
            "B: 讲道理 ('那是梦，不是真的')",
            "C: 转移话题 ('我们去玩玩具吧')"
        ]
    )
    response_map = ["A", "B", "C"]
    response_choice = response_map[response_choice_idx] if response_choice_idx is not None else "A"
    print(f"选择: {response_choice}")
    
    result = game.execute_emotion_talk_task(response_choice=response_choice)
    
    print(f"\n📊 结果: {result.message}")
    if result.special_effects:
        print(f"✨ 特效: {', '.join(result.special_effects)}")


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
    print("="*60)
    print("🍼 硬核育儿模拟器：完整游戏演示")
    print("严格按照游戏设计文档实现")
    print("="*60)
    print("\n💡 提示: 每个任务都可以输入参数，直接回车使用默认值\n")
    
    # 让用户选择要演示的阶段
    stage_choice = get_user_input(
        "请选择要演示的阶段 (可多选，用空格分隔，如: 1 2 3)",
        "choice",
        options=[
            "1. 0-3月新生儿阶段",
            "2. 3-12月婴儿阶段",
            "3. 1-2岁幼儿阶段",
            "4. 2-3岁学龄前阶段",
            "5. 困难模式演示",
            "6. 性格对比演示",
            "7. 随机事件演示",
            "8. 全部演示"
        ]
    )
    
    # 如果用户选择全部或没有输入，运行所有演示
    if stage_choice is None or stage_choice == 7:
        print("\n� 开始全部演示...\n")
        demo_newborn_stage()
        demo_infant_stage()
        demo_toddler_stage()
        demo_preschool_stage()
        demo_hard_mode()
        demo_personality_comparison()
        demo_random_events()
    else:
        # 根据选择运行对应演示
        if stage_choice == 0:
            demo_newborn_stage()
        elif stage_choice == 1:
            demo_infant_stage()
        elif stage_choice == 2:
            demo_toddler_stage()
        elif stage_choice == 3:
            demo_preschool_stage()
        elif stage_choice == 4:
            demo_hard_mode()
        elif stage_choice == 5:
            demo_personality_comparison()
        elif stage_choice == 6:
            demo_random_events()
    
    print(f"\n{'='*60}")
    print("🎉 演示完成！")
    print("="*60)
    print("\n游戏包含:")
    print("✅ 三种游戏模式 (云养娃/实习父母/地狱特训)")
    print("✅ 两种宝宝性格 (天使宝宝/高敏宝宝)")
    print("✅ 四个年龄阶段 (0-3月/3-12月/1-2岁/2-3岁)")
    print("✅ 完整的任务系统和交互玩法")
    print("✅ 困难模式专属机制 (午夜凶铃/幻听系统)")
    print("✅ 详细的状态变化和特效系统")
    print("✅ 用户交互输入，真实体验游戏")
    print("="*60)


if __name__ == "__main__":
    main()