"""
分龄育儿系统完整演示
Age-Based Parenting System Complete Demo

展示所有年龄阶段的任务执行、状态变化和惊喜时刻
"""

import asyncio
import random
from datetime import datetime, timedelta
from age_based_parenting_system import (
    AgeBasedParentingManager, AgeStage, TaskType, EmotionType,
    ChildState, ParentState
)


class AgeBasedSystemDemo:
    """分龄育儿系统演示类"""
    
    def __init__(self):
        self.manager = AgeBasedParentingManager()
        self.demo_scenarios = self._create_demo_scenarios()
    
    def _create_demo_scenarios(self):
        """创建演示场景"""
        return {
            AgeStage.NEWBORN: {
                "age_months": 2,
                "description": "2个月新生儿 - 生理需求阶段",
                "demo_tasks": [
                    ("NewbornFeedingTask", {
                        "feeding_type": "breast_milk",
                        "temperature": 36.8,
                        "response_time": 45
                    }),
                    ("NewbornSleepTask", {
                        "method": "swaddling",
                        "environment_score": 85,
                        "patience_level": 80
                    }),
                    ("CryingDecodeTask", {
                        "crying_duration": 180,
                        "parent_guess": "hunger",
                        "systematic_check": True
                    })
                ]
            },
            AgeStage.INFANT: {
                "age_months": 8,
                "description": "8个月婴儿 - 安全探索阶段",
                "demo_tasks": [
                    ("SafeExplorationTask", {
                        "exploration_type": "crawling",
                        "safety_measures": ["baby_gates", "outlet_covers", "corner_guards"],
                        "supervision_level": "close",
                        "encouragement_given": True
                    }),
                    ("SensoryStimuationTask", {
                        "stimulation_types": ["visual", "auditory", "tactile"],
                        "intensity_level": "moderate",
                        "duration_minutes": 15,
                        "interactive": True
                    })
                ]
            },
            AgeStage.TODDLER: {
                "age_months": 24,
                "description": "2岁幼儿 - 情绪行为阶段",
                "demo_tasks": [
                    ("EmotionRegulationTask", {
                        "intervention_type": "comfort",
                        "emotion_naming": True,
                        "breathing_exercise": False,
                        "distraction_method": "favorite_toy",
                        "validation_given": True,
                        "timeout_used": False
                    }),
                    ("PositiveBehaviorTask", {
                        "behavior_target": "sharing",
                        "reinforcement_type": "praise",
                        "consistency_level": "high",
                        "immediate_feedback": True,
                        "specific_praise": True
                    })
                ]
            },
            AgeStage.PRESCHOOL: {
                "age_months": 48,
                "description": "4岁学龄前 - 社交教育阶段",
                "demo_tasks": [
                    ("SocialSkillsTask", {
                        "social_situation": "playground",
                        "skill_focus": "sharing",
                        "adult_guidance": "moderate",
                        "peer_interaction": True,
                        "conflict_resolution": True
                    }),
                    ("EarlyEducationTask", {
                        "learning_activity": "reading",
                        "child_interest_level": "high",
                        "interactive_approach": True,
                        "play_based_learning": True,
                        "difficulty_appropriate": True
                    })
                ]
            }
        }
    
    async def run_complete_demo(self):
        """运行完整演示"""
        print("🎯 分龄育儿系统完整演示")
        print("=" * 60)
        print("展示从新生儿到学龄前儿童的完整育儿旅程")
        print()
        
        for stage in [AgeStage.NEWBORN, AgeStage.INFANT, AgeStage.TODDLER, AgeStage.PRESCHOOL]:
            await self._demo_age_stage(stage)
            print("\n" + "="*60 + "\n")
    
    async def _demo_age_stage(self, stage: AgeStage):
        """演示特定年龄阶段"""
        scenario = self.demo_scenarios[stage]
        
        print(f"📅 {scenario['description']}")
        print("-" * 40)
        
        # 重置并设置年龄
        self.manager = AgeBasedParentingManager()
        self.manager.child_state.age_months = scenario["age_months"]
        self.manager.current_age_stage = self.manager._determine_age_stage()
        self.manager.available_tasks = self.manager._initialize_tasks()
        
        # 设置适合演示的初始状态
        self._setup_demo_state(stage)
        
        # 显示初始状态
        print("📊 初始状态:")
        self._display_current_status()
        
        # 评估需求
        print("\n🔍 需求评估:")
        needs = await self.manager.assess_all_needs()
        for task_name, task_info in needs.items():
            if "SurpriseMomentTask" not in task_name:  # 先不显示惊喜时刻
                urgency_level = "🔴高" if task_info["urgency"] > 70 else "🟡中" if task_info["urgency"] > 40 else "🟢低"
                print(f"  {urgency_level} {task_name}: {task_info['urgency']}/100")
                print(f"     📝 {task_info['description']}")
        
        # 执行演示任务
        print(f"\n🎮 执行{stage.value}阶段特色任务:")
        for task_name, action_data in scenario["demo_tasks"]:
            await self._execute_demo_task(task_name, action_data)
        
        # 尝试触发惊喜时刻
        print("\n✨ 尝试触发惊喜时刻:")
        surprise_result = await self.manager.trigger_surprise_moment()
        if surprise_result and surprise_result["success"]:
            print(f"🎉 {surprise_result['message']}")
            print(f"   分数变化: +{surprise_result['score_change']}")
            surprise_data = surprise_result.get("task_specific_data", {})
            if "milestone_significance" in surprise_data:
                print(f"   💡 意义: {surprise_data['milestone_significance']}")
        else:
            print("   😊 这次没有惊喜时刻，但随时可能出现！")
        
        # 显示最终状态
        print("\n📈 阶段结束状态:")
        self._display_current_status()
        
        # 显示发展建议
        self._display_development_recommendations(stage)
    
    def _setup_demo_state(self, stage: AgeStage):
        """设置演示状态"""
        if stage == AgeStage.NEWBORN:
            # 新生儿：模拟一些生理需求
            self.manager.child_state.hunger_level = 65
            self.manager.child_state.sleep_debt = 40
            self.manager.child_state.diaper_wetness = 30
            self.manager.parent_state.stress_level = 45
            
        elif stage == AgeStage.INFANT:
            # 婴儿：模拟探索期状态
            self.manager.child_state.curiosity = 80
            self.manager.child_state.motor_skills = 35
            self.manager.child_state.energy_level = 85
            self.manager.parent_state.confidence = 60
            
        elif stage == AgeStage.TODDLER:
            # 幼儿：模拟情绪挑战
            self.manager.child_state.current_emotion = EmotionType.FRUSTRATED
            self.manager.child_state.emotional_regulation = 30
            self.manager.child_state.social_confidence = 45
            self.manager.parent_state.patience = 55
            
        elif stage == AgeStage.PRESCHOOL:
            # 学龄前：模拟学习和社交需求
            self.manager.child_state.learning_motivation = 75
            self.manager.child_state.social_confidence = 60
            self.manager.child_state.language_skills = 65
            self.manager.parent_state.parenting_skills = 70
    
    async def _execute_demo_task(self, task_name: str, action_data: dict):
        """执行演示任务"""
        print(f"\n  🎯 执行任务: {task_name}")
        
        # 显示任务参数
        print(f"     参数: {action_data}")
        
        # 执行任务
        result = await self.manager.execute_task(task_name, action_data)
        
        # 显示结果
        success_icon = "✅" if result["success"] else "❌"
        print(f"     {success_icon} {result['message']}")
        print(f"     分数变化: {result['score_change']:+d} (总分: {result['total_score']})")
        
        # 显示状态变化
        if result["success"]:
            before = result["before_states"]
            after = result["after_states"]
            
            # 显示重要的状态变化
            child_changes = []
            for key in ["happiness", "comfort_level", "emotional_regulation"]:
                if key in before["child"] and key in after["child"]:
                    change = after["child"][key] - before["child"][key]
                    if abs(change) >= 5:
                        child_changes.append(f"{key}: {change:+d}")
            
            parent_changes = []
            for key in ["confidence", "stress_level", "parenting_skills"]:
                if key in before["parent"] and key in after["parent"]:
                    change = after["parent"][key] - before["parent"][key]
                    if abs(change) >= 5:
                        parent_changes.append(f"{key}: {change:+d}")
            
            if child_changes:
                print(f"     👶 孩子状态变化: {', '.join(child_changes)}")
            if parent_changes:
                print(f"     👨‍👩‍👧‍👦 父母状态变化: {', '.join(parent_changes)}")
        
        # 显示任务特定信息
        task_data = result.get("task_specific_data", {})
        if "tips" in task_data:
            print(f"     💡 提示: {', '.join(task_data['tips'][:2])}")
        elif "learning_points" in task_data:
            print(f"     📚 学习要点: {', '.join(task_data['learning_points'][:2])}")
    
    def _display_current_status(self):
        """显示当前状态"""
        status = self.manager.get_comprehensive_status()
        child = status["child_state"]
        parent = status["parent_state"]
        progress = status["development_progress"]
        
        print(f"  👶 孩子状态: 快乐度{child['happiness']}/100, 舒适度{child['comfort_level']}/100, 情绪:{child['current_emotion']}")
        print(f"  👨‍👩‍👧‍👦 父母状态: 自信{parent['confidence']}/100, 压力{parent['stress_level']}/100, 总分{parent['total_parenting_score']}/1000")
        print(f"  📈 发展进度: {progress['overall_progress']:.1f}/100 ({'准备升级' if progress['ready_for_next_stage'] else '继续发展'})")
    
    def _display_development_recommendations(self, stage: AgeStage):
        """显示发展建议"""
        recommendations = {
            AgeStage.NEWBORN: [
                "建立规律的喂食和睡眠时间",
                "学会识别不同类型的哭声",
                "保持耐心，新生儿期是适应期",
                "记录宝宝的作息模式"
            ],
            AgeStage.INFANT: [
                "创造安全的探索环境",
                "提供多样化的感官刺激",
                "鼓励运动技能发展",
                "开始简单的互动游戏"
            ],
            AgeStage.TODDLER: [
                "重视情绪教育和命名",
                "使用正向强化方法",
                "保持一致的规则和界限",
                "培养自我调节能力"
            ],
            AgeStage.PRESCHOOL: [
                "提供社交互动机会",
                "采用游戏化学习方式",
                "培养独立解决问题能力",
                "准备入学前的各项技能"
            ]
        }
        
        print(f"\n💡 {stage.value}阶段发展建议:")
        for i, rec in enumerate(recommendations[stage], 1):
            print(f"  {i}. {rec}")
    
    async def demo_time_progression(self):
        """演示时间推进功能"""
        print("\n⏰ 时间推进演示")
        print("-" * 30)
        
        # 设置为新生儿阶段
        self.manager.child_state.age_months = 1
        self.manager.current_age_stage = AgeStage.NEWBORN
        self.manager.available_tasks = self.manager._initialize_tasks()
        
        print("模拟6小时时间流逝...")
        
        # 显示初始状态
        print("初始状态:")
        self._display_physiological_needs()
        
        # 模拟时间流逝
        surprise = await self.manager.simulate_time_passage(6.0)
        
        print("\n6小时后状态:")
        self._display_physiological_needs()
        
        if surprise and surprise["success"]:
            print(f"\n🎉 时间流逝中出现惊喜时刻: {surprise['message']}")
    
    def _display_physiological_needs(self):
        """显示生理需求状态"""
        child = self.manager.child_state
        print(f"  饥饿程度: {child.hunger_level}/100")
        print(f"  睡眠债务: {child.sleep_debt}/100")
        print(f"  尿布湿润: {child.diaper_wetness}/100")
        print(f"  精力水平: {child.energy_level}/100")
    
    async def demo_crisis_management(self):
        """演示危机管理场景"""
        print("\n🚨 危机管理演示")
        print("-" * 30)
        
        # 设置危机场景：2岁孩子情绪崩溃
        self.manager.child_state.age_months = 24
        self.manager.current_age_stage = AgeStage.TODDLER
        self.manager.available_tasks = self.manager._initialize_tasks()
        
        # 模拟危机状态
        self.manager.child_state.current_emotion = EmotionType.ANGRY
        self.manager.child_state.happiness = 20
        self.manager.child_state.comfort_level = 30
        self.manager.child_state.emotional_regulation = 15
        self.manager.parent_state.stress_level = 80
        self.manager.parent_state.patience = 25
        
        print("🔥 危机场景: 2岁孩子在超市情绪崩溃")
        print("初始状态:")
        self._display_current_status()
        
        # 演示不同的应对策略
        strategies = [
            ("错误应对", {
                "intervention_type": "ignore",
                "emotion_naming": False,
                "validation_given": False,
                "timeout_used": True  # 不适合的年龄使用暂停
            }),
            ("正确应对", {
                "intervention_type": "comfort",
                "emotion_naming": True,
                "validation_given": True,
                "distraction_method": "favorite_song",
                "timeout_used": False
            })
        ]
        
        for strategy_name, action_data in strategies:
            print(f"\n📋 尝试{strategy_name}:")
            
            # 重置状态以便比较
            if strategy_name == "正确应对":
                self.manager.child_state.current_emotion = EmotionType.ANGRY
                self.manager.child_state.happiness = 20
                self.manager.parent_state.stress_level = 80
            
            result = await self.manager.execute_task("EmotionRegulationTask", action_data)
            success_icon = "✅" if result["success"] else "❌"
            print(f"  {success_icon} {result['message']}")
            print(f"  分数变化: {result['score_change']:+d}")
            
            if result["success"]:
                print("  🎯 危机成功化解！")
            else:
                print("  ⚠️ 需要尝试其他方法")


async def main():
    """主演示函数"""
    demo = AgeBasedSystemDemo()
    
    print("🎮 分龄育儿系统演示菜单")
    print("1. 完整年龄阶段演示")
    print("2. 时间推进演示")
    print("3. 危机管理演示")
    print("4. 全部演示")
    
    choice = input("\n请选择演示类型 (1-4): ").strip()
    
    if choice == "1":
        await demo.run_complete_demo()
    elif choice == "2":
        await demo.demo_time_progression()
    elif choice == "3":
        await demo.demo_crisis_management()
    elif choice == "4":
        await demo.run_complete_demo()
        await demo.demo_time_progression()
        await demo.demo_crisis_management()
    else:
        print("无效选择，运行完整演示...")
        await demo.run_complete_demo()
    
    print("\n🎉 演示完成！")
    print("这个分龄育儿系统展示了:")
    print("✅ 4个年龄阶段的不同任务类型")
    print("✅ 基于状态的智能需求评估")
    print("✅ 详细的状态变化追踪")
    print("✅ 惊喜时刻彩蛋系统")
    print("✅ 时间推进和自然状态变化")
    print("✅ 危机管理和应对策略")


if __name__ == "__main__":
    asyncio.run(main())