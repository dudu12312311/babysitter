"""
育儿模拟器使用示例
演示如何使用硬核育儿模拟器的各种功能
"""

import asyncio
from datetime import datetime
from hardcore_parenting_simulator import (
    HardcoreParentingSimulator, 
    GameMode, 
    ActionType, 
    PlayerAction,
    EventType
)


async def demo_basic_gameplay():
    """基础游戏流程演示"""
    print("🍼 欢迎来到硬核父母岗前特训！")
    print("=" * 50)
    
    # 创建游戏实例
    simulator = HardcoreParentingSimulator()
    
    # 开始游戏（普通模式）
    player_id = "player_001"
    initial_state = await simulator.start_game(player_id, GameMode.NORMAL)
    
    print(f"游戏开始！初始状态：")
    print(f"宝宝舒适度: {initial_state.comfort}")
    print(f"父母理智值: {initial_state.sanity}")
    print(f"育儿KPI: {initial_state.parenting_kpi}")
    print()
    
    # 触发一个哭闹事件
    crying_event = simulator.event_manager.trigger_event(EventType.CRYING, severity=6)
    print(f"🚨 事件触发: {crying_event.description}")
    print(f"严重程度: {crying_event.severity}/10")
    print(f"需要行动: {[action.value for action in crying_event.required_actions]}")
    print()
    
    # 玩家响应（快速响应）
    quick_action = PlayerAction(
        action_type=ActionType.COMFORT,
        response_time=25.0,  # 25秒响应
        success=True,
        player_id=player_id
    )
    
    result = await simulator.process_action(player_id, quick_action)
    print(f"快速响应结果:")
    print(f"成功: {result['success']}")
    print(f"反馈: {result['message']}")
    print(f"分数影响: {result['score_impact']}")
    print(f"新状态 - 舒适度: {result['new_state'].comfort}, 理智值: {result['new_state'].sanity}")
    print()


async def demo_explosive_diaper():
    """生化危机模式演示"""
    print("💥 生化危机：换尿布炸弹演示")
    print("=" * 50)
    
    simulator = HardcoreParentingSimulator()
    player_id = "player_002"
    
    await simulator.start_game(player_id, GameMode.HARD)
    
    # 触发炸屎事件
    explosive_event = simulator.event_manager.trigger_event(EventType.EXPLOSIVE_DIAPER, severity=9)
    print(f"💀 {explosive_event.description}")
    print(f"这是一个高难度事件，需要精确操作！")
    print()
    
    # 模拟慌乱的处理（响应较慢）
    panicked_action = PlayerAction(
        action_type=ActionType.CHANGE_DIAPER,
        response_time=95.0,  # 慌乱中用了95秒
        success=False,  # 搞砸了
        player_id=player_id
    )
    
    result = await simulator.process_action(player_id, panicked_action)
    print(f"慌乱处理结果:")
    print(f"反馈: {result['message']}")
    print(f"分数影响: {result['score_impact']}")
    print(f"当前KPI: {result['new_state'].parenting_kpi}")
    print()


async def demo_midnight_terror():
    """午夜凶铃演示"""
    print("🌙 午夜凶铃：睡眠剥夺战演示")
    print("=" * 50)
    
    simulator = HardcoreParentingSimulator()
    player_id = "player_003"
    
    # 开始困难模式
    game_state = await simulator.start_game(player_id, GameMode.HARD)
    
    # 先降低理智值模拟疲劳状态
    simulator.game_state.sanity = 25  # 低理智值
    
    # 触发午夜恐怖事件
    midnight_event = simulator.event_manager.trigger_event(EventType.MIDNIGHT_TERROR, severity=8)
    print(f"😱 {midnight_event.description}")
    print(f"当前理智值: {simulator.game_state.sanity} (已进入幻觉状态)")
    print()
    
    # 检查是否出现幻觉
    midnight_task = simulator.task_handlers[EventType.MIDNIGHT_TERROR]
    if midnight_task.is_hallucinating(simulator.game_state):
        print("👻 警告：理智值过低，开始出现幻觉！操作可能会出现偏差！")
    
    # 疲惫状态下的响应
    tired_action = PlayerAction(
        action_type=ActionType.ROCK_TO_SLEEP,
        response_time=180.0,  # 疲惫中响应较慢
        success=True,
        player_id=player_id
    )
    
    result = await simulator.process_action(player_id, tired_action)
    print(f"疲惫状态处理结果:")
    print(f"反馈: {result['message']}")
    print(f"理智值变化: {simulator.game_state.sanity}")
    print()


async def demo_achievement_system():
    """成就系统演示"""
    print("🏆 成就系统演示")
    print("=" * 50)
    
    simulator = HardcoreParentingSimulator()
    player_id = "achievement_hunter"
    
    await simulator.start_game(player_id, GameMode.HARD)
    
    # 模拟完美处理生化危机事件
    simulator.player_stats[player_id]["explosive_diaper_perfect"] = 1
    
    # 检查成就
    achievements = simulator.achievement_system.check_achievements(simulator.player_stats[player_id])
    
    if achievements:
        print(f"🎉 恭喜获得成就: {achievements}")
        for achievement_id in achievements:
            achievement = simulator.achievement_system.achievements[achievement_id]
            print(f"   {achievement['name']}: {achievement['description']}")
    else:
        print("暂无新成就，继续努力！")
    print()


async def demo_game_modes():
    """游戏模式对比演示"""
    print("🎮 游戏模式对比演示")
    print("=" * 50)
    
    modes = [
        (GameMode.EASY, "云养娃"),
        (GameMode.NORMAL, "实习父母"),
        (GameMode.HARD, "地狱特训")
    ]
    
    for mode, mode_name in modes:
        simulator = HardcoreParentingSimulator()
        config = simulator.mode_manager.get_mode_config(mode)
        
        print(f"{mode_name} ({mode.value}):")
        print(f"  事件频率倍数: {config['event_frequency']}")
        print(f"  夜间保护: {config.get('night_protection', False)}")
        print(f"  离线暂停: {config.get('offline_pause', False)}")
        print(f"  理智值衰减率: {config['sanity_decay_rate']}")
        
        if mode == GameMode.HARD:
            print(f"  强制通知: {config.get('force_notifications', False)}")
            print(f"  睡眠干扰: {config.get('sleep_disruption', False)}")
        print()


async def main():
    """主演示函数"""
    print("🍼 硬核父母岗前特训 - 系统演示")
    print("在只要孩子不哭，尊严算什么？")
    print("=" * 60)
    print()
    
    # 运行各种演示
    await demo_basic_gameplay()
    await asyncio.sleep(1)
    
    await demo_explosive_diaper()
    await asyncio.sleep(1)
    
    await demo_midnight_terror()
    await asyncio.sleep(1)
    
    await demo_achievement_system()
    await asyncio.sleep(1)
    
    await demo_game_modes()
    
    print("演示完成！准备好接受硬核父母的挑战了吗？ 💪")


if __name__ == "__main__":
    asyncio.run(main())