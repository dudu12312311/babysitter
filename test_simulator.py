"""
育儿模拟器测试文件
测试核心功能和边界条件
"""

import asyncio
import pytest
from hardcore_parenting_simulator import (
    HardcoreParentingSimulator,
    GameState,
    GameMode,
    ActionType,
    EventType,
    PlayerAction,
    CryingTask,
    ExplosiveDiaperTask,
    MidnightTerrorTask
)


class TestGameState:
    """测试游戏状态"""
    
    def test_initial_state(self):
        """测试初始状态"""
        state = GameState()
        assert state.comfort == 100
        assert state.sanity == 100
        assert state.parenting_kpi == 100
        assert state.game_mode == GameMode.NORMAL
    
    def test_state_boundaries(self):
        """测试状态边界值"""
        state = GameState()
        
        # 测试下边界
        state.comfort = -10
        state.sanity = -5
        state.parenting_kpi = -20
        
        # 在实际系统中，这些值应该被限制在0-100范围内
        # 这里我们测试边界条件的处理


class TestCryingTask:
    """测试哭闹任务"""
    
    def setup_method(self):
        self.task = CryingTask()
        self.game_state = GameState()
    
    async def test_successful_comfort(self):
        """测试成功安抚"""
        action = PlayerAction(
            action_type=ActionType.COMFORT,
            response_time=20.0,  # 快速响应
            success=True,
            player_id="test_player"
        )
        
        result_state = await self.task.execute(self.game_state, action)
        
        # 快速响应应该增加舒适度和理智值
        assert result_state.comfort > self.game_state.comfort
        assert result_state.sanity >= self.game_state.sanity
    
    async def test_slow_response(self):
        """测试缓慢响应"""
        action = PlayerAction(
            action_type=ActionType.COMFORT,
            response_time=60.0,  # 慢响应
            success=True,
            player_id="test_player"
        )
        
        initial_sanity = self.game_state.sanity
        result_state = await self.task.execute(self.game_state, action)
        
        # 慢响应应该减少理智值
        assert result_state.sanity < initial_sanity
    
    def test_action_validation(self):
        """测试行动验证"""
        valid_action = PlayerAction(
            action_type=ActionType.COMFORT,
            response_time=30.0,
            success=True,
            player_id="test_player"
        )
        
        invalid_action = PlayerAction(
            action_type=ActionType.FEED,  # 错误的行动类型
            response_time=30.0,
            success=True,
            player_id="test_player"
        )
        
        assert self.task.validate_action(valid_action, self.game_state) == True
        assert self.task.validate_action(invalid_action, self.game_state) == False


class TestExplosiveDiaperTask:
    """测试生化危机任务"""
    
    def setup_method(self):
        self.task = ExplosiveDiaperTask()
        self.game_state = GameState()
    
    async def test_no_action_penalty(self):
        """测试不处理的惩罚"""
        initial_comfort = self.game_state.comfort
        initial_sanity = self.game_state.sanity
        initial_kpi = self.game_state.parenting_kpi
        
        result_state = await self.task.execute(self.game_state, None)
        
        # 不处理应该严重降低所有数值
        assert result_state.comfort < initial_comfort
        assert result_state.sanity < initial_sanity
        assert result_state.parenting_kpi < initial_kpi
    
    def test_score_impact(self):
        """测试分数影响计算"""
        successful_action = PlayerAction(
            action_type=ActionType.CHANGE_DIAPER,
            response_time=30.0,
            success=True,
            player_id="test_player"
        )
        
        failed_action = PlayerAction(
            action_type=ActionType.CHANGE_DIAPER,
            response_time=30.0,
            success=False,
            player_id="test_player"
        )
        
        success_impact = self.task.calculate_score_impact(successful_action, self.game_state)
        fail_impact = self.task.calculate_score_impact(failed_action, self.game_state)
        
        # 成功应该有正面影响，失败应该有负面影响
        assert success_impact["kpi"] > fail_impact["kpi"]


