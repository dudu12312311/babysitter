"""
育儿模拟器简化演示
不依赖异步，展示核心功能
"""

from hardcore_parenting_simulator import (
    GameState, GameMode, ActionType, EventType, PlayerAction,
    CryingTask, ExplosiveDiaperTask, MidnightTerrorTask, 
    StrollerTetrisTask, PickyEaterNegotiationTask,
    GameEventManager, ScoringSystem, AchievementSystem,
    TetrisItem, NegotiationCard
)
from datetime import datetime


def demo_game_state():
    """演示游戏状态"""
    print("🍼 游戏状态演示")
    print("=" * 40)
    
    state = GameState()
    print(f"初始状态:")
    print(f"  宝宝舒适度: {state.comfort}")
    print(f"  父母理智值: {state.sanity}")
    print(f"  育儿KPI: {state.parenting_kpi}")
    print(f"  游戏模式: {state.game_mode.value}")
    print()


def demo_event_system():
    """演示事件系统"""
    print("🚨 事件系统演示")
    print("=" * 40)
    
    event_manager = GameEventManager()
    
    # 触发哭闹事件
    crying_event = event_manager.trigger_event(EventType.CRYING, severity=6)
    print(f"触发事件: {crying_event.description}")
    print(f"事件ID: {crying_event.id}")
    print(f"严重程度: {crying_event.severity}/10")
    print(f"持续时间: {crying_event.duration}秒")
    print(f"需要行动: {[action.value for action in crying_event.required_actions]}")
    print()
    
    # 触发生化危机事件
    explosive_event = event_manager.trigger_event(EventType.EXPLOSIVE_DIAPER, severity=9)
    print(f"💥 {explosive_event.description}")
    print(f"这是高难度事件！严重程度: {explosive_event.severity}/10")
    print()
    
    # 触发俄罗斯方块事件
    tetris_event = event_manager.trigger_event(EventType.STROLLER_TETRIS, severity=7)
    print(f"🧩 {tetris_event.description}")
    print(f"需要在限时内完成打包！")
    print()
    
    # 触发挑食谈判事件
    negotiation_event = event_manager.trigger_event(EventType.PICKY_EATER_NEGOTIATION, severity=8)
    print(f"🥦 {negotiation_event.description}")
    print(f"这是一场心理博弈！")
    print()


def demo_task_execution():
    """演示任务执行"""
    print("⚡ 任务执行演示")
    print("=" * 40)
    
    # 创建任务和状态
    crying_task = CryingTask()
    game_state = GameState()
    
    print(f"执行前状态 - 舒适度: {game_state.comfort}, 理智值: {game_state.sanity}")
    
    # 创建玩家行动（快速响应）
    quick_action = PlayerAction(
        action_type=ActionType.COMFORT,
        response_time=25.0,  # 25秒快速响应
        success=True,
        player_id="demo_player"
    )
    
    # 验证行动
    is_valid = crying_task.validate_action(quick_action, game_state)
    print(f"行动验证: {'有效' if is_valid else '无效'}")
    
    # 计算分数影响
    score_impact = crying_task.calculate_score_impact(quick_action, game_state)
    print(f"分数影响: {score_impact}")
    print()


def demo_explosive_diaper():
    """演示生化危机任务"""
    print("💀 生化危机演示")
    print("=" * 40)
    
    explosive_task = ExplosiveDiaperTask()
    game_state = GameState()
    
    print("场景：凌晨3点，突然听到一声巨响...")
    print(f"初始状态 - 舒适度: {game_state.comfort}, KPI: {game_state.parenting_kpi}")
    
    # 模拟慌乱的处理
    panicked_action = PlayerAction(
        action_type=ActionType.CHANGE_DIAPER,
        response_time=95.0,  # 慌乱中用了95秒
        success=False,  # 搞砸了
        player_id="panicked_parent"
    )
    
    score_impact = explosive_task.calculate_score_impact(panicked_action, game_state)
    print(f"慌乱处理结果 - 分数影响: {score_impact}")
    print("💔 结果：弄得到处都是，需要重新清理...")
    print()


