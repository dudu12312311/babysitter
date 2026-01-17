"""
生理需求任务接口
Physiological Needs Tasks Interface

处理婴儿基本生理需求的任务系统，包括喂食、换尿布、睡眠、体温调节等
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random


class PhysiologicalNeedType(Enum):
    """生理需求类型"""
    HUNGER = "hunger"                    # 饥饿
    DIAPER_CHANGE = "diaper_change"      # 换尿布
    SLEEP = "sleep"                      # 睡眠
    TEMPERATURE = "temperature"          # 体温调节
    COMFORT = "comfort"                  # 舒适度
    HYGIENE = "hygiene"                  # 卫生清洁


class FeedingType(Enum):
    """喂食类型"""
    BREAST_MILK = "breast_milk"          # 母乳
    FORMULA = "formula"                  # 配方奶
    SOLID_FOOD = "solid_food"            # 固体食物
    WATER = "water"                      # 水


class DiaperType(Enum):
    """尿布类型"""
    WET = "wet"                          # 湿尿布
    SOILED = "soiled"                    # 脏尿布
    EXPLOSIVE = "explosive"              # 爆炸性（生化危机）


class SleepState(Enum):
    """睡眠状态"""
    AWAKE = "awake"                      # 清醒
    DROWSY = "drowsy"                    # 困倦
    LIGHT_SLEEP = "light_sleep"          # 浅睡眠
    DEEP_SLEEP = "deep_sleep"            # 深睡眠
    REM_SLEEP = "rem_sleep"              # 快速眼动睡眠


@dataclass
class PhysiologicalState:
    """生理状态数据"""
    hunger_level: int = 0                # 饥饿程度 (0-100)
    diaper_wetness: int = 0              # 尿布湿润度 (0-100)
    sleep_debt: int = 0                  # 睡眠债务 (0-100)
    body_temperature: float = 36.5       # 体温 (摄氏度)
    comfort_level: int = 100             # 舒适度 (0-100)
    last_feeding: datetime = field(default_factory=datetime.now)
    last_diaper_change: datetime = field(default_factory=datetime.now)
    last_sleep: datetime = field(default_factory=datetime.now)
    current_sleep_state: SleepState = SleepState.AWAKE


@dataclass
class FeedingAction:
    """喂食行动数据"""
    feeding_type: FeedingType
    amount_ml: int                       # 喂食量(毫升)
    temperature: float                   # 温度
    duration_minutes: int                # 喂食时长
    success_rate: float = 1.0            # 成功率


@dataclass
class DiaperChangeAction:
    """换尿布行动数据"""
    diaper_type: DiaperType
    preparation_time: float              # 准备时间
    execution_time: float                # 执行时间
    cleanliness_score: int               # 清洁度评分 (0-100)
    technique_score: int                 # 技巧评分 (0-100)
class PhysiologicalNeedTask(ABC):
    """生理需求任务抽象基类"""
    
    @abstractmethod
    async def assess_need(self, state: PhysiologicalState) -> int:
        """评估需求紧急程度 (0-100)"""
        pass
    
    @abstractmethod
    async def execute_care(self, state: PhysiologicalState, action_data: Dict[str, Any]) -> PhysiologicalState:
        """执行护理行动"""
        pass
    
    @abstractmethod
    def validate_action(self, action_data: Dict[str, Any]) -> bool:
        """验证行动数据有效性"""
        pass
    
    @abstractmethod
    def calculate_effectiveness(self, action_data: Dict[str, Any], state: PhysiologicalState) -> float:
        """计算护理效果 (0.0-1.0)"""
        pass


class FeedingTask(PhysiologicalNeedTask):
    """喂食任务"""
    
    def __init__(self):
        self.feeding_intervals = {
            "newborn": 2,      # 新生儿每2小时喂一次
            "infant": 3,       # 婴儿每3小时喂一次
            "toddler": 4       # 幼儿每4小时喂一次
        }
        self.optimal_temperatures = {
            FeedingType.BREAST_MILK: (36.0, 37.0),
            FeedingType.FORMULA: (35.0, 37.0),
            FeedingType.SOLID_FOOD: (20.0, 40.0),
            FeedingType.WATER: (20.0, 25.0)
        }
    
    async def assess_need(self, state: PhysiologicalState) -> int:
        """评估饥饿程度"""
        time_since_feeding = (datetime.now() - state.last_feeding).total_seconds() / 3600
        
        # 基础饥饿值
        base_hunger = min(100, state.hunger_level + (time_since_feeding * 25))
        
        # 考虑其他因素
        if state.comfort_level < 50:
            base_hunger += 10  # 不舒适时更容易饿
        
        if state.sleep_debt > 70:
            base_hunger += 15  # 睡眠不足影响食欲调节
        
        return min(100, int(base_hunger))
    
    async def execute_care(self, state: PhysiologicalState, action_data: Dict[str, Any]) -> PhysiologicalState:
        """执行喂食"""
        feeding_action = FeedingAction(**action_data)
        
        # 检查温度是否合适
        temp_range = self.optimal_temperatures.get(feeding_action.feeding_type, (20, 40))
        temp_penalty = 0
        
        if feeding_action.temperature < temp_range[0]:
            temp_penalty = 20  # 太冷
        elif feeding_action.temperature > temp_range[1]:
            temp_penalty = 30  # 太热，更危险
        
        # 计算喂食效果
        effectiveness = self.calculate_effectiveness(action_data, state)
        effectiveness -= temp_penalty / 100.0
        effectiveness = max(0, min(1, effectiveness))
        
        # 更新状态
        hunger_reduction = int(effectiveness * 80)  # 最多减少80点饥饿
        state.hunger_level = max(0, state.hunger_level - hunger_reduction)
        state.last_feeding = datetime.now()
        
        # 副作用：喂食后可能需要换尿布
        if effectiveness > 0.7:
            state.diaper_wetness += random.randint(10, 25)
        
        # 舒适度影响
        if temp_penalty > 0:
            state.comfort_level = max(0, state.comfort_level - temp_penalty)
        else:
            state.comfort_level = min(100, state.comfort_level + 15)
        
        return state
    
    def validate_action(self, action_data: Dict[str, Any]) -> bool:
        """验证喂食行动"""
        required_fields = ["feeding_type", "amount_ml", "temperature", "duration_minutes"]
        
        if not all(field in action_data for field in required_fields):
            return False
        
        # 检查数值范围
        if not (10 <= action_data["amount_ml"] <= 300):
            return False
        
        if not (0 <= action_data["temperature"] <= 60):
            return False
        
        if not (1 <= action_data["duration_minutes"] <= 60):
            return False
        
        return True
    
    def calculate_effectiveness(self, action_data: Dict[str, Any], state: PhysiologicalState) -> float:
        """计算喂食效果"""
        base_effectiveness = 0.8
        
        # 根据喂食量调整
        amount = action_data["amount_ml"]
        if amount < 50:
            base_effectiveness -= 0.3  # 量太少
        elif amount > 200:
            base_effectiveness -= 0.2  # 量太多，可能吐奶
        
        # 根据持续时间调整
        duration = action_data["duration_minutes"]
        if duration < 5:
            base_effectiveness -= 0.2  # 太匆忙
        elif duration > 30:
            base_effectiveness -= 0.1  # 太慢，可能睡着
        
        # 根据饥饿程度调整
        if state.hunger_level > 80:
            base_effectiveness += 0.2  # 很饿时效果更好
        
        return max(0, min(1, base_effectiveness))
    
    def get_feeding_recommendations(self, state: PhysiologicalState, baby_age_months: int) -> Dict[str, Any]:
        """获取喂食建议"""
        recommendations = {
            "urgency": await self.assess_need(state),
            "recommended_amount": 120,  # 默认120ml
            "recommended_type": FeedingType.FORMULA,
            "optimal_temperature": 36.5,
            "estimated_duration": 15
        }
        
        # 根据年龄调整建议
        if baby_age_months < 1:  # 新生儿
            recommendations["recommended_amount"] = 60
            recommendations["recommended_type"] = FeedingType.BREAST_MILK
        elif baby_age_months < 6:  # 婴儿
            recommendations["recommended_amount"] = 120
        else:  # 幼儿
            recommendations["recommended_amount"] = 180
            recommendations["recommended_type"] = FeedingType.SOLID_FOOD
        
        return recommendations
class DiaperChangeTask(PhysiologicalNeedTask):
    """换尿布任务"""
    
    def __init__(self):
        self.change_thresholds = {
            DiaperType.WET: 60,        # 湿润度60以上需要换
            DiaperType.SOILED: 30,     # 有便便立即换
            DiaperType.EXPLOSIVE: 0    # 爆炸性立即换
        }
    
    async def assess_need(self, state: PhysiologicalState) -> int:
        """评估换尿布需求"""
        urgency = state.diaper_wetness
        
        # 时间因素
        time_since_change = (datetime.now() - state.last_diaper_change).total_seconds() / 3600
        if time_since_change > 3:  # 超过3小时
            urgency += 20
        
        # 舒适度影响
        if state.comfort_level < 30:
            urgency += 30  # 不舒适可能是尿布问题
        
        return min(100, urgency)
    
    async def execute_care(self, state: PhysiologicalState, action_data: Dict[str, Any]) -> PhysiologicalState:
        """执行换尿布"""
        change_action = DiaperChangeAction(**action_data)
        
        # 计算换尿布效果
        effectiveness = self.calculate_effectiveness(action_data, state)
        
        # 更新状态
        if effectiveness > 0.8:
            # 换得很好
            state.diaper_wetness = 0
            state.comfort_level = min(100, state.comfort_level + 25)
        elif effectiveness > 0.5:
            # 换得一般
            state.diaper_wetness = max(0, state.diaper_wetness - 70)
            state.comfort_level = min(100, state.comfort_level + 15)
        else:
            # 换得不好
            state.diaper_wetness = max(0, state.diaper_wetness - 30)
            state.comfort_level = max(0, state.comfort_level - 10)
        
        state.last_diaper_change = datetime.now()
        
        # 特殊情况处理
        if change_action.diaper_type == DiaperType.EXPLOSIVE:
            # 生化危机情况
            if effectiveness < 0.6:
                state.comfort_level = max(0, state.comfort_level - 20)
                # 可能弄脏衣服，需要额外清洁
        
        return state
    
    def validate_action(self, action_data: Dict[str, Any]) -> bool:
        """验证换尿布行动"""
        required_fields = ["diaper_type", "preparation_time", "execution_time", 
                          "cleanliness_score", "technique_score"]
        
        if not all(field in action_data for field in required_fields):
            return False
        
        # 检查数值范围
        if not (0 <= action_data["preparation_time"] <= 300):  # 最多5分钟准备
            return False
        
        if not (30 <= action_data["execution_time"] <= 600):   # 30秒到10分钟执行
            return False
        
        if not (0 <= action_data["cleanliness_score"] <= 100):
            return False
        
        if not (0 <= action_data["technique_score"] <= 100):
            return False
        
        return True
    
    def calculate_effectiveness(self, action_data: Dict[str, Any], state: PhysiologicalState) -> float:
        """计算换尿布效果"""
        # 基础效果由清洁度和技巧决定
        base_effectiveness = (action_data["cleanliness_score"] + action_data["technique_score"]) / 200.0
        
        # 时间因素
        total_time = action_data["preparation_time"] + action_data["execution_time"]
        if total_time < 60:
            base_effectiveness -= 0.2  # 太匆忙
        elif total_time > 300:
            base_effectiveness -= 0.1  # 太慢，宝宝不耐烦
        
        # 尿布类型影响难度
        diaper_type = DiaperType(action_data["diaper_type"])
        if diaper_type == DiaperType.EXPLOSIVE:
            base_effectiveness *= 0.7  # 生化危机更难处理
        elif diaper_type == DiaperType.SOILED:
            base_effectiveness *= 0.8  # 有便便稍难
        
        return max(0, min(1, base_effectiveness))
    
    def get_change_difficulty(self, state: PhysiologicalState) -> str:
        """获取换尿布难度评估"""
        if state.diaper_wetness > 90:
            return "EXPLOSIVE"  # 生化危机级别
        elif state.diaper_wetness > 70:
            return "DIFFICULT"  # 困难
        elif state.diaper_wetness > 40:
            return "MODERATE"   # 中等
        else:
            return "EASY"       # 简单


class SleepTask(PhysiologicalNeedTask):
    """睡眠任务"""
    
    def __init__(self):
        self.sleep_cycles = {
            "newborn": 45,     # 新生儿45分钟一个周期
            "infant": 60,      # 婴儿60分钟一个周期
            "toddler": 90      # 幼儿90分钟一个周期
        }
        self.daily_sleep_needs = {
            "newborn": 16,     # 新生儿每天16小时
            "infant": 14,      # 婴儿每天14小时
            "toddler": 12      # 幼儿每天12小时
        }
    
    async def assess_need(self, state: PhysiologicalState) -> int:
        """评估睡眠需求"""
        urgency = state.sleep_debt
        
        # 时间因素
        time_since_sleep = (datetime.now() - state.last_sleep).total_seconds() / 3600
        if time_since_sleep > 2:  # 超过2小时没睡
            urgency += int(time_since_sleep * 15)
        
        # 其他生理需求影响睡眠
        if state.hunger_level > 70:
            urgency -= 20  # 太饿难以入睡
        
        if state.diaper_wetness > 60:
            urgency -= 15  # 尿布湿难以入睡
        
        if state.comfort_level < 40:
            urgency -= 25  # 不舒适难以入睡
        
        return max(0, min(100, urgency))
    
    async def execute_care(self, state: PhysiologicalState, action_data: Dict[str, Any]) -> PhysiologicalState:
        """执行睡眠护理"""
        sleep_method = action_data.get("method", "rocking")
        duration = action_data.get("duration_minutes", 30)
        environment_score = action_data.get("environment_score", 70)
        
        # 计算入睡成功率
        success_rate = self.calculate_effectiveness(action_data, state)
        
        if random.random() < success_rate:
            # 成功入睡
            sleep_reduction = min(duration * 2, state.sleep_debt)
            state.sleep_debt = max(0, state.sleep_debt - sleep_reduction)
            state.comfort_level = min(100, state.comfort_level + 20)
            state.current_sleep_state = SleepState.LIGHT_SLEEP
            state.last_sleep = datetime.now()
        else:
            # 入睡失败
            state.sleep_debt = min(100, state.sleep_debt + 10)
            state.comfort_level = max(0, state.comfort_level - 15)
        
        return state
    
    def validate_action(self, action_data: Dict[str, Any]) -> bool:
        """验证睡眠护理行动"""
        if "method" not in action_data:
            return False
        
        valid_methods = ["rocking", "singing", "patting", "swaddling", "white_noise"]
        if action_data["method"] not in valid_methods:
            return False
        
        duration = action_data.get("duration_minutes", 30)
        if not (5 <= duration <= 120):
            return False
        
        environment_score = action_data.get("environment_score", 70)
        if not (0 <= environment_score <= 100):
            return False
        
        return True
    
    def calculate_effectiveness(self, action_data: Dict[str, Any], state: PhysiologicalState) -> float:
        """计算睡眠护理效果"""
        base_effectiveness = 0.6
        
        # 环境因素
        environment_score = action_data.get("environment_score", 70)
        base_effectiveness += (environment_score - 50) / 100.0
        
        # 方法效果
        method_effectiveness = {
            "rocking": 0.8,
            "singing": 0.7,
            "patting": 0.6,
            "swaddling": 0.9,
            "white_noise": 0.7
        }
        method = action_data.get("method", "rocking")
        base_effectiveness *= method_effectiveness.get(method, 0.5)
        
        # 生理状态影响
        if state.hunger_level > 70:
            base_effectiveness *= 0.3  # 太饿难以入睡
        
        if state.diaper_wetness > 60:
            base_effectiveness *= 0.4  # 尿布湿难以入睡
        
        if state.comfort_level < 30:
            base_effectiveness *= 0.2  # 不舒适难以入睡
        
        # 睡眠债务越高，越容易入睡
        if state.sleep_debt > 80:
            base_effectiveness += 0.3
        
        return max(0, min(1, base_effectiveness))
    
    def get_sleep_recommendations(self, state: PhysiologicalState) -> Dict[str, Any]:
        """获取睡眠建议"""
        urgency = await self.assess_need(state)
        
        recommendations = {
            "urgency": urgency,
            "recommended_method": "swaddling",
            "optimal_duration": 60,
            "environment_tips": []
        }
        
        # 根据状态给出建议
        if state.hunger_level > 50:
            recommendations["environment_tips"].append("先喂食再哄睡")
        
        if state.diaper_wetness > 40:
            recommendations["environment_tips"].append("先换尿布再哄睡")
        
        if urgency > 80:
            recommendations["recommended_method"] = "swaddling"
            recommendations["environment_tips"].append("使用白噪音")
        
        return recommendations
class TemperatureRegulationTask(PhysiologicalNeedTask):
    """体温调节任务"""
    
    def __init__(self):
        self.normal_temp_range = (36.0, 37.5)  # 正常体温范围
        self.fever_threshold = 38.0             # 发烧阈值
        self.hypothermia_threshold = 35.0       # 体温过低阈值
    
    async def assess_need(self, state: PhysiologicalState) -> int:
        """评估体温调节需求"""
        temp = state.body_temperature
        
        if temp >= self.fever_threshold:
            # 发烧
            urgency = min(100, int((temp - self.fever_threshold) * 50) + 70)
        elif temp <= self.hypothermia_threshold:
            # 体温过低
            urgency = min(100, int((self.hypothermia_threshold - temp) * 50) + 70)
        elif temp < self.normal_temp_range[0]:
            # 偏低
            urgency = int((self.normal_temp_range[0] - temp) * 30) + 30
        elif temp > self.normal_temp_range[1]:
            # 偏高
            urgency = int((temp - self.normal_temp_range[1]) * 30) + 30
        else:
            # 正常范围
            urgency = 0
        
        return min(100, urgency)
    
    async def execute_care(self, state: PhysiologicalState, action_data: Dict[str, Any]) -> PhysiologicalState:
        """执行体温调节"""
        action_type = action_data.get("action_type", "monitor")
        effectiveness = self.calculate_effectiveness(action_data, state)
        
        current_temp = state.body_temperature
        
        if action_type == "cool_down":
            # 降温措施
            temp_reduction = effectiveness * 1.5
            state.body_temperature = max(35.0, current_temp - temp_reduction)
            
        elif action_type == "warm_up":
            # 保温措施
            temp_increase = effectiveness * 1.0
            state.body_temperature = min(39.0, current_temp + temp_increase)
            
        elif action_type == "medication":
            # 药物治疗（需要专业指导）
            if current_temp >= self.fever_threshold:
                temp_reduction = effectiveness * 2.0
                state.body_temperature = max(36.0, current_temp - temp_reduction)
            
        elif action_type == "monitor":
            # 仅监测，不做处理
            pass
        
        # 体温异常影响舒适度
        urgency = await self.assess_need(state)
        if urgency > 50:
            state.comfort_level = max(0, state.comfort_level - (urgency - 50))
        else:
            state.comfort_level = min(100, state.comfort_level + 10)
        
        return state
    
    def validate_action(self, action_data: Dict[str, Any]) -> bool:
        """验证体温调节行动"""
        if "action_type" not in action_data:
            return False
        
        valid_actions = ["cool_down", "warm_up", "medication", "monitor"]
        if action_data["action_type"] not in valid_actions:
            return False
        
        # 检查药物使用是否有专业指导
        if action_data["action_type"] == "medication":
            if not action_data.get("professional_guidance", False):
                return False
        
        return True
    
    def calculate_effectiveness(self, action_data: Dict[str, Any], state: PhysiologicalState) -> float:
        """计算体温调节效果"""
        action_type = action_data.get("action_type", "monitor")
        current_temp = state.body_temperature
        
        if action_type == "cool_down":
            if current_temp > self.normal_temp_range[1]:
                return 0.8  # 体温高时降温效果好
            else:
                return 0.3  # 正常体温时降温效果差
                
        elif action_type == "warm_up":
            if current_temp < self.normal_temp_range[0]:
                return 0.8  # 体温低时保温效果好
            else:
                return 0.3  # 正常体温时保温效果差
                
        elif action_type == "medication":
            if current_temp >= self.fever_threshold:
                return 0.9  # 发烧时药物效果好
            else:
                return 0.1  # 正常体温时不应用药
                
        elif action_type == "monitor":
            return 0.5  # 监测本身有一定价值
        
        return 0.5
    
    def get_temperature_status(self, state: PhysiologicalState) -> Dict[str, Any]:
        """获取体温状态"""
        temp = state.body_temperature
        
        if temp >= 39.0:
            status = "HIGH_FEVER"
            severity = "CRITICAL"
            recommendation = "立即就医"
        elif temp >= self.fever_threshold:
            status = "FEVER"
            severity = "HIGH"
            recommendation = "物理降温，考虑就医"
        elif temp > self.normal_temp_range[1]:
            status = "SLIGHTLY_HIGH"
            severity = "MODERATE"
            recommendation = "注意观察，适当降温"
        elif temp < self.hypothermia_threshold:
            status = "HYPOTHERMIA"
            severity = "CRITICAL"
            recommendation = "立即保温并就医"
        elif temp < self.normal_temp_range[0]:
            status = "SLIGHTLY_LOW"
            severity = "MODERATE"
            recommendation = "注意保温"
        else:
            status = "NORMAL"
            severity = "LOW"
            recommendation = "继续监测"
        
        return {
            "temperature": temp,
            "status": status,
            "severity": severity,
            "recommendation": recommendation,
            "urgency": await self.assess_need(state)
        }


class ComfortTask(PhysiologicalNeedTask):
    """舒适度任务"""
    
    def __init__(self):
        self.comfort_factors = [
            "clothing_comfort",    # 衣物舒适度
            "position_comfort",    # 姿势舒适度
            "environment_comfort", # 环境舒适度
            "emotional_comfort"    # 情感舒适度
        ]
    
    async def assess_need(self, state: PhysiologicalState) -> int:
        """评估舒适度需求"""
        # 舒适度越低，需求越高
        urgency = 100 - state.comfort_level
        
        # 其他生理需求影响舒适度
        if state.hunger_level > 60:
            urgency += 20
        
        if state.diaper_wetness > 50:
            urgency += 25
        
        if state.sleep_debt > 70:
            urgency += 15
        
        temp_urgency = await TemperatureRegulationTask().assess_need(state)
        urgency += temp_urgency // 2
        
        return min(100, urgency)
    
    async def execute_care(self, state: PhysiologicalState, action_data: Dict[str, Any]) -> PhysiologicalState:
        """执行舒适度护理"""
        care_type = action_data.get("care_type", "general_comfort")
        effectiveness = self.calculate_effectiveness(action_data, state)
        
        comfort_improvement = int(effectiveness * 30)
        state.comfort_level = min(100, state.comfort_level + comfort_improvement)
        
        # 特定护理类型的额外效果
        if care_type == "swaddling":
            # 襁褓有助于睡眠
            state.sleep_debt = max(0, state.sleep_debt - 10)
        elif care_type == "massage":
            # 按摩有助于消化和循环
            state.comfort_level = min(100, state.comfort_level + 10)
        elif care_type == "skin_to_skin":
            # 肌肤接触有助于情感连接和体温调节
            state.comfort_level = min(100, state.comfort_level + 15)
            if abs(state.body_temperature - 36.5) > 0.5:
                # 帮助体温调节
                target_temp = 36.5
                temp_diff = target_temp - state.body_temperature
                state.body_temperature += temp_diff * 0.3
        
        return state
    
    def validate_action(self, action_data: Dict[str, Any]) -> bool:
        """验证舒适度护理行动"""
        if "care_type" not in action_data:
            return False
        
        valid_care_types = [
            "general_comfort", "swaddling", "massage", 
            "skin_to_skin", "position_change", "environment_adjust"
        ]
        
        if action_data["care_type"] not in valid_care_types:
            return False
        
        return True
    
    def calculate_effectiveness(self, action_data: Dict[str, Any], state: PhysiologicalState) -> float:
        """计算舒适度护理效果"""
        care_type = action_data.get("care_type", "general_comfort")
        
        # 不同护理类型的基础效果
        base_effectiveness = {
            "general_comfort": 0.6,
            "swaddling": 0.8,
            "massage": 0.7,
            "skin_to_skin": 0.9,
            "position_change": 0.5,
            "environment_adjust": 0.6
        }.get(care_type, 0.5)
        
        # 当前舒适度越低，护理效果越好
        if state.comfort_level < 30:
            base_effectiveness += 0.3
        elif state.comfort_level < 60:
            base_effectiveness += 0.1
        
        # 技巧评分影响
        technique_score = action_data.get("technique_score", 70)
        base_effectiveness *= (technique_score / 100.0)
        
        return max(0, min(1, base_effectiveness))
class PhysiologicalNeedsManager:
    """生理需求管理器"""
    
    def __init__(self):
        self.tasks = {
            PhysiologicalNeedType.HUNGER: FeedingTask(),
            PhysiologicalNeedType.DIAPER_CHANGE: DiaperChangeTask(),
            PhysiologicalNeedType.SLEEP: SleepTask(),
            PhysiologicalNeedType.TEMPERATURE: TemperatureRegulationTask(),
            PhysiologicalNeedType.COMFORT: ComfortTask()
        }
        self.state = PhysiologicalState()
    
    async def assess_all_needs(self) -> Dict[PhysiologicalNeedType, int]:
        """评估所有生理需求"""
        needs_assessment = {}
        
        for need_type, task in self.tasks.items():
            urgency = await task.assess_need(self.state)
            needs_assessment[need_type] = urgency
        
        return needs_assessment
    
    async def get_priority_needs(self, threshold: int = 50) -> List[tuple]:
        """获取优先级需求列表"""
        needs = await self.assess_all_needs()
        priority_needs = [
            (need_type, urgency) 
            for need_type, urgency in needs.items() 
            if urgency >= threshold
        ]
        
        # 按紧急程度排序
        priority_needs.sort(key=lambda x: x[1], reverse=True)
        return priority_needs
    
    async def execute_care_action(self, need_type: PhysiologicalNeedType, 
                                 action_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行护理行动"""
        if need_type not in self.tasks:
            return {"success": False, "message": "未知的需求类型"}
        
        task = self.tasks[need_type]
        
        # 验证行动数据
        if not task.validate_action(action_data):
            return {"success": False, "message": "无效的行动数据"}
        
        # 记录执行前状态
        before_state = {
            "comfort": self.state.comfort_level,
            "hunger": self.state.hunger_level,
            "diaper_wetness": self.state.diaper_wetness,
            "sleep_debt": self.state.sleep_debt,
            "temperature": self.state.body_temperature
        }
        
        # 执行护理
        try:
            self.state = await task.execute_care(self.state, action_data)
            effectiveness = task.calculate_effectiveness(action_data, self.state)
            
            # 记录执行后状态
            after_state = {
                "comfort": self.state.comfort_level,
                "hunger": self.state.hunger_level,
                "diaper_wetness": self.state.diaper_wetness,
                "sleep_debt": self.state.sleep_debt,
                "temperature": self.state.body_temperature
            }
            
            return {
                "success": True,
                "effectiveness": effectiveness,
                "before_state": before_state,
                "after_state": after_state,
                "message": self._generate_feedback_message(need_type, effectiveness)
            }
            
        except Exception as e:
            return {"success": False, "message": f"执行失败: {str(e)}"}
    
    def _generate_feedback_message(self, need_type: PhysiologicalNeedType, 
                                  effectiveness: float) -> str:
        """生成反馈消息"""
        if effectiveness >= 0.9:
            level = "完美"
        elif effectiveness >= 0.7:
            level = "优秀"
        elif effectiveness >= 0.5:
            level = "良好"
        elif effectiveness >= 0.3:
            level = "一般"
        else:
            level = "需要改进"
        
        need_names = {
            PhysiologicalNeedType.HUNGER: "喂食",
            PhysiologicalNeedType.DIAPER_CHANGE: "换尿布",
            PhysiologicalNeedType.SLEEP: "哄睡",
            PhysiologicalNeedType.TEMPERATURE: "体温调节",
            PhysiologicalNeedType.COMFORT: "舒适护理"
        }
        
        need_name = need_names.get(need_type, "护理")
        return f"{need_name}执行{level}！效果评分: {effectiveness:.1%}"
    
    def get_comprehensive_status(self) -> Dict[str, Any]:
        """获取综合状态报告"""
        return {
            "physiological_state": {
                "hunger_level": self.state.hunger_level,
                "diaper_wetness": self.state.diaper_wetness,
                "sleep_debt": self.state.sleep_debt,
                "body_temperature": self.state.body_temperature,
                "comfort_level": self.state.comfort_level,
                "current_sleep_state": self.state.current_sleep_state.value
            },
            "last_care_times": {
                "feeding": self.state.last_feeding.isoformat(),
                "diaper_change": self.state.last_diaper_change.isoformat(),
                "sleep": self.state.last_sleep.isoformat()
            },
            "overall_wellbeing": self._calculate_overall_wellbeing()
        }
    
    def _calculate_overall_wellbeing(self) -> Dict[str, Any]:
        """计算整体健康状况"""
        # 各项指标权重
        weights = {
            "comfort": 0.3,
            "hunger": 0.2,
            "sleep": 0.2,
            "diaper": 0.15,
            "temperature": 0.15
        }
        
        # 计算各项得分（0-100）
        comfort_score = self.state.comfort_level
        hunger_score = 100 - self.state.hunger_level
        sleep_score = 100 - self.state.sleep_debt
        diaper_score = 100 - self.state.diaper_wetness
        
        # 体温得分
        temp_diff = abs(self.state.body_temperature - 36.5)
        temp_score = max(0, 100 - (temp_diff * 50))
        
        # 加权平均
        overall_score = (
            comfort_score * weights["comfort"] +
            hunger_score * weights["hunger"] +
            sleep_score * weights["sleep"] +
            diaper_score * weights["diaper"] +
            temp_score * weights["temperature"]
        )
        
        # 状态评级
        if overall_score >= 90:
            status = "优秀"
            emoji = "😊"
        elif overall_score >= 75:
            status = "良好"
            emoji = "🙂"
        elif overall_score >= 60:
            status = "一般"
            emoji = "😐"
        elif overall_score >= 40:
            status = "需要关注"
            emoji = "😟"
        else:
            status = "需要紧急护理"
            emoji = "😢"
        
        return {
            "overall_score": round(overall_score, 1),
            "status": status,
            "emoji": emoji,
            "individual_scores": {
                "comfort": comfort_score,
                "hunger": hunger_score,
                "sleep": sleep_score,
                "diaper": diaper_score,
                "temperature": temp_score
            }
        }
    
    async def simulate_time_passage(self, hours: float):
        """模拟时间流逝对生理状态的影响"""
        # 饥饿增加
        hunger_increase = hours * 15  # 每小时增加15点饥饿
        self.state.hunger_level = min(100, self.state.hunger_level + hunger_increase)
        
        # 尿布湿润度增加
        wetness_increase = hours * 10  # 每小时增加10点湿润度
        self.state.diaper_wetness = min(100, self.state.diaper_wetness + wetness_increase)
        
        # 睡眠债务增加（如果醒着）
        if self.state.current_sleep_state == SleepState.AWAKE:
            sleep_debt_increase = hours * 20  # 每小时增加20点睡眠债务
            self.state.sleep_debt = min(100, self.state.sleep_debt + sleep_debt_increase)
        else:
            # 如果在睡觉，减少睡眠债务
            sleep_debt_decrease = hours * 30
            self.state.sleep_debt = max(0, self.state.sleep_debt - sleep_debt_decrease)
        
        # 舒适度受其他因素影响
        comfort_penalty = 0
        if self.state.hunger_level > 70:
            comfort_penalty += 10
        if self.state.diaper_wetness > 60:
            comfort_penalty += 15
        if self.state.sleep_debt > 80:
            comfort_penalty += 20
        
        self.state.comfort_level = max(0, self.state.comfort_level - comfort_penalty)


