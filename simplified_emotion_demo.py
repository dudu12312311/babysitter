#!/usr/bin/env python3
"""
简化情绪系统演示
Simplified Emotion System Demo

展示简化后的情绪类型和状态系统，让demo更简洁有趣
"""

import asyncio
import random
from age_based_parenting_system import (
    AgeBasedParentingManager, 
    EmotionType, 
    AgeStage
)


async def demo_simplified_emotions():
    """演示简化的情绪系统"""
    print("🎭 简化情绪系统演示")
    print("=" * 50)
    
    manager = AgeBasedParentingManager()
    
    # 设置为2岁幼儿（情绪管理关键期）
    manager.child_state.age_months = 24
    manager.current_age_stage = AgeStage.TODDLER
    manager.available_tasks = manager._initialize_tasks()
    
    print(f"👶 当前年龄: {manager.child_state.age_months}个月 ({manager.current_age_stage.value})")
    print(f"😊 当前情绪: {manager.child_state.current_emotion.value}")
    print()
    
    # 演示不同情绪状态下的任务执行
    emotion_scenarios = [
        (EmotionType.HAPPY, "宝宝很开心，适合学习新技能"),
        (EmotionType.UPSET, "宝宝不开心，需要情绪调节"),
        (EmotionType.WORRIED, "宝宝有些担心，需要安抚和支持")
    ]
    
    for emotion, description in emotion_scenarios:
        print(f"=== 情绪场景: {emotion.value} ===")
        print(f"📝 场景描述: {description}")
        
        # 设置情绪状态
        manager.child_state.current_emotion = emotion
        
        # 根据情绪调整其他状态
        if emotion == EmotionType.HAPPY:
            manager.child_state.happiness = 90
            manager.child_state.energy_level = 85
        elif emotion == EmotionType.UPSET:
            manager.child_state.happiness = 30
            manager.child_state.emotional_regulation = 20
        elif emotion == EmotionType.WORRIED:
            manager.child_state.happiness = 50
            manager.child_state.comfort_level = 40
        
        # 评估任务需求
        needs = await manager.assess_all_needs()
        priority_tasks = await manager.get_priority_tasks(threshold=40)
        
        print(f"🎯 优先任务数量: {len(priority_tasks)}")
        
        if priority_tasks:
            # 执行最紧急的任务
            top_task, urgency = priority_tasks[0]
            task_name = top_task.__class__.__name__
            
            print(f"🚀 执行任务: {task_name}")
            print(f"⚡ 紧急程度: {urgency}/100")
            
            # 模拟任务执行
            if task_name == "EmotionRegulationTask":
                action_data = {
                    "intervention_type": "comfort",
                    "emotion_naming": True,
                    "validation_given": True,
                    "breathing_exercise": emotion != EmotionType.WORRIED  # 担心时不适合呼吸练习
                }
            elif task_name == "PositiveBehaviorTask":
                action_data = {
                    "behavior_target": "sharing",
                    "reinforcement_type": "praise",
                    "consistency_level": "high",
                    "immediate_feedback": True,
                    "specific_praise": True
                }
            else:
                action_data = {"method": "gentle_approach"}
            
            result = await manager.execute_task(task_name, action_data)
            
            print(f"✅ 执行结果: {result['message']}")
            print(f"📊 分数变化: {result['score_change']:+d}")
            print(f"🏆 总分: {result['total_score']}")
            
            # 显示状态变化
            before = result['before_states']['child']
            after = result['after_states']['child']
            
            print("📈 状态变化:")
            for key in before:
                if before[key] != after[key]:
                    change = after[key] - before[key]
                    print(f"  {key}: {before[key]} → {after[key]} ({change:+d})")
            
            print(f"😊 情绪变化: {manager.child_state.current_emotion.value}")
        
        print()
        await asyncio.sleep(0.5)  # 短暂停顿，便于观察


