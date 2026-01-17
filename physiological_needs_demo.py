"""
生理需求任务接口使用示例
展示如何使用生理需求系统进行婴儿护理
"""

import asyncio
from physiological_needs_tasks import (
    PhysiologicalNeedsManager, PhysiologicalNeedType, 
    FeedingType, DiaperType, SleepState
)


async def basic_care_scenario():
    """基础护理场景演示"""
    print("👶 基础护理场景演示")
    print("=" * 40)
    
    manager = PhysiologicalNeedsManager()
    
    # 场景1: 新生儿刚醒来
    print("场景: 新生儿刚从睡眠中醒来")
    
    # 模拟一些时间流逝
    await manager.simulate_time_passage(3.0)  # 3小时
    
    # 评估需求
    needs = await manager.assess_all_needs()
    print("需求评估:")
    for need_type, urgency in needs.items():
        if urgency > 20:
            print(f"  ⚠️ {need_type.value}: {urgency}/100")
    print()
    
    # 执行护理序列
    care_sequence = [
        (PhysiologicalNeedType.DIAPER_CHANGE, {
            "diaper_type": DiaperType.WET.value,
            "preparation_time": 30,
            "execution_time": 120,
            "cleanliness_score": 85,
            "technique_score": 75
        }),
        (PhysiologicalNeedType.HUNGER, {
            "feeding_type": FeedingType.BREAST_MILK.value,
            "amount_ml": 80,
            "temperature": 36.8,
            "duration_minutes": 20
        }),
        (PhysiologicalNeedType.COMFORT, {
            "care_type": "swaddling",
            "technique_score": 80
        })
    ]
    
    for need_type, action_data in care_sequence:
        result = await manager.execute_care_action(need_type, action_data)
        print(f"执行 {need_type.value}: {result['message']}")
    
    print()


async def emergency_scenario():
    """紧急情况场景演示"""
    print("🚨 紧急情况场景演示")
    print("=" * 40)
    
    manager = PhysiologicalNeedsManager()
    
    # 模拟发烧情况
    manager.state.body_temperature = 38.5
    manager.state.comfort_level = 30
    
    print(f"紧急情况: 宝宝发烧 {manager.state.body_temperature}°C")
    
    # 评估体温需求
    temp_task = manager.tasks[PhysiologicalNeedType.TEMPERATURE]
    temp_urgency = await temp_task.assess_need(manager.state)
    temp_status = temp_task.get_temperature_status(manager.state)
    
    print(f"体温状态: {temp_status['status']} (紧急程度: {temp_urgency}/100)")
    print(f"建议: {temp_status['recommendation']}")
    print()
    
    # 执行降温措施
    cooling_result = await manager.execute_care_action(
        PhysiologicalNeedType.TEMPERATURE,
        {
            "action_type": "cool_down",
            "method": "physical_cooling"
        }
    )
    
    print(f"降温结果: {cooling_result['message']}")
    print(f"体温变化: {cooling_result['before_state']['temperature']:.1f}°C → {cooling_result['after_state']['temperature']:.1f}°C")
    print()


async def sleep_training_scenario():
    """睡眠训练场景演示"""
    print("😴 睡眠训练场景演示")
    print("=" * 40)
    
    manager = PhysiologicalNeedsManager()
    
    # 模拟睡眠债务积累
    manager.state.sleep_debt = 85
    manager.state.comfort_level = 60
    
    print(f"睡眠债务: {manager.state.sleep_debt}/100")
    
    # 获取睡眠建议
    sleep_task = manager.tasks[PhysiologicalNeedType.SLEEP]
    recommendations = sleep_task.get_sleep_recommendations(manager.state)
    
    print("睡眠建议:")
    print(f"  紧急程度: {recommendations['urgency']}/100")
    print(f"  推荐方法: {recommendations['recommended_method']}")
    print(f"  建议时长: {recommendations['optimal_duration']}分钟")
    for tip in recommendations['environment_tips']:
        print(f"  💡 {tip}")
    print()
    
    # 尝试不同的哄睡方法
    sleep_methods = [
        {"method": "rocking", "duration_minutes": 20, "environment_score": 70},
        {"method": "singing", "duration_minutes": 15, "environment_score": 80},
        {"method": "swaddling", "duration_minutes": 10, "environment_score": 90}
    ]
    
    for method_data in sleep_methods:
        print(f"尝试方法: {method_data['method']}")
        
        # 计算成功率
        effectiveness = sleep_task.calculate_effectiveness(method_data, manager.state)
        print(f"  预期成功率: {effectiveness:.1%}")
        
        # 执行哄睡
        result = await manager.execute_care_action(PhysiologicalNeedType.SLEEP, method_data)
        print(f"  结果: {result['message']}")
        
        if result['after_state']['sleep_debt'] < result['before_state']['sleep_debt']:
            print("  ✅ 成功入睡！")
            break
        else:
            print("  ❌ 入睡失败，尝试下一种方法")
        print()


