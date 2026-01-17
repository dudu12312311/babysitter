"""
分龄育儿系统：硬核父母岗前特训
Age-Based Parenting System: Hardcore Parent Pre-Combat Training

按年龄阶段分层的育儿任务系统，涵盖生理需求、心理需求和惊喜时刻
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import random


class AgeStage(Enum):
    """年龄阶段"""
    NEWBORN = "0-3months"           # 0-3月：生理需求为主
    INFANT = "4-12months"           # 4-12月：安全探索期
    TODDLER = "1-3years"            # 1-3岁：情绪、行走、行为正向激励
    PRESCHOOL = "4-5years"          # 4-5岁：社交、儿童教育


class TaskType(Enum):
    """任务类型"""
    PHYSIOLOGICAL = "physiological"  # 生理需求
    PSYCHOLOGICAL = "psychological"  # 心理需求
    SAFETY = "safety"               # 安全探索
    EMOTIONAL = "emotional"         # 情绪管理
    BEHAVIORAL = "behavioral"       # 行为引导
    SOCIAL = "social"              # 社交技能
    EDUCATIONAL = "educational"     # 教育启蒙
    SURPRISE = "surprise"          # 惊喜时刻（彩蛋）


class EmotionType(Enum):
    """情绪类型 - 简化版"""
    HAPPY = "开心"        # 合并 happy + excited
    UPSET = "不开心"      # 合并 angry + frustrated + sad
    WORRIED = "担心"      # 合并 scared + anxious + jealous


@dataclass
class ChildState:
    """儿童状态 - 简化版"""
    # 基础状态
    age_months: int = 0
    happiness: int = 100            # 快乐度 (0-100)
    energy_level: int = 100         # 精力值 (0-100)
    
    # 生理状态 (0-3月主要)
    hunger_level: int = 0           # 饥饿程度 (0-100)
    sleep_debt: int = 0             # 睡眠债务 (0-100)
    comfort_level: int = 100        # 舒适度 (0-100)
    
    # 发展状态 (按年龄逐步重要)
    curiosity: int = 50             # 好奇心 (0-100)
    motor_skills: int = 0           # 运动技能 (0-100)
    language_skills: int = 0        # 语言技能 (0-100)
    emotional_regulation: int = 0   # 情绪调节 (0-100)
    social_confidence: int = 50     # 社交自信 (0-100)
    learning_motivation: int = 50   # 学习动机 (0-100)
    
    # 当前状态
    current_emotion: EmotionType = EmotionType.HAPPY
    last_feeding: datetime = field(default_factory=datetime.now)
    last_sleep: datetime = field(default_factory=datetime.now)


@dataclass
class ParentState:
    """父母状态 - 简化版"""
    confidence: int = 50            # 育儿自信 (0-100)
    stress_level: int = 0           # 压力值 (0-100)
    patience: int = 100             # 耐心值 (0-100)
    parenting_skills: int = 30      # 育儿技能 (0-100)
    
    # 统计数据
    successful_interventions: int = 0
    failed_interventions: int = 0
    total_parenting_score: int = 100
class AgeBasedTask(ABC):
    """年龄分层任务抽象基类"""
    
    def __init__(self, age_stage: AgeStage, task_type: TaskType):
        self.age_stage = age_stage
        self.task_type = task_type
        self.base_score = 10  # 基础分数
    
    @abstractmethod
    async def assess_need(self, child_state: ChildState, parent_state: ParentState) -> int:
        """评估任务需求紧急程度 (0-100)"""
        pass
    
    @abstractmethod
    async def execute_task(self, child_state: ChildState, parent_state: ParentState, 
                          action_data: Dict[str, Any]) -> Tuple[ChildState, ParentState, Dict[str, Any]]:
        """执行任务，返回更新后的状态和结果"""
        pass
    
    @abstractmethod
    def get_task_description(self) -> str:
        """获取任务描述"""
        pass


# ==================== 0-3月：生理需求阶段 ====================

class NewbornFeedingTask(AgeBasedTask):
    """新生儿喂食任务"""
    
    def __init__(self):
        super().__init__(AgeStage.NEWBORN, TaskType.PHYSIOLOGICAL)
        self.base_score = 15
    
    async def assess_need(self, child_state: ChildState, parent_state: ParentState) -> int:
        urgency = child_state.hunger_level
        
        # 时间因素
        time_since_feeding = (datetime.now() - child_state.last_feeding).total_seconds() / 3600
        if time_since_feeding > 2:  # 新生儿2小时喂一次
            urgency += int(time_since_feeding * 20)
        
        return min(100, urgency)
    
    async def execute_task(self, child_state: ChildState, parent_state: ParentState, 
                          action_data: Dict[str, Any]) -> Tuple[ChildState, ParentState, Dict[str, Any]]:
        
        feeding_type = action_data.get("feeding_type", "formula")
        temperature = action_data.get("temperature", 36.5)
        response_time = action_data.get("response_time", 60)  # 响应时间(秒)
        
        # 计算成功率
        success_rate = 0.8
        if temperature < 35 or temperature > 38:
            success_rate -= 0.3  # 温度不当
        if response_time > 300:  # 超过5分钟响应
            success_rate -= 0.2
        
        # 执行结果
        if random.random() < success_rate:
            # 喂食成功
            child_state.hunger_level = max(0, child_state.hunger_level - 70)
            child_state.comfort_level = min(100, child_state.comfort_level + 20)
            child_state.happiness = min(100, child_state.happiness + 15)
            child_state.last_feeding = datetime.now()
            
            # 父母状态改善
            parent_state.confidence = min(100, parent_state.confidence + 5)
            parent_state.successful_interventions += 1
            
            score_change = self.base_score
            message = "✅ 喂食成功！宝宝满足地吃饱了"
            
        else:
            # 喂食失败
            child_state.comfort_level = max(0, child_state.comfort_level - 10)
            parent_state.stress_level = min(100, parent_state.stress_level + 15)
            parent_state.patience = max(0, parent_state.patience - 10)
            parent_state.failed_interventions += 1
            
            score_change = -5
            message = "❌ 喂食遇到困难，宝宝还是不满足"
        
        # 副作用：喂食后可能需要换尿布
        if success_rate > 0.7:
            child_state.comfort_level = max(0, child_state.comfort_level - 5)  # 轻微不适
        
        result = {
            "success": random.random() < success_rate,
            "score_change": score_change,
            "message": message,
            "side_effects": ["可能需要拍嗝", "30分钟后可能需要换尿布"]
        }
        
        return child_state, parent_state, result
    
    def get_task_description(self) -> str:
        return "新生儿喂食：及时满足宝宝的营养需求，建立规律的喂食习惯"


class NewbornSleepTask(AgeBasedTask):
    """新生儿睡眠任务"""
    
    def __init__(self):
        super().__init__(AgeStage.NEWBORN, TaskType.PHYSIOLOGICAL)
        self.base_score = 12
    
    async def assess_need(self, child_state: ChildState, parent_state: ParentState) -> int:
        urgency = child_state.sleep_debt
        
        # 新生儿睡眠特点：短睡眠周期
        time_awake = (datetime.now() - child_state.last_sleep).total_seconds() / 3600
        if time_awake > 1.5:  # 醒着超过1.5小时
            urgency += int(time_awake * 30)
        
        # 其他因素影响睡眠
        if child_state.hunger_level > 60:
            urgency -= 20  # 饿了难以入睡
        if child_state.comfort_level < 50:
            urgency -= 15  # 不舒服难以入睡
        
        return max(0, min(100, urgency))
    
    async def execute_task(self, child_state: ChildState, parent_state: ParentState, 
                          action_data: Dict[str, Any]) -> Tuple[ChildState, ParentState, Dict[str, Any]]:
        
        method = action_data.get("method", "swaddling")  # 襁褓、摇晃、白噪音等
        environment_score = action_data.get("environment_score", 70)  # 环境评分
        patience_level = action_data.get("patience_level", parent_state.patience)
        
        # 计算成功率
        method_effectiveness = {
            "swaddling": 0.8,
            "rocking": 0.7,
            "white_noise": 0.6,
            "singing": 0.5,
            "patting": 0.6
        }
        
        base_success = method_effectiveness.get(method, 0.5)
        base_success += (environment_score - 50) / 100.0
        base_success += (patience_level - 50) / 200.0  # 父母耐心影响
        
        # 生理状态影响
        if child_state.hunger_level > 60:
            base_success *= 0.3
        if child_state.comfort_level < 50:
            base_success *= 0.4
        
        success = random.random() < base_success
        
        if success:
            # 哄睡成功
            child_state.sleep_debt = max(0, child_state.sleep_debt - 40)
            child_state.comfort_level = min(100, child_state.comfort_level + 25)
            child_state.energy_level = min(100, child_state.energy_level + 30)
            child_state.last_sleep = datetime.now()
            
            parent_state.confidence = min(100, parent_state.confidence + 8)
            parent_state.stress_level = max(0, parent_state.stress_level - 10)
            
            score_change = self.base_score + 3  # 哄睡成功额外奖励
            message = f"😴 哄睡成功！使用{method}方法很有效"
            
        else:
            # 哄睡失败
            child_state.sleep_debt = min(100, child_state.sleep_debt + 10)
            parent_state.patience = max(0, parent_state.patience - 15)
            parent_state.stress_level = min(100, parent_state.stress_level + 20)
            
            score_change = -3
            message = f"😫 哄睡失败，{method}方法这次没有效果"
        
        result = {
            "success": success,
            "score_change": score_change,
            "message": message,
            "tips": ["保持环境安静", "注意室温适宜", "检查是否需要换尿布"]
        }
        
        return child_state, parent_state, result
    
    def get_task_description(self) -> str:
        return "新生儿睡眠：帮助宝宝建立健康的睡眠模式，掌握有效的哄睡技巧"


class CryingDecodeTask(AgeBasedTask):
    """哭闹解码任务（0-3月核心任务）"""
    
    def __init__(self):
        super().__init__(AgeStage.NEWBORN, TaskType.PHYSIOLOGICAL)
        self.base_score = 20  # 高分值任务
        self.crying_patterns = {
            "hunger": {"frequency": "high", "intensity": "building", "duration": "persistent"},
            "tired": {"frequency": "low", "intensity": "whining", "duration": "intermittent"},
            "pain": {"frequency": "very_high", "intensity": "sharp", "duration": "sudden"},
            "discomfort": {"frequency": "medium", "intensity": "fussing", "duration": "variable"}
        }
    
    async def assess_need(self, child_state: ChildState, parent_state: ParentState) -> int:
        # 当多个生理需求未满足时，哭闹解码变得重要
        unmet_needs = 0
        if child_state.hunger_level > 60:
            unmet_needs += 1
        if child_state.sleep_debt > 70:
            unmet_needs += 1
        if child_state.comfort_level < 40:
            unmet_needs += 1
        
        urgency = unmet_needs * 25  # 每个未满足需求增加25点紧急度
        
        # 父母压力越大，越需要哭闹解码帮助
        if parent_state.stress_level > 70:
            urgency += 20
        
        return min(100, urgency)
    
    async def execute_task(self, child_state: ChildState, parent_state: ParentState, 
                          action_data: Dict[str, Any]) -> Tuple[ChildState, ParentState, Dict[str, Any]]:
        
        # 模拟哭声分析
        crying_duration = action_data.get("crying_duration", 120)  # 哭闹持续时间(秒)
        parent_guess = action_data.get("parent_guess", "unknown")  # 父母的猜测
        systematic_check = action_data.get("systematic_check", False)  # 是否系统性检查
        
        # 确定实际原因（基于当前状态）
        actual_causes = []
        if child_state.hunger_level > 60:
            actual_causes.append("hunger")
        if child_state.sleep_debt > 70:
            actual_causes.append("tired")
        if child_state.comfort_level < 40:
            actual_causes.append("discomfort")
        
        if not actual_causes:
            actual_causes = ["overstimulation"]  # 默认原因
        
        primary_cause = random.choice(actual_causes)
        
        # 评估父母的诊断准确性
        correct_diagnosis = parent_guess == primary_cause
        used_systematic_approach = systematic_check
        
        if correct_diagnosis and used_systematic_approach:
            # 完美诊断
            parent_state.confidence = min(100, parent_state.confidence + 15)
            parent_state.parenting_skills = min(100, parent_state.parenting_skills + 10)
            parent_state.stress_level = max(0, parent_state.stress_level - 20)
            
            score_change = self.base_score + 10
            message = f"🎯 完美诊断！正确识别了{primary_cause}，并使用了系统性方法"
            
        elif correct_diagnosis:
            # 正确诊断但方法不够系统
            parent_state.confidence = min(100, parent_state.confidence + 8)
            parent_state.parenting_skills = min(100, parent_state.parenting_skills + 5)
            
            score_change = self.base_score
            message = f"✅ 诊断正确！识别了{primary_cause}，建议使用更系统的检查方法"
            
        elif used_systematic_approach:
            # 方法正确但诊断错误
            parent_state.parenting_skills = min(100, parent_state.parenting_skills + 8)
            parent_state.confidence = min(100, parent_state.confidence + 3)
            
            score_change = self.base_score // 2
            message = f"📋 方法很好！虽然这次是{primary_cause}而不是{parent_guess}，但系统性检查很重要"
            
        else:
            # 诊断错误且方法不系统
            parent_state.stress_level = min(100, parent_state.stress_level + 10)
            parent_state.confidence = max(0, parent_state.confidence - 5)
            
            score_change = -5
            message = f"❌ 需要改进！实际原因是{primary_cause}，建议使用系统性检查清单"
        
        # 提供具体建议
        suggestions = {
            "hunger": ["检查上次喂食时间", "观察吸吮动作", "尝试喂食"],
            "tired": ["注意揉眼睛动作", "检查清醒时间", "尝试哄睡"],
            "discomfort": ["检查衣物是否过紧", "检查室温", "轻抚安慰"],
            "overstimulation": ["降低环境刺激", "轻柔安抚", "安静环境"]
        }
        
        result = {
            "success": correct_diagnosis,
            "score_change": score_change,
            "message": message,
            "actual_cause": primary_cause,
            "suggestions": suggestions.get(primary_cause, ["观察宝宝的具体表现"]),
            "learning_points": [
                "建立系统性检查习惯",
                "记录哭闹模式和时间",
                "相信自己的观察能力"
            ]
        }
        
        return child_state, parent_state, result
    
    def get_task_description(self) -> str:
        return "哭闹解码：学会识别不同类型的哭声，快速定位宝宝的真实需求"
# ==================== 4-12月：安全探索阶段 ====================

class SafeExplorationTask(AgeBasedTask):
    """安全探索任务"""
    
    def __init__(self):
        super().__init__(AgeStage.INFANT, TaskType.SAFETY)
        self.base_score = 18
    
    async def assess_need(self, child_state: ChildState, parent_state: ParentState) -> int:
        # 4-12月宝宝开始爬行、站立，好奇心强
        urgency = child_state.curiosity
        
        # 运动技能发展影响探索需求
        if child_state.motor_skills > 30:
            urgency += 20  # 运动能力强的宝宝更需要安全探索
        
        # 舒适度不足时需要更多引导
        if child_state.comfort_level < 60:
            urgency += 15
        
        return min(100, urgency)
    
    async def execute_task(self, child_state: ChildState, parent_state: ParentState, 
                          action_data: Dict[str, Any]) -> Tuple[ChildState, ParentState, Dict[str, Any]]:
        
        exploration_type = action_data.get("exploration_type", "crawling")  # 爬行、站立、抓握等
        safety_measures = action_data.get("safety_measures", [])  # 安全措施列表
        supervision_level = action_data.get("supervision_level", "close")  # 监督程度
        encouragement_given = action_data.get("encouragement_given", True)
        
        # 计算探索成功率
        base_success = 0.7
        
        # 安全措施影响
        safety_score = len(safety_measures) * 0.1
        base_success += min(0.2, safety_score)
        
        # 监督程度影响
        supervision_bonus = {
            "close": 0.2,      # 近距离监督
            "moderate": 0.1,   # 适度监督
            "distant": -0.1    # 远距离监督（可能不安全）
        }
        base_success += supervision_bonus.get(supervision_level, 0)
        
        # 鼓励影响
        if encouragement_given:
            base_success += 0.1
        
        success = random.random() < base_success
        
        if success:
            # 安全探索成功
            child_state.curiosity = min(100, child_state.curiosity + 15)
            child_state.motor_skills = min(100, child_state.motor_skills + 10)
            child_state.comfort_level = min(100, child_state.comfort_level + 8)
            child_state.happiness = min(100, child_state.happiness + 12)
            
            parent_state.confidence = min(100, parent_state.confidence + 10)
            parent_state.parenting_skills = min(100, parent_state.parenting_skills + 5)
            
            score_change = self.base_score
            message = f"🎯 安全探索成功！宝宝在{exploration_type}中获得了新体验"
            
        else:
            # 探索遇到困难或不安全
            child_state.comfort_level = max(0, child_state.comfort_level - 10)
            parent_state.stress_level = min(100, parent_state.stress_level + 15)
            
            score_change = -8
            message = f"⚠️ 探索遇到困难，需要调整安全措施或监督方式"
        
        result = {
            "success": success,
            "score_change": score_change,
            "message": message,
            "development_areas": ["运动技能", "空间认知", "安全意识"],
            "next_milestones": self._get_next_milestones(child_state.age_months)
        }
        
        return child_state, parent_state, result
    
    def _get_next_milestones(self, age_months: int) -> List[str]:
        """获取下一阶段发展里程碑"""
        if age_months < 6:
            return ["翻身", "坐立", "抓握"]
        elif age_months < 9:
            return ["爬行", "拉站", "捏取"]
        else:
            return ["独立站立", "迈步", "精细动作"]
    
    def get_task_description(self) -> str:
        return "安全探索：在确保安全的前提下，鼓励宝宝探索环境，发展运动技能"


class SensoryStimuationTask(AgeBasedTask):
    """感官刺激任务"""
    
    def __init__(self):
        super().__init__(AgeStage.INFANT, TaskType.PSYCHOLOGICAL)
        self.base_score = 15
    
    async def assess_need(self, child_state: ChildState, parent_state: ParentState) -> int:
        # 感官发展需求评估
        urgency = 50  # 基础需求
        
        # 好奇心强的宝宝需要更多感官刺激
        urgency += (child_state.curiosity - 50) // 2
        
        # 能量充沛时需要更多刺激
        if child_state.energy_level > 70:
            urgency += 20
        
        return min(100, urgency)
    
    async def execute_task(self, child_state: ChildState, parent_state: ParentState, 
                          action_data: Dict[str, Any]) -> Tuple[ChildState, ParentState, Dict[str, Any]]:
        
        stimulation_types = action_data.get("stimulation_types", [])  # 视觉、听觉、触觉等
        intensity_level = action_data.get("intensity_level", "moderate")  # 刺激强度
        duration_minutes = action_data.get("duration_minutes", 15)
        interactive = action_data.get("interactive", True)  # 是否互动
        
        # 计算刺激效果
        effectiveness = 0.6
        
        # 多样性奖励
        effectiveness += len(stimulation_types) * 0.05
        
        # 强度适宜性
        intensity_bonus = {
            "gentle": 0.1,
            "moderate": 0.15,
            "strong": -0.05  # 过强可能过度刺激
        }
        effectiveness += intensity_bonus.get(intensity_level, 0)
        
        # 时长适宜性
        if 10 <= duration_minutes <= 20:
            effectiveness += 0.1
        elif duration_minutes > 30:
            effectiveness -= 0.1  # 时间过长可能疲劳
        
        # 互动性奖励
        if interactive:
            effectiveness += 0.1
        
        success = random.random() < effectiveness
        
        if success:
            # 感官刺激成功
            child_state.curiosity = min(100, child_state.curiosity + 12)
            child_state.happiness = min(100, child_state.happiness + 15)
            child_state.language_skills = min(100, child_state.language_skills + 5)  # 语言发展
            
            parent_state.confidence = min(100, parent_state.confidence + 8)
            
            score_change = self.base_score
            message = f"🌈 感官刺激很成功！宝宝对{', '.join(stimulation_types)}反应很好"
            
        else:
            # 过度刺激或不适应
            child_state.energy_level = max(0, child_state.energy_level - 20)
            child_state.comfort_level = max(0, child_state.comfort_level - 10)
            
            score_change = -5
            message = "😵 刺激过度了，宝宝显得有些疲惫或不适应"
        
        result = {
            "success": success,
            "score_change": score_change,
            "message": message,
            "development_benefits": ["感官发展", "认知能力", "注意力"],
            "recommended_activities": self._get_age_appropriate_activities(child_state.age_months)
        }
        
        return child_state, parent_state, result
    
    def _get_age_appropriate_activities(self, age_months: int) -> List[str]:
        """获取适龄活动建议"""
        if age_months < 6:
            return ["黑白卡片", "摇铃", "柔软玩具"]
        elif age_months < 9:
            return ["彩色积木", "音乐玩具", "触感书"]
        else:
            return ["形状分类", "简单拼图", "乐器玩具"]
    
    def get_task_description(self) -> str:
        return "感官刺激：通过多样化的感官体验，促进宝宝大脑发育和认知能力"


# ==================== 1-3岁：情绪行为阶段 ====================

class EmotionRegulationTask(AgeBasedTask):
    """情绪调节任务"""
    
    def __init__(self):
        super().__init__(AgeStage.TODDLER, TaskType.EMOTIONAL)
        self.base_score = 25  # 高分值，情绪管理很重要
    
    async def assess_need(self, child_state: ChildState, parent_state: ParentState) -> int:
        # 情绪调节需求评估
        urgency = 100 - child_state.emotional_regulation
        
        # 当前情绪状态影响
        if child_state.current_emotion in [EmotionType.UPSET, EmotionType.WORRIED]:
            urgency += 30
        
        # 父母压力影响
        if parent_state.stress_level > 70:
            urgency += 15  # 父母压力大时更需要情绪管理
        
        return min(100, urgency)
    
    async def execute_task(self, child_state: ChildState, parent_state: ParentState, 
                          action_data: Dict[str, Any]) -> Tuple[ChildState, ParentState, Dict[str, Any]]:
        
        intervention_type = action_data.get("intervention_type", "comfort")
        emotion_naming = action_data.get("emotion_naming", False)  # 是否进行情绪命名
        breathing_exercise = action_data.get("breathing_exercise", False)  # 呼吸练习
        distraction_method = action_data.get("distraction_method", None)  # 转移注意力方法
        validation_given = action_data.get("validation_given", True)  # 是否给予情绪验证
        timeout_used = action_data.get("timeout_used", False)  # 是否使用暂停
        
        # 计算干预效果
        base_effectiveness = 0.5
        
        # 情绪验证很重要
        if validation_given:
            base_effectiveness += 0.2
        
        # 情绪命名教育价值高
        if emotion_naming:
            base_effectiveness += 0.15
        
        # 呼吸练习对大一点的孩子有效
        if breathing_exercise and child_state.age_months >= 24:
            base_effectiveness += 0.1
        
        # 转移注意力的效果
        if distraction_method:
            base_effectiveness += 0.1
        
        # 暂停方法需要谨慎使用
        if timeout_used:
            if child_state.age_months >= 24:
                base_effectiveness += 0.05  # 适龄使用
            else:
                base_effectiveness -= 0.1   # 过早使用效果不好
        
        success = random.random() < base_effectiveness
        
        if success:
            # 情绪调节成功
            child_state.emotional_regulation = min(100, child_state.emotional_regulation + 15)
            child_state.happiness = min(100, child_state.happiness + 20)
            child_state.security_feeling = min(100, child_state.security_feeling + 10)
            child_state.current_emotion = EmotionType.HAPPY
            
            parent_state.confidence = min(100, parent_state.confidence + 12)
            parent_state.stress_level = max(0, parent_state.stress_level - 15)
            
            score_change = self.base_score
            if emotion_naming:
                score_change += 5  # 情绪教育奖励
            
            message = f"💚 情绪调节成功！使用{intervention_type}方法很有效"
            
        else:
            # 情绪调节失败
            child_state.current_emotion = EmotionType.UPSET
            parent_state.stress_level = min(100, parent_state.stress_level + 20)
            parent_state.patience = max(0, parent_state.patience - 15)
            
            score_change = -10
            message = f"😤 情绪调节遇到困难，可能需要尝试其他方法"
        
        result = {
            "success": success,
            "score_change": score_change,
            "message": message,
            "emotion_before": child_state.current_emotion.value,
            "emotion_after": child_state.current_emotion.value,
            "learning_opportunities": [
                "情绪识别和命名",
                "自我调节技巧",
                "表达需求的方式"
            ],
            "parent_tips": [
                "保持冷静和耐心",
                "验证孩子的情绪",
                "教授应对策略"
            ]
        }
        
        return child_state, parent_state, result
    
    def get_task_description(self) -> str:
        return "情绪调节：帮助孩子识别、理解和管理情绪，培养情商和自控能力"


class PositiveBehaviorTask(AgeBasedTask):
    """正向行为激励任务"""
    
    def __init__(self):
        super().__init__(AgeStage.TODDLER, TaskType.BEHAVIORAL)
        self.base_score = 20
    
    async def assess_need(self, child_state: ChildState, parent_state: ParentState) -> int:
        # 行为引导需求
        urgency = 60  # 基础需求
        
        # 情绪调节能力低时更需要行为引导
        if child_state.emotional_regulation < 50:
            urgency += 20
        
        # 社交自信低时需要正向激励
        if child_state.social_confidence < 50:
            urgency += 15
        
        return min(100, urgency)
    
    async def execute_task(self, child_state: ChildState, parent_state: ParentState, 
                          action_data: Dict[str, Any]) -> Tuple[ChildState, ParentState, Dict[str, Any]]:
        
        behavior_target = action_data.get("behavior_target", "sharing")  # 目标行为
        reinforcement_type = action_data.get("reinforcement_type", "praise")  # 强化类型
        consistency_level = action_data.get("consistency_level", "high")  # 一致性程度
        immediate_feedback = action_data.get("immediate_feedback", True)  # 即时反馈
        specific_praise = action_data.get("specific_praise", True)  # 具体表扬
        
        # 计算强化效果
        base_effectiveness = 0.6
        
        # 即时反馈很重要
        if immediate_feedback:
            base_effectiveness += 0.15
        
        # 具体表扬比泛泛表扬更有效
        if specific_praise:
            base_effectiveness += 0.1
        
        # 一致性影响
        consistency_bonus = {
            "high": 0.2,
            "medium": 0.1,
            "low": -0.1
        }
        base_effectiveness += consistency_bonus.get(consistency_level, 0)
        
        # 强化类型效果
        reinforcement_effectiveness = {
            "praise": 0.15,
            "sticker_chart": 0.1,
            "special_activity": 0.12,
            "natural_consequence": 0.18
        }
        base_effectiveness += reinforcement_effectiveness.get(reinforcement_type, 0.05)
        
        success = random.random() < base_effectiveness
        
        if success:
            # 正向行为强化成功
            child_state.social_confidence = min(100, child_state.social_confidence + 12)
            child_state.happiness = min(100, child_state.happiness + 15)
            child_state.language_skills = min(100, child_state.language_skills + 10)  # 通过交流提升语言
            
            parent_state.confidence = min(100, parent_state.confidence + 10)
            parent_state.parenting_skills = min(100, parent_state.parenting_skills + 8)
            
            score_change = self.base_score
            if specific_praise and immediate_feedback:
                score_change += 5  # 最佳实践奖励
            
            message = f"⭐ 正向激励成功！{behavior_target}行为得到了很好的强化"
            
        else:
            # 强化效果不明显
            parent_state.confidence = max(0, parent_state.confidence - 5)
            
            score_change = -3
            message = f"🤔 这次强化效果不明显，可能需要调整方法或时机"
        
        result = {
            "success": success,
            "score_change": score_change,
            "message": message,
            "behavior_progress": f"{behavior_target}行为{'有所改善' if success else '需要继续努力'}",
            "reinforcement_tips": [
                "保持一致性",
                "及时给予反馈",
                "表扬要具体明确",
                "关注过程而非结果"
            ]
        }
        
        return child_state, parent_state, result
    
    def get_task_description(self) -> str:
        return "正向行为激励：通过科学的强化方法，培养孩子的良好行为习惯"
# ==================== 4-5岁：社交教育阶段 ====================

class SocialSkillsTask(AgeBasedTask):
    """社交技能任务"""
    
    def __init__(self):
        super().__init__(AgeStage.PRESCHOOL, TaskType.SOCIAL)
        self.base_score = 22
    
    async def assess_need(self, child_state: ChildState, parent_state: ParentState) -> int:
        # 社交技能需求评估
        urgency = 100 - child_state.social_confidence
        
        # 语言技能影响社交
        if child_state.language_skills < 60:
            urgency += 15
        
        return min(100, urgency)
    
    async def execute_task(self, child_state: ChildState, parent_state: ParentState, 
                          action_data: Dict[str, Any]) -> Tuple[ChildState, ParentState, Dict[str, Any]]:
        
        social_situation = action_data.get("social_situation", "playground")  # 社交场景
        skill_focus = action_data.get("skill_focus", "sharing")  # 技能重点
        adult_guidance = action_data.get("adult_guidance", "moderate")  # 成人指导程度
        peer_interaction = action_data.get("peer_interaction", True)  # 同伴互动
        conflict_resolution = action_data.get("conflict_resolution", False)  # 冲突解决
        
        # 计算社交成功率
        base_success = 0.6
        
        # 成人指导程度影响
        guidance_bonus = {
            "minimal": 0.05,    # 最少指导，培养独立性
            "moderate": 0.15,   # 适度指导，最佳平衡
            "intensive": 0.1    # 过度指导可能限制发展
        }
        base_success += guidance_bonus.get(adult_guidance, 0.1)
        
        # 同伴互动很重要
        if peer_interaction:
            base_success += 0.2
        
        # 冲突解决是高级技能
        if conflict_resolution:
            if child_state.emotional_regulation > 60:
                base_success += 0.1
            else:
                base_success -= 0.05  # 情绪调节不够时处理冲突困难
        
        # 语言技能影响社交表现
        if child_state.language_skills > 70:
            base_success += 0.1
        
        success = random.random() < base_success
        
        if success:
            # 社交技能发展成功
            child_state.social_confidence = min(100, child_state.social_confidence + 15)
            child_state.language_skills = min(100, child_state.language_skills + 12)  # 社交促进语言发展
            child_state.happiness = min(100, child_state.happiness + 10)
            
            parent_state.confidence = min(100, parent_state.confidence + 10)
            parent_state.parenting_skills = min(100, parent_state.parenting_skills + 6)
            
            score_change = self.base_score
            if conflict_resolution and success:
                score_change += 8  # 冲突解决奖励
            
            message = f"🤝 社交技能发展很好！在{social_situation}中{skill_focus}表现出色"
            
        else:
            # 社交遇到困难
            child_state.social_confidence = max(0, child_state.social_confidence - 8)
            parent_state.stress_level = min(100, parent_state.stress_level + 10)
            
            score_change = -8
            message = f"😔 社交遇到一些困难，需要更多练习和支持"
        
        result = {
            "success": success,
            "score_change": score_change,
            "message": message,
            "social_skills_developed": [
                "分享与合作",
                "沟通表达",
                "冲突解决",
                "同理心"
            ],
            "next_challenges": self._get_social_challenges(child_state.age_months)
        }
        
        return child_state, parent_state, result
    
    def _get_social_challenges(self, age_months: int) -> List[str]:
        """获取下一阶段社交挑战"""
        if age_months < 54:  # 4.5岁以下
            return ["学会等待", "轮流游戏", "表达需求"]
        else:
            return ["团队合作", "领导能力", "解决分歧"]
    
    def get_task_description(self) -> str:
        return "社交技能：培养孩子与他人互动、合作和沟通的能力"


class EarlyEducationTask(AgeBasedTask):
    """早期教育任务"""
    
    def __init__(self):
        super().__init__(AgeStage.PRESCHOOL, TaskType.EDUCATIONAL)
        self.base_score = 20
    
    async def assess_need(self, child_state: ChildState, parent_state: ParentState) -> int:
        # 教育需求评估
        urgency = child_state.learning_motivation
        
        # 语言技能发展需求
        if child_state.language_skills < 70:
            urgency += 20
        
        return min(100, urgency)
    
    async def execute_task(self, child_state: ChildState, parent_state: ParentState, 
                          action_data: Dict[str, Any]) -> Tuple[ChildState, ParentState, Dict[str, Any]]:
        
        learning_activity = action_data.get("learning_activity", "reading")  # 学习活动
        child_interest_level = action_data.get("child_interest_level", "medium")  # 孩子兴趣程度
        interactive_approach = action_data.get("interactive_approach", True)  # 互动式方法
        play_based_learning = action_data.get("play_based_learning", True)  # 游戏化学习
        difficulty_appropriate = action_data.get("difficulty_appropriate", True)  # 难度适宜
        
        # 计算学习效果
        base_effectiveness = 0.6
        
        # 兴趣是最好的老师
        interest_bonus = {
            "high": 0.25,
            "medium": 0.1,
            "low": -0.15
        }
        base_effectiveness += interest_bonus.get(child_interest_level, 0)
        
        # 互动式学习更有效
        if interactive_approach:
            base_effectiveness += 0.15
        
        # 游戏化学习符合幼儿特点
        if play_based_learning:
            base_effectiveness += 0.2
        
        # 难度适宜很重要
        if difficulty_appropriate:
            base_effectiveness += 0.1
        else:
            base_effectiveness -= 0.2  # 过难或过易都不好
        
        success = random.random() < base_effectiveness
        
        if success:
            # 教育活动成功
            child_state.learning_motivation = min(100, child_state.learning_motivation + 12)
            child_state.language_skills = min(100, child_state.language_skills + 10)
            child_state.happiness = min(100, child_state.happiness + 10)
            
            parent_state.confidence = min(100, parent_state.confidence + 8)
            parent_state.parenting_skills = min(100, parent_state.parenting_skills + 6)
            
            score_change = self.base_score
            if play_based_learning and interactive_approach:
                score_change += 5  # 最佳教育实践奖励
            
            message = f"📚 教育活动很成功！{learning_activity}激发了孩子的学习兴趣"
            
        else:
            # 教育活动效果不佳
            child_state.learning_motivation = max(0, child_state.learning_motivation - 8)
            parent_state.confidence = max(0, parent_state.confidence - 5)
            
            score_change = -5
            message = f"📖 这次学习活动效果不太好，可能需要调整方法或内容"
        
        result = {
            "success": success,
            "score_change": score_change,
            "message": message,
            "learning_areas": [
                "语言发展",
                "认知能力",
                "创造思维",
                "学习兴趣"
            ],
            "educational_tips": [
                "跟随孩子的兴趣",
                "保持互动和参与",
                "游戏化学习方式",
                "适当的挑战难度"
            ]
        }
        
        return child_state, parent_state, result
    
    def get_task_description(self) -> str:
        return "早期教育：通过适宜的教育活动，促进孩子全面发展"


# ==================== 惊喜时刻彩蛋任务 ====================

class SurpriseMomentTask(AgeBasedTask):
    """惊喜时刻彩蛋任务"""
    
    def __init__(self, age_stage: AgeStage):
        super().__init__(age_stage, TaskType.SURPRISE)
        self.base_score = 50  # 高分值彩蛋任务
        self.surprise_moments = {
            AgeStage.NEWBORN: [
                "第一次微笑", "第一次睡整夜", "第一次认出妈妈",
                "第一次抓握", "第一次翻身"
            ],
            AgeStage.INFANT: [
                "第一次坐立", "第一次爬行", "第一次叫妈妈/爸爸",
                "第一次拍手", "第一次挥手再见"
            ],
            AgeStage.TODDLER: [
                "第一次走路", "第一次说完整句子", "第一次主动分享",
                "第一次表达爱意", "第一次帮助他人"
            ],
            AgeStage.PRESCHOOL: [
                "第一次写自己名字", "第一次交到好朋友", "第一次独立解决问题",
                "第一次表演节目", "第一次表达复杂情感"
            ]
        }
    
    async def assess_need(self, child_state: ChildState, parent_state: ParentState) -> int:
        # 惊喜时刻是随机触发的，基于发展状态
        base_probability = 5  # 基础5%概率
        
        # 发展良好时更容易出现惊喜时刻
        if child_state.happiness > 80:
            base_probability += 10
        if child_state.comfort_level > 80:
            base_probability += 5
        
        # 父母状态好时更容易注意到惊喜时刻
        if parent_state.confidence > 70:
            base_probability += 8
        if parent_state.stress_level < 30:
            base_probability += 7
        
        return min(100, base_probability)
    
    async def execute_task(self, child_state: ChildState, parent_state: ParentState, 
                          action_data: Dict[str, Any]) -> Tuple[ChildState, ParentState, Dict[str, Any]]:
        
        # 随机选择一个惊喜时刻
        possible_moments = self.surprise_moments.get(self.age_stage, ["特殊时刻"])
        surprise_moment = random.choice(possible_moments)
        
        parent_recognition = action_data.get("parent_recognition", True)  # 父母是否识别到
        celebration_level = action_data.get("celebration_level", "moderate")  # 庆祝程度
        documentation = action_data.get("documentation", False)  # 是否记录
        sharing_with_others = action_data.get("sharing_with_others", False)  # 是否分享
        
        # 惊喜时刻总是成功的，关键是父母如何响应
        success = True
        
        # 基础奖励
        child_state.happiness = min(100, child_state.happiness + 25)
        child_state.comfort_level = min(100, child_state.comfort_level + 15)
        
        parent_state.confidence = min(100, parent_state.confidence + 20)
        parent_state.stress_level = max(0, parent_state.stress_level - 25)
        
        score_change = self.base_score
        
        # 父母响应奖励
        if parent_recognition:
            score_change += 10
            parent_state.parenting_skills = min(100, parent_state.parenting_skills + 10)
        
        # 庆祝程度奖励
        celebration_bonus = {
            "enthusiastic": 15,
            "moderate": 10,
            "minimal": 5
        }
        score_change += celebration_bonus.get(celebration_level, 10)
        
        # 记录和分享奖励
        if documentation:
            score_change += 5
            parent_state.parenting_skills = min(100, parent_state.parenting_skills + 5)
        
        if sharing_with_others:
            score_change += 5
            parent_state.confidence = min(100, parent_state.confidence + 5)
        
        # 根据年龄阶段给予特定发展奖励
        if self.age_stage == AgeStage.NEWBORN:
            child_state.comfort_level = min(100, child_state.comfort_level + 10)
        elif self.age_stage == AgeStage.INFANT:
            child_state.curiosity = min(100, child_state.curiosity + 15)
            child_state.motor_skills = min(100, child_state.motor_skills + 10)
        elif self.age_stage == AgeStage.TODDLER:
            child_state.emotional_regulation = min(100, child_state.emotional_regulation + 12)
            child_state.social_confidence = min(100, child_state.social_confidence + 10)
        elif self.age_stage == AgeStage.PRESCHOOL:
            child_state.learning_motivation = min(100, child_state.learning_motivation + 15)
            child_state.language_skills = min(100, child_state.language_skills + 12)
        
        message = f"🎉 惊喜时刻！{surprise_moment} - 这是珍贵的成长里程碑！"
        
        result = {
            "success": success,
            "score_change": score_change,
            "message": message,
            "surprise_moment": surprise_moment,
            "milestone_significance": self._get_milestone_significance(surprise_moment),
            "celebration_suggestions": [
                "拍照记录这个时刻",
                "与家人朋友分享喜悦",
                "在成长日记中记录",
                "给孩子额外的拥抱和表扬"
            ],
            "development_impact": "这个里程碑标志着重要的发展进步！"
        }
        
        return child_state, parent_state, result
    
    def _get_milestone_significance(self, moment: str) -> str:
        """获取里程碑意义"""
        significance_map = {
            "第一次微笑": "社交发展的重要开始，表明大脑发育良好",
            "第一次走路": "运动发展的重大突破，独立性的开始",
            "第一次说话": "语言发展的里程碑，沟通能力的体现",
            "第一次分享": "社交情感发展的重要标志，同理心的萌芽",
            "第一次写字": "精细动作和认知发展的结合体现"
        }
        
        for key, significance in significance_map.items():
            if key in moment:
                return significance
        
        return "每个第一次都是孩子成长路上的珍贵时刻"
    
    def get_task_description(self) -> str:
        return f"惊喜时刻：捕捉和庆祝{self.age_stage.value}阶段的珍贵成长里程碑"
# ==================== 分龄育儿系统管理器 ====================

class AgeBasedParentingManager:
    """分龄育儿系统管理器"""
    
    def __init__(self):
        self.child_state = ChildState()
        self.parent_state = ParentState()
        self.current_age_stage = self._determine_age_stage()
        self.available_tasks = self._initialize_tasks()
        self.completed_surprises = []
        
    def _determine_age_stage(self) -> AgeStage:
        """根据月龄确定年龄阶段"""
        age_months = self.child_state.age_months
        
        if age_months <= 3:
            return AgeStage.NEWBORN
        elif age_months <= 12:
            return AgeStage.INFANT
        elif age_months <= 36:
            return AgeStage.TODDLER
        else:
            return AgeStage.PRESCHOOL
    
    def _initialize_tasks(self) -> Dict[AgeStage, List[AgeBasedTask]]:
        """初始化各年龄阶段的任务"""
        tasks = {
            AgeStage.NEWBORN: [
                NewbornFeedingTask(),
                NewbornSleepTask(),
                CryingDecodeTask(),
                SurpriseMomentTask(AgeStage.NEWBORN)
            ],
            AgeStage.INFANT: [
                SafeExplorationTask(),
                SensoryStimuationTask(),
                SurpriseMomentTask(AgeStage.INFANT)
            ],
            AgeStage.TODDLER: [
                EmotionRegulationTask(),
                PositiveBehaviorTask(),
                SurpriseMomentTask(AgeStage.TODDLER)
            ],
            AgeStage.PRESCHOOL: [
                SocialSkillsTask(),
                EarlyEducationTask(),
                SurpriseMomentTask(AgeStage.PRESCHOOL)
            ]
        }
        return tasks
    
    async def assess_all_needs(self) -> Dict[str, Any]:
        """评估当前阶段所有任务需求"""
        current_tasks = self.available_tasks.get(self.current_age_stage, [])
        needs_assessment = {}
        
        for task in current_tasks:
            urgency = await task.assess_need(self.child_state, self.parent_state)
            needs_assessment[task.__class__.__name__] = {
                "urgency": urgency,
                "task_type": task.task_type.value,
                "description": task.get_task_description(),
                "base_score": task.base_score
            }
        
        return needs_assessment
    
    async def get_priority_tasks(self, threshold: int = 50) -> List[Tuple[AgeBasedTask, int]]:
        """获取优先级任务列表"""
        current_tasks = self.available_tasks.get(self.current_age_stage, [])
        priority_tasks = []
        
        for task in current_tasks:
            urgency = await task.assess_need(self.child_state, self.parent_state)
            if urgency >= threshold:
                priority_tasks.append((task, urgency))
        
        # 按紧急程度排序
        priority_tasks.sort(key=lambda x: x[1], reverse=True)
        return priority_tasks
    
    async def execute_task(self, task_class_name: str, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行指定任务"""
        current_tasks = self.available_tasks.get(self.current_age_stage, [])
        
        # 查找对应任务
        target_task = None
        for task in current_tasks:
            if task.__class__.__name__ == task_class_name:
                target_task = task
                break
        
        if not target_task:
            return {
                "success": False,
                "message": f"未找到任务: {task_class_name}",
                "score_change": 0
            }
        
        # 记录执行前状态
        before_child_state = {
            "happiness": self.child_state.happiness,
            "comfort_level": self.child_state.comfort_level,
            "emotional_regulation": self.child_state.emotional_regulation
        }
        
        before_parent_state = {
            "confidence": self.parent_state.confidence,
            "stress_level": self.parent_state.stress_level,
            "parenting_skills": self.parent_state.parenting_skills
        }
        
        # 执行任务
        try:
            self.child_state, self.parent_state, task_result = await target_task.execute_task(
                self.child_state, self.parent_state, action_data
            )
            
            # 更新父母总分
            score_change = task_result.get("score_change", 0)
            self.parent_state.total_parenting_score = max(0, min(1000, 
                self.parent_state.total_parenting_score + score_change))
            
            # 记录执行后状态
            after_child_state = {
                "happiness": self.child_state.happiness,
                "comfort_level": self.child_state.comfort_level,
                "emotional_regulation": self.child_state.emotional_regulation
            }
            
            after_parent_state = {
                "confidence": self.parent_state.confidence,
                "stress_level": self.parent_state.stress_level,
                "parenting_skills": self.parent_state.parenting_skills
            }
            
            # 检查是否需要升级到下一阶段
            self._check_age_progression()
            
            return {
                "success": task_result["success"],
                "message": task_result["message"],
                "score_change": score_change,
                "total_score": self.parent_state.total_parenting_score,
                "before_states": {
                    "child": before_child_state,
                    "parent": before_parent_state
                },
                "after_states": {
                    "child": after_child_state,
                    "parent": after_parent_state
                },
                "task_specific_data": {k: v for k, v in task_result.items() 
                                     if k not in ["success", "message", "score_change"]}
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"任务执行失败: {str(e)}",
                "score_change": -5
            }
    
    def _check_age_progression(self):
        """检查是否需要升级年龄阶段"""
        new_stage = self._determine_age_stage()
        if new_stage != self.current_age_stage:
            self.current_age_stage = new_stage
            # 可以在这里触发阶段升级的特殊事件
    
    async def trigger_surprise_moment(self) -> Optional[Dict[str, Any]]:
        """尝试触发惊喜时刻"""
        surprise_tasks = [task for task in self.available_tasks.get(self.current_age_stage, [])
                         if isinstance(task, SurpriseMomentTask)]
        
        if not surprise_tasks:
            return None
        
        surprise_task = surprise_tasks[0]
        urgency = await surprise_task.assess_need(self.child_state, self.parent_state)
        
        # 惊喜时刻是随机触发的
        if random.random() * 100 < urgency:
            action_data = {
                "parent_recognition": True,
                "celebration_level": "moderate",
                "documentation": random.choice([True, False]),
                "sharing_with_others": random.choice([True, False])
            }
            
            result = await self.execute_task("SurpriseMomentTask", action_data)
            if result["success"]:
                self.completed_surprises.append({
                    "moment": result["task_specific_data"]["surprise_moment"],
                    "timestamp": datetime.now(),
                    "age_stage": self.current_age_stage.value
                })
            
            return result
        
        return None
    
    def get_comprehensive_status(self) -> Dict[str, Any]:
        """获取综合状态报告"""
        return {
            "child_state": {
                "age_months": self.child_state.age_months,
                "age_stage": self.current_age_stage.value,
                "happiness": self.child_state.happiness,
                "comfort_level": self.child_state.comfort_level,
                "energy_level": self.child_state.energy_level,
                "emotional_regulation": self.child_state.emotional_regulation,
                "social_confidence": self.child_state.social_confidence,
                "learning_motivation": self.child_state.learning_motivation,
                "current_emotion": self.child_state.current_emotion.value
            },
            "parent_state": {
                "total_parenting_score": self.parent_state.total_parenting_score,
                "confidence": self.parent_state.confidence,
                "stress_level": self.parent_state.stress_level,
                "patience": self.parent_state.patience,
                "parenting_skills": self.parent_state.parenting_skills,
                "emotional_intelligence": self.parent_state.emotional_intelligence,
                "successful_interventions": self.parent_state.successful_interventions,
                "failed_interventions": self.parent_state.failed_interventions
            },
            "development_progress": self._calculate_development_progress(),
            "completed_surprises": len(self.completed_surprises),
            "recent_surprises": [s["moment"] for s in self.completed_surprises[-3:]]
        }
    
    def _calculate_development_progress(self) -> Dict[str, Any]:
        """计算发展进度"""
        if self.current_age_stage == AgeStage.NEWBORN:
            key_areas = {
                "生理适应": (self.child_state.comfort_level + (100 - self.child_state.hunger_level)) / 2,
                "睡眠规律": 100 - self.child_state.sleep_debt,
                "整体舒适": self.child_state.comfort_level
            }
        elif self.current_age_stage == AgeStage.INFANT:
            key_areas = {
                "运动发展": self.child_state.motor_skills,
                "认知发展": self.child_state.curiosity,
                "探索能力": self.child_state.comfort_level
            }
        elif self.current_age_stage == AgeStage.TODDLER:
            key_areas = {
                "情绪调节": self.child_state.emotional_regulation,
                "社交自信": self.child_state.social_confidence,
                "语言发展": self.child_state.language_skills
            }
        else:  # PRESCHOOL
            key_areas = {
                "社交技能": self.child_state.social_confidence,
                "学习动机": self.child_state.learning_motivation,
                "语言能力": self.child_state.language_skills
            }
        
        overall_progress = sum(key_areas.values()) / len(key_areas)
        
        return {
            "overall_progress": round(overall_progress, 1),
            "key_areas": key_areas,
            "stage_completion": min(100, overall_progress),
            "ready_for_next_stage": overall_progress > 75
        }
    
    async def simulate_time_passage(self, hours: float):
        """模拟时间流逝"""
        # 基础生理需求变化（主要影响0-3月）
        if self.current_age_stage == AgeStage.NEWBORN:
            self.child_state.hunger_level = min(100, self.child_state.hunger_level + hours * 20)
            self.child_state.sleep_debt = min(100, self.child_state.sleep_debt + hours * 15)
            self.child_state.diaper_wetness = min(100, self.child_state.diaper_wetness + hours * 12)
        
        # 能量和情绪的自然变化
        if self.child_state.energy_level > 50:
            self.child_state.energy_level = max(0, self.child_state.energy_level - hours * 8)
        
        # 父母状态的自然变化
        if self.parent_state.stress_level > 0:
            self.parent_state.stress_level = max(0, self.parent_state.stress_level - hours * 2)
        
        if self.parent_state.patience < 100:
            self.parent_state.patience = min(100, self.parent_state.patience + hours * 3)
        
        # 随机触发惊喜时刻
        surprise_result = await self.trigger_surprise_moment()
        return surprise_result


