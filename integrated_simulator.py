"""
集成育儿模拟器：硬核父母岗前特训 + 分龄育儿系统
Integrated Parenting Simulator: Hardcore Training + Age-Based System

将原有的特色任务模式与分龄育儿系统完美结合
"""

import asyncio
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

# 导入原有系统
from hardcore_parenting_simulator import (
    HardcoreParentingSimulator, GameMode, BabyState, 
    ParentState as OriginalParentState, GameEvent, EventType
)

# 导入分龄系统
from age_based_parenting_system import (
    AgeBasedParentingManager, AgeStage, TaskType, EmotionType,
    ChildState, ParentState as AgeBasedParentState
)


class IntegratedGameMode(Enum):
    """集成游戏模式"""
    CLASSIC_HARDCORE = "classic_hardcore"      # 原版硬核模式
    AGE_BASED_TRAINING = "age_based_training"  # 分龄训练模式
    HYBRID_CHALLENGE = "hybrid_challenge"      # 混合挑战模式


class IntegratedParentingSimulator:
    """集成育儿模拟器"""
    
    def __init__(self):
        # 初始化两个系统
        self.hardcore_simulator = HardcoreParentingSimulator()
        self.age_based_manager = AgeBasedParentingManager()
        
        # 集成状态
        self.current_mode = IntegratedGameMode.HYBRID_CHALLENGE
        self.integration_score = 1000  # 集成总分
        self.special_achievements = []
        
        # 同步初始状态
        self._sync_states()
    
    def _sync_states(self):
        """同步两个系统的状态"""
        # 将分龄系统的状态映射到硬核系统
        age_child = self.age_based_manager.child_state
        age_parent = self.age_based_manager.parent_state
        
        # 同步宝宝状态
        self.hardcore_simulator.baby_state.comfort = age_child.comfort_level
        self.hardcore_simulator.baby_state.hunger = age_child.hunger_level
        self.hardcore_simulator.baby_state.sleep_debt = age_child.sleep_debt
        
        # 同步父母状态
        self.hardcore_simulator.parent_state.sanity = age_parent.sanity_level
        self.hardcore_simulator.parent_state.stress = age_parent.stress_level
        self.hardcore_simulator.parent_state.confidence = age_parent.confidence
    
    async def start_integrated_session(self, mode: IntegratedGameMode, 
                                     age_months: int = 2) -> Dict[str, Any]:
        """开始集成游戏会话"""
        self.current_mode = mode
        
        # 设置年龄
        self.age_based_manager.child_state.age_months = age_months
        self.age_based_manager.current_age_stage = self.age_based_manager._determine_age_stage()
        self.age_based_manager.available_tasks = self.age_based_manager._initialize_tasks()
        
        # 根据模式初始化
        if mode == IntegratedGameMode.CLASSIC_HARDCORE:
            return await self._start_classic_mode()
        elif mode == IntegratedGameMode.AGE_BASED_TRAINING:
            return await self._start_age_based_mode()
        else:  # HYBRID_CHALLENGE
            return await self._start_hybrid_mode()
    
    async def _start_classic_mode(self) -> Dict[str, Any]:
        """启动经典硬核模式"""
        print("🔥 启动经典硬核模式")
        print("特色任务: 生化危机、午夜凶铃、后备箱俄罗斯方块、挑食谈判专家")
        
        # 使用原有的硬核系统
        session_result = await self.hardcore_simulator.start_game_session(
            mode=GameMode.HELL_WEEK,
            duration_hours=168  # 7天挑战
        )
        
        return {
            "mode": "classic_hardcore",
            "session_id": session_result["session_id"],
            "special_tasks_available": [
                "explosive_diaper", "midnight_terror", 
                "stroller_tetris", "picky_eater_negotiation"
            ],
            "challenge_level": "极限挑战",
            "duration": "7天实时挑战"
        }
    
    async def _start_age_based_mode(self) -> Dict[str, Any]:
        """启动分龄训练模式"""
        current_stage = self.age_based_manager.current_age_stage
        print(f"👶 启动分龄训练模式 - {current_stage.value}")
        
        # 评估当前阶段需求
        needs = await self.age_based_manager.assess_all_needs()
        priority_tasks = await self.age_based_manager.get_priority_tasks(threshold=40)
        
        return {
            "mode": "age_based_training",
            "current_stage": current_stage.value,
            "age_months": self.age_based_manager.child_state.age_months,
            "priority_tasks": [(task.__class__.__name__, urgency) for task, urgency in priority_tasks],
            "development_focus": self._get_stage_focus(current_stage),
            "available_surprises": True
        }
    
    async def _start_hybrid_mode(self) -> Dict[str, Any]:
        """启动混合挑战模式"""
        current_stage = self.age_based_manager.current_age_stage
        print(f"⚡ 启动混合挑战模式 - {current_stage.value} + 特色任务")
        
        # 结合两个系统的优势
        age_tasks = await self.age_based_manager.get_priority_tasks(threshold=30)
        
        return {
            "mode": "hybrid_challenge",
            "current_stage": current_stage.value,
            "age_months": self.age_based_manager.child_state.age_months,
            "age_based_tasks": [(task.__class__.__name__, urgency) for task, urgency in age_tasks],
            "special_tasks_available": self._get_age_appropriate_special_tasks(current_stage),
            "integration_features": [
                "分龄任务与特色模式结合",
                "动态难度调整",
                "发展里程碑奖励",
                "惊喜时刻彩蛋"
            ]
        }
    
    def _get_stage_focus(self, stage: AgeStage) -> List[str]:
        """获取阶段重点"""
        focus_map = {
            AgeStage.NEWBORN: ["生理需求满足", "哭闹解码", "睡眠建立", "喂食技巧"],
            AgeStage.INFANT: ["安全探索", "感官刺激", "运动发展", "认知启蒙"],
            AgeStage.TODDLER: ["情绪调节", "行为引导", "语言发展", "社交启蒙"],
            AgeStage.PRESCHOOL: ["社交技能", "学习能力", "独立性", "创造力"]
        }
        return focus_map.get(stage, ["全面发展"])
    
    def _get_age_appropriate_special_tasks(self, stage: AgeStage) -> List[str]:
        """获取适龄特色任务"""
        if stage == AgeStage.NEWBORN:
            return ["explosive_diaper", "midnight_terror"]
        elif stage == AgeStage.INFANT:
            return ["explosive_diaper", "stroller_tetris"]
        elif stage == AgeStage.TODDLER:
            return ["picky_eater_negotiation", "stroller_tetris"]
        else:  # PRESCHOOL
            return ["picky_eater_negotiation", "social_challenge"]
    
    async def execute_integrated_task(self, task_type: str, 
                                    action_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行集成任务"""
        if task_type in ["explosive_diaper", "midnight_terror", "stroller_tetris", "picky_eater_negotiation"]:
            # 执行特色任务
            return await self._execute_special_task(task_type, action_data)
        else:
            # 执行分龄任务
            return await self._execute_age_based_task(task_type, action_data)
    
    async def _execute_special_task(self, task_type: str, 
                                  action_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行特色任务"""
        print(f"🎮 执行特色任务: {task_type}")
        
        # 根据任务类型调用相应的特色模式
        if task_type == "explosive_diaper":
            result = await self.hardcore_simulator.handle_explosive_diaper(action_data)
        elif task_type == "midnight_terror":
            result = await self.hardcore_simulator.handle_midnight_terror(action_data)
        elif task_type == "stroller_tetris":
            result = await self.hardcore_simulator.handle_stroller_tetris(action_data)
        elif task_type == "picky_eater_negotiation":
            result = await self.hardcore_simulator.handle_picky_eater_negotiation(action_data)
        else:
            return {"success": False, "message": "未知特色任务"}
        
        # 将结果同步到分龄系统
        if result["success"]:
            await self._sync_special_task_effects(task_type, result)
        
        return result
    
    async def _execute_age_based_task(self, task_type: str, 
                                    action_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行分龄任务"""
        print(f"👶 执行分龄任务: {task_type}")
        
        result = await self.age_based_manager.execute_task(task_type, action_data)
        
        # 将结果同步到硬核系统
        if result["success"]:
            await self._sync_age_based_effects(result)
        
        return result
    
    async def _sync_special_task_effects(self, task_type: str, result: Dict[str, Any]):
        """同步特色任务效果到分龄系统"""
        score_change = result.get("score_change", 0)
        
        # 根据任务类型给予不同的发展奖励
        if task_type == "explosive_diaper":
            # 换尿布任务提升父母技能和孩子舒适度
            self.age_based_manager.parent_state.parenting_skills = min(100, 
                self.age_based_manager.parent_state.parenting_skills + 5)
            self.age_based_manager.child_state.comfort_level = min(100,
                self.age_based_manager.child_state.comfort_level + 10)
        
        elif task_type == "midnight_terror":
            # 夜间任务影响睡眠和理智
            self.age_based_manager.parent_state.sanity_level = max(0,
                self.age_based_manager.parent_state.sanity_level - 10)
            self.age_based_manager.child_state.sleep_debt = max(0,
                self.age_based_manager.child_state.sleep_debt - 20)
        
        elif task_type == "picky_eater_negotiation":
            # 喂食谈判提升沟通技能
            if self.age_based_manager.current_age_stage in [AgeStage.TODDLER, AgeStage.PRESCHOOL]:
                self.age_based_manager.child_state.language_skills = min(100,
                    self.age_based_manager.child_state.language_skills + 8)
                self.age_based_manager.parent_state.emotional_intelligence = min(100,
                    self.age_based_manager.parent_state.emotional_intelligence + 6)
        
        # 更新集成分数
        self.integration_score = max(0, min(2000, self.integration_score + score_change))
    
    async def _sync_age_based_effects(self, result: Dict[str, Any]):
        """同步分龄任务效果到硬核系统"""
        # 更新硬核系统的状态
        self._sync_states()
        
        # 更新集成分数
        score_change = result.get("score_change", 0)
        self.integration_score = max(0, min(2000, self.integration_score + score_change))
    
    async def trigger_integrated_surprise(self) -> Optional[Dict[str, Any]]:
        """触发集成惊喜时刻"""
        # 首先尝试分龄系统的惊喜时刻
        age_surprise = await self.age_based_manager.trigger_surprise_moment()
        
        if age_surprise and age_surprise["success"]:
            # 分龄惊喜成功，给予额外奖励
            bonus_score = 20
            self.integration_score += bonus_score
            
            age_surprise["integration_bonus"] = bonus_score
            age_surprise["total_integration_score"] = self.integration_score
            
            return age_surprise
        
        # 如果没有分龄惊喜，尝试特色惊喜
        return await self._trigger_special_surprise()
    
    async def _trigger_special_surprise(self) -> Optional[Dict[str, Any]]:
        """触发特色惊喜时刻"""
        special_surprises = [
            "完美配合：双人任务零失误",
            "时间管理大师：同时处理3个任务",
            "危机化解：成功处理紧急情况",
            "育儿直觉：不看提示完成复杂任务"
        ]
        
        # 基于当前状态计算触发概率
        trigger_probability = 0.1  # 基础10%
        
        if self.age_based_manager.parent_state.confidence > 80:
            trigger_probability += 0.05
        if self.age_based_manager.parent_state.stress_level < 30:
            trigger_probability += 0.05
        
        if random.random() < trigger_probability:
            surprise = random.choice(special_surprises)
            bonus_score = 30
            self.integration_score += bonus_score
            
            return {
                "success": True,
                "message": f"🌟 特色惊喜时刻：{surprise}",
                "score_change": bonus_score,
                "total_integration_score": self.integration_score,
                "surprise_type": "special_achievement"
            }
        
        return None
    
    def get_integrated_status(self) -> Dict[str, Any]:
        """获取集成状态"""
        age_status = self.age_based_manager.get_comprehensive_status()
        hardcore_status = self.hardcore_simulator.get_game_state()
        
        return {
            "integration_score": self.integration_score,
            "current_mode": self.current_mode.value,
            "age_based_status": age_status,
            "hardcore_status": {
                "baby_comfort": hardcore_status["baby_state"]["comfort"],
                "parent_sanity": hardcore_status["parent_state"]["sanity"],
                "active_events": len(hardcore_status.get("active_events", [])),
                "achievements": hardcore_status.get("achievements", [])
            },
            "special_achievements": self.special_achievements,
            "sync_status": "已同步"
        }
    
    async def run_integrated_demo(self):
        """运行集成演示"""
        print("🎯 集成育儿模拟器演示")
        print("=" * 50)
        
        # 演示不同模式
        modes = [
            (IntegratedGameMode.AGE_BASED_TRAINING, 2),
            (IntegratedGameMode.HYBRID_CHALLENGE, 8),
            (IntegratedGameMode.HYBRID_CHALLENGE, 24)
        ]
        
        for mode, age_months in modes:
            print(f"\n=== {mode.value} 模式演示 (年龄: {age_months}个月) ===")
            
            # 启动会话
            session = await self.start_integrated_session(mode, age_months)
            print(f"会话启动: {session}")
            
            # 显示当前状态
            status = self.get_integrated_status()
            print(f"集成分数: {status['integration_score']}/2000")
            print(f"当前阶段: {status['age_based_status']['child_state']['age_stage']}")
            
            # 执行一些任务
            if mode == IntegratedGameMode.AGE_BASED_TRAINING:
                # 执行分龄任务
                if age_months <= 3:
                    result = await self.execute_integrated_task("NewbornFeedingTask", {
                        "feeding_type": "breast_milk",
                        "temperature": 36.8,
                        "response_time": 30
                    })
                    print(f"喂食任务结果: {result['message']}")
            
            elif mode == IntegratedGameMode.HYBRID_CHALLENGE:
                # 执行混合任务
                if age_months <= 12:
                    # 执行特色任务
                    result = await self.execute_integrated_task("explosive_diaper", {
                        "player_a_actions": ["hold_legs", "clean_area"],
                        "player_b_actions": ["provide_wipes", "dispose_diaper"],
                        "coordination_score": 85
                    })
                    print(f"生化危机任务结果: {result.get('message', '任务完成')}")
                
                # 执行分龄任务
                age_task = "SafeExplorationTask" if age_months >= 4 else "NewbornSleepTask"
                result = await self.execute_integrated_task(age_task, {
                    "method": "swaddling" if age_months < 4 else "crawling",
                    "safety_measures": ["baby_gates"] if age_months >= 4 else [],
                    "environment_score": 80
                })
                print(f"分龄任务结果: {result['message']}")
            
            # 尝试触发惊喜
            surprise = await self.trigger_integrated_surprise()
            if surprise:
                print(f"惊喜时刻: {surprise['message']}")
            
            print(f"最终集成分数: {self.get_integrated_status()['integration_score']}/2000")
            print("-" * 50)


async def main():
    """主函数"""
    simulator = IntegratedParentingSimulator()
    await simulator.run_integrated_demo()
    
    print("\n🎉 集成演示完成！")
    print("集成系统特色:")
    print("✅ 结合硬核特色任务与分龄科学育儿")
    print("✅ 动态状态同步和效果传递")
    print("✅ 多模式游戏体验")
    print("✅ 集成评分和成就系统")
    print("✅ 双重惊喜时刻机制")


if __name__ == "__main__":
    asyncio.run(main())