def demo_midnight_terror():
    """演示午夜恐怖"""
    print("🌙 午夜恐怖演示")
    print("=" * 40)
    
    midnight_task = MidnightTerrorTask()
    game_state = GameState()
    game_state.sanity = 25  # 设置低理智值
    
    print(f"凌晨3:00，理智值已降至: {game_state.sanity}")
    
    if midnight_task.is_hallucinating(game_state):
        print("👻 警告：理智值过低，开始出现幻觉！")
        print("屏幕开始出现重影，操作变得迟钝...")
    
    # 疲惫状态下的响应
    tired_action = PlayerAction(
        action_type=ActionType.ROCK_TO_SLEEP,
        response_time=180.0,  # 疲惫中响应较慢
        success=True,
        player_id="exhausted_parent"
    )
    
    score_impact = midnight_task.calculate_score_impact(tired_action, game_state)
    print(f"疲惫状态处理 - 分数影响: {score_impact}")
    print()


def demo_stroller_tetris():
    """演示后备箱俄罗斯方块"""
    print("🧩 后备箱俄罗斯方块演示")
    print("=" * 40)
    
    tetris_task = StrollerTetrisTask()
    game_state = GameState()
    
    print("场景：准备出门，需要把所有东西塞进后备箱...")
    print(f"后备箱尺寸: {tetris_task.trunk_size[0]}x{tetris_task.trunk_size[1]}")
    print(f"需要打包的物品: {len(tetris_task.items)}件")
    
    # 显示物品列表
    for item in tetris_task.items[:3]:  # 只显示前3个
        print(f"  • {item.name} (优先级: {item.priority})")
    print("  • ...")
    
    # 模拟旋转物品
    rotate_action = PlayerAction(
        action_type=ActionType.ROTATE_ITEM,
        response_time=5.0,
        success=True,
        player_id="tetris_player",
        extra_data={"item_name": "婴儿车"}
    )
    
    print(f"\n尝试旋转婴儿车...")
    print(f"旋转前角度: {tetris_task.items[0].rotation}°")
    # 这里只是演示，实际需要异步执行
    tetris_task.items[0].rotation = (tetris_task.items[0].rotation + 90) % 360
    print(f"旋转后角度: {tetris_task.items[0].rotation}°")
    
    # 获取打包进度
    progress = tetris_task.get_packing_progress()
    print(f"当前进度: {progress['progress']:.1%}")
    print(f"剩余物品: {len(progress['remaining_items'])}件")
    print()


def demo_picky_eater_negotiation():
    """演示挑食谈判专家"""
    print("🥦 挑食谈判专家演示")
    print("=" * 40)
    
    negotiation_task = PickyEaterNegotiationTask()
    game_state = GameState()
    
    print(f"目标：让孩子吃{negotiation_task.target_food}")
    print(f"孩子抗拒值: {negotiation_task.child_resistance}/100")
    print(f"父母耐心值: {negotiation_task.parent_patience}/100")
    print()
    
    print("可用卡牌:")
    for card in negotiation_task.cards_deck[:5]:  # 显示前5张卡
        print(f"  🃏 {card.name} (有效性: {card.effectiveness}/10)")
        print(f"     {card.description}")
    print("  🃏 ...")
    print()
    
    # 模拟使用"飞机勺"卡牌
    airplane_card = negotiation_task.cards_deck[0]  # 飞机勺
    print(f"使用卡牌: {airplane_card.name}")
    print(f"卡牌描述: {airplane_card.description}")
    
    # 计算效果
    effectiveness = negotiation_task._calculate_card_effectiveness(airplane_card)
    success_rate = min(0.9, effectiveness / 10.0)
    print(f"成功率: {success_rate:.1%}")
    
    # 模拟结果
    if random.random() < success_rate:
        print("✅ 卡牌成功！孩子的抗拒值下降了！")
        negotiation_task.child_resistance = max(0, negotiation_task.child_resistance - 15)
    else:
        print("❌ 卡牌失败！孩子更加抗拒了...")
        negotiation_task.child_resistance = min(100, negotiation_task.child_resistance + 15)
    
    status = negotiation_task.get_negotiation_status()
    print(f"谈判后状态:")
    print(f"  孩子抗拒值: {status['child_resistance']}/100")
    print(f"  成功概率: {status['success_probability']:.1%}")
    print(f"  剩余回合: {status['rounds_remaining']}")
    print()