# 使用示例
async def demo_age_based_system():
    """演示分龄育儿系统"""
    print("👶 分龄育儿系统演示")
    print("=" * 50)
    
    manager = AgeBasedParentingManager()
    
    # 设置不同年龄进行演示
    age_scenarios = [
        (2, "2个月新生儿"),
        (8, "8个月婴儿"),
        (24, "2岁幼儿"),
        (48, "4岁学龄前儿童")
    ]
    
    for age_months, description in age_scenarios:
        print(f"\n=== {description} 演示 ===")
        
        # 设置年龄
        manager.child_state.age_months = age_months
        manager.current_age_stage = manager._determine_age_stage()
        manager.available_tasks = manager._initialize_tasks()
        
        # 评估需求
        needs = await manager.assess_all_needs()
        print(f"当前阶段: {manager.current_age_stage.value}")
        print("主要任务:")
        for task_name, task_info in needs.items():
            if task_info["urgency"] > 30:
                print(f"  🎯 {task_name}: {task_info['description']}")
                print(f"     紧急程度: {task_info['urgency']}/100, 基础分值: {task_info['base_score']}")
        
        # 获取状态
        status = manager.get_comprehensive_status()
        progress = status["development_progress"]
        print(f"发展进度: {progress['overall_progress']:.1f}/100")
        print(f"关键领域: {list(progress['key_areas'].keys())}")
        
        print()


if __name__ == "__main__":
    import asyncio
    asyncio.run(demo_age_based_system())