async def demo_emotion_transitions():
    """演示情绪转换"""
    print("🔄 情绪转换演示")
    print("=" * 30)
    
    manager = AgeBasedParentingManager()
    manager.child_state.age_months = 30  # 2.5岁
    manager.current_age_stage = AgeStage.TODDLER
    manager.available_tasks = manager._initialize_tasks()
    
    # 模拟一天中的情绪变化
    daily_scenarios = [
        ("早晨醒来", EmotionType.HAPPY, "精神饱满的开始"),
        ("饿了想吃饭", EmotionType.UPSET, "肚子饿了有点烦躁"),
        ("吃饱了", EmotionType.HAPPY, "满足的感觉"),
        ("看到陌生人", EmotionType.WORRIED, "有点紧张和担心"),
        ("妈妈安慰后", EmotionType.HAPPY, "重新感到安全"),
        ("玩具被抢", EmotionType.UPSET, "生气和沮丧"),
        ("学会新技能", EmotionType.HAPPY, "成就感满满")
    ]
    
    for time_desc, emotion, situation in daily_scenarios:
        print(f"⏰ {time_desc}")
        print(f"😊 情绪: {emotion.value}")
        print(f"📝 情况: {situation}")
        
        manager.child_state.current_emotion = emotion
        
        # 根据情绪调整状态
        if emotion == EmotionType.HAPPY:
            manager.child_state.happiness = min(100, manager.child_state.happiness + 10)
            manager.child_state.energy_level = min(100, manager.child_state.energy_level + 5)
        elif emotion == EmotionType.UPSET:
            manager.child_state.happiness = max(0, manager.child_state.happiness - 15)
            manager.parent_state.stress_level = min(100, manager.parent_state.stress_level + 10)
        elif emotion == EmotionType.WORRIED:
            manager.child_state.comfort_level = max(0, manager.child_state.comfort_level - 10)
        
        # 显示当前状态
        print(f"📊 快乐度: {manager.child_state.happiness}/100")
        print(f"⚡ 精力: {manager.child_state.energy_level}/100")
        print(f"🛡️ 舒适度: {manager.child_state.comfort_level}/100")
        print(f"😰 父母压力: {manager.parent_state.stress_level}/100")
        print()
        
        await asyncio.sleep(0.3)


async def demo_simplified_system():
    """演示简化后的整体系统"""
    print("🎮 简化育儿系统完整演示")
    print("=" * 40)
    
    manager = AgeBasedParentingManager()
    
    # 快速体验不同年龄阶段
    age_demos = [
        (2, "新生儿", "主要关注生理需求"),
        (8, "婴儿", "探索和感官发展"),
        (24, "幼儿", "情绪和行为管理"),
        (48, "学龄前", "社交和学习能力")
    ]
    
    for age_months, stage_name, focus in age_demos:
        print(f"=== {stage_name}阶段 ({age_months}个月) ===")
        print(f"🎯 重点: {focus}")
        
        manager.child_state.age_months = age_months
        manager.current_age_stage = manager._determine_age_stage()
        manager.available_tasks = manager._initialize_tasks()
        
        # 获取状态概览
        status = manager.get_comprehensive_status()
        child_state = status['child_state']
        parent_state = status['parent_state']
        progress = status['development_progress']
        
        print(f"😊 当前情绪: {child_state['current_emotion']}")
        print(f"📈 发展进度: {progress['overall_progress']:.1f}/100")
        print(f"🏆 父母总分: {parent_state['total_parenting_score']}")
        print(f"💪 父母自信: {parent_state['confidence']}/100")
        
        # 显示关键发展领域
        print("🎯 关键发展领域:")
        for area, score in progress['key_areas'].items():
            emoji = "✅" if score >= 70 else "🔄" if score >= 40 else "⚠️"
            print(f"  {emoji} {area}: {score:.0f}/100")
        
        print()
        await asyncio.sleep(0.5)


async def main():
    """主演示函数"""
    print("🌟 欢迎体验简化版育儿系统！")
    print("本次更新简化了情绪类型，让游戏更容易上手")
    print()
    
    demos = [
        ("情绪系统演示", demo_simplified_emotions),
        ("情绪转换演示", demo_emotion_transitions),
        ("系统概览演示", demo_simplified_system)
    ]
    
    for demo_name, demo_func in demos:
        print(f"🎬 开始 {demo_name}")
        print("=" * 60)
        await demo_func()
        print("=" * 60)
        print()
        await asyncio.sleep(1)
    
    print("🎉 演示完成！")
    print("💡 简化要点:")
    print("  • 情绪类型从8种简化为3种：开心、不开心、担心")
    print("  • 状态属性精简，保留核心发展指标")
    print("  • 任务逻辑更清晰，专注于有趣的游戏体验")
    print("  • 保持了分龄特色和教育价值")


if __name__ == "__main__":
    asyncio.run(main())