async def feeding_optimization_scenario():
    """喂食优化场景演示"""
    print("🍼 喂食优化场景演示")
    print("=" * 40)
    
    manager = PhysiologicalNeedsManager()
    
    # 模拟不同年龄段的喂食需求
    age_scenarios = [
        {"age_months": 0, "name": "新生儿"},
        {"age_months": 3, "name": "3个月婴儿"},
        {"age_months": 8, "name": "8个月婴儿"}
    ]
    
    for scenario in age_scenarios:
        print(f"--- {scenario['name']} 喂食建议 ---")
        
        # 模拟饥饿状态
        manager.state.hunger_level = 70
        
        # 获取喂食建议
        feeding_task = manager.tasks[PhysiologicalNeedType.HUNGER]
        recommendations = feeding_task.get_feeding_recommendations(
            manager.state, scenario['age_months']
        )
        
        print(f"饥饿程度: {recommendations['urgency']}/100")
        print(f"推荐类型: {recommendations['recommended_type'].value}")
        print(f"推荐量: {recommendations['recommended_amount']}ml")
        print(f"最佳温度: {recommendations['optimal_temperature']}°C")
        print(f"预计时长: {recommendations['estimated_duration']}分钟")
        print()


async def comprehensive_care_cycle():
    """综合护理周期演示"""
    print("🔄 24小时护理周期演示")
    print("=" * 40)
    
    manager = PhysiologicalNeedsManager()
    
    # 模拟24小时护理周期
    time_points = [0, 3, 6, 9, 12, 15, 18, 21, 24]  # 每3小时一个时间点
    
    for i, hour in enumerate(time_points[:-1]):
        next_hour = time_points[i + 1]
        time_passed = next_hour - hour
        
        print(f"⏰ 时间: {hour:02d}:00 - {next_hour:02d}:00")
        
        # 模拟时间流逝
        await manager.simulate_time_passage(time_passed)
        
        # 获取优先级需求
        priority_needs = await manager.get_priority_needs(40)
        
        if priority_needs:
            print("需要护理:")
            for need_type, urgency in priority_needs[:2]:  # 只处理前2个最紧急的
                print(f"  🚨 {need_type.value}: {urgency}/100")
                
                # 根据需求类型执行相应护理
                if need_type == PhysiologicalNeedType.HUNGER:
                    action_data = {
                        "feeding_type": FeedingType.FORMULA.value,
                        "amount_ml": 100,
                        "temperature": 36.5,
                        "duration_minutes": 15
                    }
                elif need_type == PhysiologicalNeedType.DIAPER_CHANGE:
                    action_data = {
                        "diaper_type": DiaperType.WET.value,
                        "preparation_time": 20,
                        "execution_time": 90,
                        "cleanliness_score": 80,
                        "technique_score": 75
                    }
                elif need_type == PhysiologicalNeedType.SLEEP:
                    action_data = {
                        "method": "swaddling",
                        "duration_minutes": 30,
                        "environment_score": 85
                    }
                else:
                    continue
                
                result = await manager.execute_care_action(need_type, action_data)
                print(f"    护理结果: {result['message']}")
        else:
            print("  😊 宝宝状态良好，无需特殊护理")
        
        # 显示整体健康状况
        status = manager.get_comprehensive_status()
        wellbeing = status["overall_wellbeing"]
        print(f"  整体健康: {wellbeing['overall_score']:.1f}/100 {wellbeing['emoji']}")
        print()


async def main():
    """主演示函数"""
    print("🍼 生理需求任务接口完整演示")
    print("硬核父母岗前特训 - 生理护理专项")
    print("=" * 60)
    print()
    
    # 运行各种场景演示
    scenarios = [
        basic_care_scenario,
        emergency_scenario,
        sleep_training_scenario,
        feeding_optimization_scenario,
        comprehensive_care_cycle
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"📋 场景 {i}/{len(scenarios)}: {scenario.__name__}")
        await scenario()
        print("=" * 60)
        print()
    
    print("🎯 生理需求任务接口演示完成！")
    print()
    print("💡 系统特点总结:")
    print("✅ 全面的生理需求评估 (饥饿、睡眠、体温、舒适度等)")
    print("✅ 智能的护理建议系统")
    print("✅ 实时的效果评估和反馈")
    print("✅ 紧急情况的快速识别和处理")
    print("✅ 24小时护理周期的完整支持")
    print("✅ 不同年龄段的个性化护理方案")
    print()
    print("这个接口为硬核父母提供了科学、全面的婴儿生理护理指导！ 👶💪")


if __name__ == "__main__":
    asyncio.run(main())