def demo_scoring_system():
    """演示评分系统"""
    print("📊 评分系统演示")
    print("=" * 40)
    
    scoring = ScoringSystem()
    
    # 模拟一些行动记录
    actions = [
        PlayerAction(ActionType.COMFORT, 20.0, True, "player1"),
        PlayerAction(ActionType.CHANGE_DIAPER, 45.0, True, "player1"),
        PlayerAction(ActionType.FEED, 90.0, False, "player1"),
    ]
    
    game_state = GameState()
    game_state.parenting_kpi = 75
    game_state.sanity = 60
    
    kpi_score = scoring.calculate_kpi(game_state, actions)
    feedback = scoring.get_performance_feedback(kpi_score)
    
    print(f"当前KPI分数: {kpi_score}")
    print(f"表现反馈: {feedback}")
    print()


def demo_achievements():
    """演示成就系统"""
    print("🏆 成就系统演示")
    print("=" * 40)
    
    achievement_system = AchievementSystem()
    
    # 模拟玩家统计数据
    player_stats = {
        "explosive_diaper_perfect": 1,  # 完美处理生化危机
        "hard_mode_days": 5,           # 困难模式天数
        "min_sanity": 45,              # 最低理智值
        "earned_achievements": []       # 已获得成就
    }
    
    print("检查可获得的成就...")
    new_achievements = achievement_system.check_achievements(player_stats)
    
    if new_achievements:
        print("🎉 恭喜获得新成就:")
        for achievement_id in new_achievements:
            achievement = achievement_system.achievements[achievement_id]
            print(f"  🏅 {achievement['name']}: {achievement['description']}")
    else:
        print("暂无新成就，继续努力！")
    
    print("\n所有可用成就:")
    for achievement_id, achievement in achievement_system.achievements.items():
        print(f"  • {achievement['name']}: {achievement['description']}")
    print()


def demo_game_modes():
    """演示游戏模式"""
    print("🎮 游戏模式对比")
    print("=" * 40)
    
    from hardcore_parenting_simulator import GameModeManager
    mode_manager = GameModeManager()
    
    modes = [
        (GameMode.EASY, "云养娃 - 适合观光客"),
        (GameMode.NORMAL, "实习父母 - 平衡体验"),
        (GameMode.HARD, "地狱特训 - 硬核挑战")
    ]
    
    for mode, description in modes:
        config = mode_manager.get_mode_config(mode)
        print(f"{description}:")
        print(f"  事件频率: {config['event_frequency']}x")
        print(f"  夜间保护: {'是' if config.get('night_protection', False) else '否'}")
        print(f"  离线暂停: {'是' if config.get('offline_pause', False) else '否'}")
        print(f"  理智衰减: {config['sanity_decay_rate']}x")
        
        if mode == GameMode.HARD:
            print(f"  强制通知: {'是' if config.get('force_notifications', False) else '否'}")
            print(f"  睡眠干扰: {'是' if config.get('sleep_disruption', False) else '否'}")
        print()


def main():
    """主演示函数"""
    print("🍼 硬核父母岗前特训 - 系统功能演示")
    print("在只要孩子不哭，尊严算什么？")
    print("=" * 60)
    print()
    
    # 运行各种演示
    demo_game_state()
    demo_event_system()
    demo_task_execution()
    demo_explosive_diaper()
    demo_midnight_terror()
    demo_stroller_tetris()
    demo_picky_eater_negotiation()
    demo_scoring_system()
    demo_achievements()
    demo_game_modes()
    
    print("🎯 演示完成！")
    print("这个系统提供了完整的育儿模拟体验：")
    print("• 三种难度模式适应不同需求")
    print("• 四种特色任务模式：")
    print("  - 生化危机：换尿布炸弹")
    print("  - 午夜凶铃：睡眠剥夺战")
    print("  - 后备箱俄罗斯方块：出行打包解谜")
    print("  - 挑食谈判专家：卡牌对战系统")
    print("• 科学的评分和反馈机制")
    print("• 丰富的成就和进度系统")
    print("• 支持多人协作训练")
    print()
    print("准备好接受硬核父母的挑战了吗？ 💪")


if __name__ == "__main__":
    main()