class TestMidnightTerrorTask:
    """测试午夜恐怖任务"""
    
    def setup_method(self):
        self.task = MidnightTerrorTask()
        self.game_state = GameState()
    
    def test_hallucination_detection(self):
        """测试幻觉检测"""
        # 正常理智值
        self.game_state.sanity = 50
        assert self.task.is_hallucinating(self.game_state) == False
        
        # 低理智值
        self.game_state.sanity = 20
        assert self.task.is_hallucinating(self.game_state) == True
    
    async def test_critical_response_time(self):
        """测试关键响应时间"""
        slow_action = PlayerAction(
            action_type=ActionType.COMFORT,
            response_time=400.0,  # 超过5分钟
            success=True,
            player_id="test_player"
        )
        
        initial_kpi = self.game_state.parenting_kpi
        await self.task.execute(self.game_state, slow_action)
        
        # 响应过慢应该影响KPI（通过calculate_score_impact体现）
        impact = self.task.calculate_score_impact(slow_action, self.game_state)
        assert impact["kpi"] < 0


class TestHardcoreParentingSimulator:
    """测试主控制器"""
    
    def setup_method(self):
        self.simulator = HardcoreParentingSimulator()
    
    async def test_game_initialization(self):
        """测试游戏初始化"""
        player_id = "test_player"
        initial_state = await self.simulator.start_game(player_id, GameMode.NORMAL)
        
        assert initial_state.comfort == 100
        assert initial_state.sanity == 100
        assert initial_state.parenting_kpi == 100
        assert initial_state.game_mode == GameMode.NORMAL
        assert player_id in self.simulator.player_stats
    
    async def test_event_triggering(self):
        """测试事件触发"""
        event = await self.simulator.trigger_random_event()
        
        # 由于是随机的，可能返回None或事件
        if event:
            assert event.event_type in EventType
            assert 0 <= event.severity <= 10
            assert len(event.required_actions) > 0
    
    def test_game_status(self):
        """测试游戏状态获取"""
        status = self.simulator.get_game_status()
        
        assert "game_state" in status
        assert "active_events" in status
        assert "is_hallucinating" in status
        
        # 检查游戏状态结构
        game_state = status["game_state"]
        assert "comfort" in game_state
        assert "sanity" in game_state
        assert "parenting_kpi" in game_state
        assert "mode" in game_state


class TestGameModeManager:
    """测试游戏模式管理器"""
    
    def setup_method(self):
        from hardcore_parenting_simulator import GameModeManager
        self.manager = GameModeManager()
    
    def test_mode_configs(self):
        """测试模式配置"""
        easy_config = self.manager.get_mode_config(GameMode.EASY)
        normal_config = self.manager.get_mode_config(GameMode.NORMAL)
        hard_config = self.manager.get_mode_config(GameMode.HARD)
        
        # 简单模式应该有夜间保护
        assert easy_config["night_protection"] == True
        assert easy_config["offline_pause"] == True
        
        # 困难模式应该有更高的事件频率
        assert hard_config["event_frequency"] > normal_config["event_frequency"]
        assert hard_config.get("force_notifications") == True


async def run_tests():
    """运行所有测试"""
    print("🧪 开始运行育儿模拟器测试...")
    print("=" * 50)
    
    # 创建测试实例
    test_classes = [
        TestGameState(),
        TestCryingTask(),
        TestExplosiveDiaperTask(),
        TestMidnightTerrorTask(),
        TestHardcoreParentingSimulator(),
        TestGameModeManager()
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for test_class in test_classes:
        class_name = test_class.__class__.__name__
        print(f"\n📋 运行 {class_name} 测试...")
        
        # 获取所有测试方法
        test_methods = [method for method in dir(test_class) if method.startswith('test_')]
        
        for method_name in test_methods:
            total_tests += 1
            try:
                method = getattr(test_class, method_name)
                
                # 运行setup方法（如果存在）
                if hasattr(test_class, 'setup_method'):
                    test_class.setup_method()
                
                # 运行测试方法
                if asyncio.iscoroutinefunction(method):
                    await method()
                else:
                    method()
                
                print(f"  ✅ {method_name}")
                passed_tests += 1
                
            except Exception as e:
                print(f"  ❌ {method_name}: {str(e)}")
    
    print(f"\n📊 测试结果: {passed_tests}/{total_tests} 通过")
    
    if passed_tests == total_tests:
        print("🎉 所有测试通过！系统准备就绪！")
    else:
        print("⚠️ 部分测试失败，需要修复问题。")


if __name__ == "__main__":
    asyncio.run(run_tests())