# 使用示例和测试函数
async def demo_physiological_needs():
    """演示生理需求系统"""
    print("🍼 生理需求任务系统演示")
    print("=" * 50)
    
    manager = PhysiologicalNeedsManager()
    
    # 显示初始状态
    print("初始状态:")
    status = manager.get_comprehensive_status()
    wellbeing = status["overall_wellbeing"]
    print(f"  整体健康: {wellbeing['overall_score']}/100 {wellbeing['emoji']} ({wellbeing['status']})")
    print(f"  饥饿程度: {status['physiological_state']['hunger_level']}/100")
    print(f"  尿布湿润: {status['physiological_state']['diaper_wetness']}/100")
    print(f"  睡眠债务: {status['physiological_state']['sleep_debt']}/100")
    print(f"  体温: {status['physiological_state']['body_temperature']:.1f}°C")
    print(f"  舒适度: {status['physiological_state']['comfort_level']}/100")
    print()
    
    # 模拟时间流逝
    print("⏰ 模拟2小时时间流逝...")
    await manager.simulate_time_passage(2.0)
    
    # 评估需求
    needs = await manager.assess_all_needs()
    print("当前需求评估:")
    for need_type, urgency in needs.items():
        print(f"  {need_type.value}: {urgency}/100")
    print()
    
    # 获取优先级需求
    priority_needs = await manager.get_priority_needs(30)
    print("优先级需求 (>30):")
    for need_type, urgency in priority_needs:
        print(f"  🚨 {need_type.value}: {urgency}/100")
    print()
    
    # 执行喂食
    if PhysiologicalNeedType.HUNGER in [need[0] for need in priority_needs]:
        print("执行喂食...")
        feeding_result = await manager.execute_care_action(
            PhysiologicalNeedType.HUNGER,
            {
                "feeding_type": FeedingType.FORMULA.value,
                "amount_ml": 120,
                "temperature": 36.5,
                "duration_minutes": 15
            }
        )
        print(f"  结果: {feeding_result['message']}")
        print(f"  效果: {feeding_result['effectiveness']:.1%}")
        print()
    
    # 最终状态
    final_status = manager.get_comprehensive_status()
    final_wellbeing = final_status["overall_wellbeing"]
    print("最终状态:")
    print(f"  整体健康: {final_wellbeing['overall_score']}/100 {final_wellbeing['emoji']} ({final_wellbeing['status']})")
    print()


if __name__ == "__main__":
    import asyncio
    asyncio.run(demo_physiological_needs())