#!/usr/bin/env python3
"""
硬核育儿模拟器 - 交互式演示
允许用户输入参数，体验真实游戏玩法
"""

from hardcore_parenting_game import (
    HardcoreParentingGame, 
    GameMode, 
    BabyPersonality
)


def get_user_choice(prompt, options):
    """获取用户选择"""
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    while True:
        try:
            choice = int(input("请输入选项编号: "))
            if 1 <= choice <= len(options):
                return choice - 1
            print("❌ 无效选择，请重新输入")
        except ValueError:
            print("❌ 请输入数字")


def get_float_input(prompt, min_val=None, max_val=None):
    """获取浮点数输入"""
    while True:
        try:
            value = float(input(f"{prompt}: "))
            if min_val is not None and value < min_val:
                print(f"❌ 值不能小于 {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"❌ 值不能大于 {max_val}")
                continue
            return value
        except ValueError:
            print("❌ 请输入有效的数字")


def get_int_input(prompt, min_val=None, max_val=None):
    """获取整数输入"""
    while True:
        try:
            value = int(input(f"{prompt}: "))
            if min_val is not None and value < min_val:
                print(f"❌ 值不能小于 {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"❌ 值不能大于 {max_val}")
                continue
            return value
        except ValueError:
            print("❌ 请输入有效的整数")


def print_result(result):
    """打印任务结果"""
    print(f"\n{'='*60}")
    print(f"📊 任务结果: {result.message}")
    if result.special_effects:
        print(f"✨ 特效: {', '.join(result.special_effects)}")
    if result.unlock_achievements:
        print(f"🏆 解锁成就: {', '.join(result.unlock_achievements)}")
    print(f"{'='*60}")


def print_status(game):
    """打印游戏状态"""
    status = game.get_game_status()
    state = status['game_state']
    print(f"\n📊 当前状态:")
    print(f"   ❤️  健康值: {state['health']}/100")
    print(f"   🍼 饥饿度: {state['hunger']}/100")
    print(f"   🛁 清洁度: {state['cleanliness']}/100")
    print(f"   😊 快乐度: {state['happiness']}/100")
    print(f"   💕 亲密度: {state['intimacy']}/100")


def demo_feeding_task(game):
    """冲奶粉喂食任务"""
    print("\n" + "="*60)
    print("🍼 冲奶粉喂食任务")
    print("="*60)
    print("提示: 理想水温 37-40°C，摇晃强度 3-7，倾斜角度 30-60°")
    
    water_temp = get_float_input("请输入水温 (°C, 建议37-40)", 20, 60)
    shake_intensity = get_int_input("请输入摇晃强度 (1-10, 建议3-7)", 1, 10)
    tilt_angle = get_int_input("请输入倾斜角度 (度, 建议30-60)", 0, 90)
    
    result = game.execute_feeding_task(
        water_temp=water_temp,
        shake_intensity=shake_intensity,
        tilt_angle=tilt_angle
    )
    
    print_result(result)
    print_status(game)


def demo_sleep_task(game):
    """摇晃哄睡任务"""
    print("\n" + "="*60)
    print("😴 摇晃哄睡任务")
    print("="*60)
    print("提示: 理想频率 1.5-2.5Hz，持续时间 30-120秒")
    
    shake_frequency = get_float_input("请输入摇晃频率 (Hz, 建议1.5-2.5)", 0.5, 5.0)
    duration = get_int_input("请输入持续时间 (秒, 建议30-120)", 10, 300)
    
    app_switched_choice = get_user_choice(
        "是否切出过App？",
        ["否 (专心哄睡)", "是 (分心了)"]
    )
    app_switched = app_switched_choice == 1
    
    result = game.execute_sleep_task(
        shake_frequency=shake_frequency,
        duration=duration,
        app_switched=app_switched
    )
    
    print_result(result)
    print_status(game)


def demo_diaper_task(game):
    """换尿布任务"""
    print("\n" + "="*60)
    print("💩 换尿布任务")
    print("="*60)
    print("提示: 提腿速度 < 5秒最佳，擦拭彻底度 7-10")
    
    lift_speed = get_float_input("请输入提腿速度 (秒, 越快越好)", 1.0, 10.0)
    wipe_thoroughness = get_int_input("请输入擦拭彻底度 (1-10)", 1, 10)
    
    placement_choice = get_user_choice(
        "尿布放置方式",
        ["正确放置", "放反了", "太松了"]
    )
    placement_map = ["correct", "reversed", "loose"]
    diaper_placement = placement_map[placement_choice]
    
    result = game.execute_diaper_task(
        lift_speed=lift_speed,
        wipe_thoroughness=wipe_thoroughness,
        diaper_placement=diaper_placement
    )
    
    print_result(result)
    print_status(game)


def demo_medicine_task(game):
    """选药任务"""
    print("\n" + "="*60)
    print("💊 选药任务")
    print("="*60)
    print("宝宝发烧 38.5°C，请选择合适的药物")
    
    medicine_choice = get_user_choice(
        "请选择药物",
        ["退烧贴 (正确)", "退烧药 (错误，太小)", "物理降温 (可以但不够)"]
    )
    medicine_map = ["fever_patch", "fever_medicine", "physical_cooling"]
    medicine = medicine_map[medicine_choice]
    
    result = game.execute_medicine_task(medicine)
    
    print_result(result)
    print_status(game)


def demo_hug_task(game):
    """拥抱任务"""
    print("\n" + "="*60)
    print("🤗 拥抱任务")
    print("="*60)
    print("提示: 长按 3-5秒 效果最佳")
    
    press_duration = get_float_input("请输入长按时间 (秒)", 0.5, 10.0)
    
    result = game.execute_hug_task(press_duration=press_duration)
    
    print_result(result)
    print_status(game)


def demo_talk_task(game):
    """叽里咕噜对话任务"""
    print("\n" + "="*60)
    print("🗣️ 叽里咕噜对话任务")
    print("="*60)
    print("提示: 包含关键词 '宝宝'、'乖'、'可爱' 等，持续 20-60秒")
    
    print("\n请输入说话内容中包含的关键词 (用空格分隔):")
    keywords_input = input("例如: 宝宝 乖 可爱\n> ")
    speech_keywords = keywords_input.split()
    
    voice_duration = get_float_input("请输入说话持续时间 (秒)", 5, 120)
    
    result = game.execute_talk_task(
        speech_keywords=speech_keywords,
        voice_duration=voice_duration
    )
    
    print_result(result)
    print_status(game)


def demo_food_task(game):
    """做辅食任务"""
    print("\n" + "="*60)
    print("🥕 做辅食任务")
    print("="*60)
    
    if game.state.personality == BabyPersonality.FUSSY:
        print("⚠️  注意: 高敏宝宝对胡萝卜过敏！")
    
    food_choice_idx = get_user_choice(
        "请选择食材",
        ["南瓜 (安全)", "胡萝卜 (高敏宝宝会过敏)", "土豆 (安全)"]
    )
    food_map = ["pumpkin", "carrot", "potato"]
    food_choice = food_map[food_choice_idx]
    
    cutting_skill = get_int_input("请输入切菜技巧 (1-10)", 1, 10)
    
    result = game.execute_food_task(
        food_choice=food_choice,
        cutting_skill=cutting_skill
    )
    
    print_result(result)
    print_status(game)


def demo_safety_task(game):
    """防摔倒QTE任务"""
    print("\n" + "="*60)
    print("🛡️ 防摔倒QTE任务")
    print("="*60)
    print("宝宝要摔倒了！快速反应！")
    
    reaction_time = get_float_input("请输入你的反应时间 (秒, 越快越好)", 0.1, 5.0)
    
    button_clicked_choice = get_user_choice(
        "是否成功点击按钮？",
        ["是 (成功接住)", "否 (没反应过来)"]
    )
    button_clicked = button_clicked_choice == 0
    
    result = game.execute_safety_task(
        reaction_time=reaction_time,
        button_clicked=button_clicked
    )
    
    print_result(result)
    print_status(game)


def demo_danger_touch_task(game):
    """触摸禁区任务"""
    print("\n" + "="*60)
    print("⚡ 触摸禁区任务")
    print("="*60)
    print("宝宝要摸危险物品了！")
    
    danger_choice = get_user_choice(
        "宝宝要摸什么？",
        ["插座", "刀具", "热水壶"]
    )
    danger_map = ["插座", "刀具", "热水壶"]
    danger_type = danger_map[danger_choice]
    
    swipe_choice = get_user_choice(
        "你的操作",
        ["向外滑动 (正确，拉开宝宝)", "向内滑动 (错误，推向危险)"]
    )
    swipe_direction = "away" if swipe_choice == 0 else "toward"
    
    result = game.execute_danger_touch_task(
        swipe_direction=swipe_direction,
        danger_type=danger_type
    )
    
    print_result(result)
    print_status(game)


def main():
    """主程序"""
    print("🍼 硬核育儿模拟器 - 交互式演示")
    print("="*60)
    
    # 选择游戏模式
    mode_choice = get_user_choice(
        "请选择游戏模式",
        ["简单模式 (云养娃)", "普通模式 (实习父母)", "困难模式 (地狱特训)"]
    )
    modes = [GameMode.EASY, GameMode.NORMAL, GameMode.HARD]
    game_mode = modes[mode_choice]
    
    # 选择宝宝性格
    personality_choice = get_user_choice(
        "请选择宝宝性格",
        ["天使宝宝 (好带)", "高敏宝宝 (难带)"]
    )
    personalities = [BabyPersonality.ANGEL, BabyPersonality.FUSSY]
    baby_personality = personalities[personality_choice]
    
    # 选择宝宝年龄
    age = get_int_input("请输入宝宝年龄 (月, 0-36)", 0, 36)
    
    # 开始游戏
    game = HardcoreParentingGame()
    start_result = game.start_game(game_mode, baby_personality, age)
    
    print(f"\n🎮 {start_result['message']}")
    print_status(game)
    
    # 根据年龄阶段提供不同任务
    age_stage = game.state.age_stage.value
    
    # 任务菜单
    while True:
        print("\n" + "="*60)
        print("📋 可用任务")
        print("="*60)
        
        tasks = []
        
        if "0-3months" in age_stage:
            tasks = [
                ("冲奶粉喂食", demo_feeding_task),
                ("摇晃哄睡", demo_sleep_task),
                ("换尿布", demo_diaper_task),
                ("选药", demo_medicine_task),
                ("拥抱", demo_hug_task)
            ]
        elif "3-12months" in age_stage:
            tasks = [
                ("叽里咕噜对话", demo_talk_task),
                ("做辅食", demo_food_task),
                ("防摔倒QTE", demo_safety_task),
                ("拥抱", demo_hug_task)
            ]
        elif "1-2years" in age_stage:
            tasks = [
                ("触摸禁区", demo_danger_touch_task),
                ("做辅食", demo_food_task),
                ("拥抱", demo_hug_task)
            ]
        else:  # 2-3岁
            tasks = [
                ("做辅食", demo_food_task),
                ("对话", demo_talk_task),
                ("拥抱", demo_hug_task)
            ]
        
        tasks.append(("查看状态", lambda g: print_status(g)))
        tasks.append(("退出游戏", None))
        
        task_names = [t[0] for t in tasks]
        choice = get_user_choice("请选择任务", task_names)
        
        if tasks[choice][1] is None:
            print("\n👋 感谢游玩！")
            break
        
        tasks[choice][1](game)
        
        # 检查游戏是否结束
        status = game.get_game_status()
        if status['game_state']['health'] <= 0:
            print("\n💀 游戏结束！宝宝健康值归零！")
            break


if __name__ == "__main__":
    main()
