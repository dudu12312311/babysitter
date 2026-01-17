#!/usr/bin/env python3
"""
育儿模拟器：硬核父母岗前特训
严格按照游戏设计文档实现的完整系统

游戏模式：
1. 简单模式：云养娃 (离线暂停，夜间保护)
2. 普通模式：实习父母 (离线缓慢衰减)
3. 困难模式：地狱特训 (真实时间同步，午夜凶铃)

孩子性格：
- 天使宝宝：负面事件30%，正面事件70%
- 高敏宝宝：负面事件70%，正面事件30%
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import random
import time
import json


class GameMode(Enum):
    """游戏模式"""
    EASY = "cloud_parenting"        # 云养娃
    NORMAL = "intern_parent"        # 实习父母
    HARD = "hell_week"             # 地狱特训


class BabyPersonality(Enum):
    """宝宝性格"""
    ANGEL = "chill_angel"          # 天使宝宝
    FUSSY = "fussy_crybaby"        # 高敏宝宝


class AgeStage(Enum):
    """年龄阶段"""
    NEWBORN_0_3 = "0-3months"      # 0-3月：除了吃就是睡
    INFANT_3_12 = "3-12months"     # 3-12月：解锁翻身与互动
    TODDLER_1_2 = "1-2years"       # 1-2岁：破坏王与学语期
    PRESCHOOL_2_3 = "2-3years"     # 2-3岁：自我意识觉醒


class TaskType(Enum):
    """任务类型"""
    # 0-3月任务
    FEEDING_HUNGRY = "feeding_hungry"           # 哭(饿) - 喂奶
    SLEEP_TIRED = "sleep_tired"                 # 哭(困) - 哄睡
    DIAPER_DIRTY = "diaper_dirty"               # 哭(脏) - 换尿布
    MEDICINE_SICK = "medicine_sick"             # 哭(病) - 选药
    HUG_HAPPY = "hug_happy"                     # 笑 - 拥抱
    
    # 3-12月任务
    TALK_PLAY = "talk_play"                     # 笑(玩) - 叽里咕噜
    FOOD_HUNGRY = "food_hungry"                 # 哭(饿) - 做辅食
    SAFETY_DANGER = "safety_danger"             # 险(动) - 翻身/站立
    FIRST_WORD = "first_word"                   # 笑(彩蛋) - 叫爹妈
    
    # 1-2岁任务
    DANGER_TOUCH = "danger_touch"               # 玩(危) - 触摸禁区
    TOY_CONFLICT = "toy_conflict"               # 哭(闹) - 玩具断案
    BAD_WORD = "bad_word"                       # 学说话 - 乱讲
    
    # 2-3岁任务
    DRESSING_WILD = "dressing_wild"             # 哭(野) - 出门
    EMOTION_TALK = "emotion_talk"               # 笑(通) - 完整表达


@dataclass
class GameState:
    """游戏状态"""
    # 基础状态
    mode: GameMode = GameMode.NORMAL
    baby_age_months: int = 0
    baby_personality: BabyPersonality = BabyPersonality.ANGEL
    
    # 数值状态 (0-100)
    health: int = 100              # 健康值
    hunger: int = 0                # 饥饿度 (0=饱, 100=饿)
    cleanliness: int = 100         # 清洁度
    happiness: int = 100           # 快乐度
    intimacy: int = 50             # 亲密度
    
    # 发展属性
    social_ability: int = 0        # 社交能力
    language_ability: int = 0      # 语言能力
    confidence: int = 50           # 自信心
    imagination: int = 50          # 想象力
    rationality: int = 50          # 理性
    
    # 父母状态
    parent_stress: int = 0         # 父母压力值
    parent_anxiety: int = 0        # 父母焦虑值
    
    # 游戏机制
    is_sleeping: bool = False      # 是否在睡觉
    sleep_end_time: Optional[datetime] = None  # 睡眠结束时间
    last_update: datetime = field(default_factory=datetime.now)
    
    # 困难模式专属
    hell_week_day: int = 0         # 地狱特训第几天
    phantom_cry_active: bool = False  # 幻听系统是否激活


@dataclass
class TaskResult:
    """任务执行结果"""
    success: bool
    message: str
    state_changes: Dict[str, int]
    special_effects: List[str] = field(default_factory=list)
    unlock_achievements: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


class HardcoreParentingGame:
    """硬核育儿模拟器主类"""
    
    def __init__(self):
        self.state = GameState()
        self.task_history: List[TaskResult] = []
        self.achievements: List[str] = []
        
        # 事件权重配置
        self.event_weights = {
            BabyPersonality.ANGEL: {
                "negative": 0.3,  # 负面事件30%
                "positive": 0.7   # 正面事件70%
            },
            BabyPersonality.FUSSY: {
                "negative": 0.7,  # 负面事件70%
                "positive": 0.3   # 正面事件30%
            }
        }
        
        # 模式配置
        self.mode_configs = {
            GameMode.EASY: {
                "decay_rate": 0.5,      # 数值衰减速度50%
                "offline_pause": True,   # 离线暂停
                "night_protection": True # 夜间保护
            },
            GameMode.NORMAL: {
                "decay_rate": 1.0,      # 正常衰减速度
                "offline_pause": False,  # 离线缓慢衰减
                "night_protection": False
            },
            GameMode.HARD: {
                "decay_rate": 1.5,      # 加速衰减
                "offline_pause": False,
                "night_protection": False,
                "real_time_sync": True,  # 真实时间同步
                "midnight_alarm": True,  # 午夜凶铃
                "phantom_cries": True    # 幻听系统
            }
        }
    
    def start_game(self, mode: GameMode, baby_personality: BabyPersonality, 
                   age_months: int = 0) -> Dict[str, Any]:
        """开始游戏"""
        self.state.mode = mode
        self.state.baby_personality = baby_personality
        self.state.baby_age_months = age_months
        self.state.last_update = datetime.now()
        
        if mode == GameMode.HARD:
            self.state.hell_week_day = 1
            
        return {
            "message": f"开始{mode.value}模式，宝宝{age_months}个月，性格：{baby_personality.value}",
            "initial_state": self._get_state_dict()
        }
    
    def _get_current_age_stage(self) -> AgeStage:
        """获取当前年龄阶段"""
        age = self.state.baby_age_months
        if age <= 3:
            return AgeStage.NEWBORN_0_3
        elif age <= 12:
            return AgeStage.INFANT_3_12
        elif age <= 24:
            return AgeStage.TODDLER_1_2
        else:
            return AgeStage.PRESCHOOL_2_3
    
    def _update_passive_decay(self):
        """更新被动数值衰减"""
        now = datetime.now()
        time_diff = (now - self.state.last_update).total_seconds() / 3600  # 小时
        
        # 检查夜间保护
        if (self.state.mode == GameMode.EASY and 
            self.mode_configs[GameMode.EASY]["night_protection"]):
            current_hour = now.hour
            if 22 <= current_hour or current_hour <= 8:
                # 夜间保护时间，不衰减
                return
        
        # 检查离线暂停
        if (self.state.mode == GameMode.EASY and 
            self.mode_configs[GameMode.EASY]["offline_pause"]):
            # 简单模式离线暂停，这里假设在线
            pass
        
        # 计算衰减
        decay_rate = self.mode_configs[self.state.mode]["decay_rate"]
        base_decay = time_diff * decay_rate
        
        # 饥饿度增加
        hunger_increase = int(base_decay * 10)  # 每小时增加10点
        self.state.hunger = min(100, self.state.hunger + hunger_increase)
        
        # 清洁度下降
        clean_decrease = int(base_decay * 5)   # 每小时下降5点
        self.state.cleanliness = max(0, self.state.cleanliness - clean_decrease)
        
        # 快乐度缓慢下降
        happy_decrease = int(base_decay * 3)   # 每小时下降3点
        self.state.happiness = max(0, self.state.happiness - happy_decrease)
        
        self.state.last_update = now
    
    # ==================== 0-3月任务实现 ====================
    
    def execute_feeding_task(self, water_temp: float, shake_intensity: int, 
                           tilt_angle: int) -> TaskResult:
        """冲奶粉小游戏：调节水温 -> 摇晃混匀 -> 倾斜喂奶"""
        
        success = True
        message = ""
        state_changes = {}
        special_effects = []
        
        # 1. 水温检查
        if water_temp > 45:
            success = False
            message = "💥 水温过高！孩子猛地吐奶，健康值-5，哭声升级！"
            state_changes["health"] = -5
            state_changes["hunger"] = +10  # 吐奶后更饿
            special_effects.append("吐奶动画")
            special_effects.append("哭声升级")
            
        elif water_temp < 37:
            success = False
            message = "❄️ 水温过低！孩子拒食，继续哭闹"
            state_changes["happiness"] = -10
            special_effects.append("拒食动画")
            
        elif 39 <= water_temp <= 41:
            # 完美温度
            message = "🍼 完美温度！"
            state_changes["hunger"] = -80  # 大幅减少饥饿
            state_changes["happiness"] = +20
            special_effects.append("咕咚咕咚喝奶音效")
            
        else:
            # 可接受温度
            message = "🍼 温度还行，宝宝喝了一些"
            state_changes["hunger"] = -50
            state_changes["happiness"] = +10
        
        # 2. 摇晃强度检查
        if shake_intensity > 8:
            success = False
            message += "\n⚠️ 摇晃过猛！可能影响奶粉质量"
            state_changes["health"] = state_changes.get("health", 0) - 3
            
        elif shake_intensity < 3:
            message += "\n🥛 摇晃不够，奶粉没完全溶解"
            state_changes["hunger"] = int(state_changes.get("hunger", 0) * 0.8)
        
        # 3. 倾斜角度检查
        if not (30 <= tilt_angle <= 60):
            message += "\n📐 喂奶角度不当，容易呛到"
            state_changes["health"] = state_changes.get("health", 0) - 2
        
        # 应用状态变化
        self._apply_state_changes(state_changes)
        
        return TaskResult(
            success=success,
            message=message,
            state_changes=state_changes,
            special_effects=special_effects
        )
    
    def execute_sleep_task(self, shake_frequency: float, duration: int, 
                          app_switched: bool) -> TaskResult:
        """摇晃抱哄：利用陀螺仪保持特定频率摇晃60秒"""
        
        success = True
        message = ""
        state_changes = {}
        special_effects = ["视野模糊效果", "安抚进度条"]
        
        # 检查是否中途切出App
        if app_switched:
            success = False
            message = "📱 中途切出App！孩子惊醒，进度条归零，需重来"
            state_changes["happiness"] = -15
            state_changes["parent_stress"] = +20
            special_effects.append("惊醒动画")
            special_effects.append("进度条归零")
            
        # 检查摇晃频率 (理想频率: 1.5-2.5 Hz)
        elif shake_frequency > 3.0:
            success = False
            message = "🚨 摇晃过猛！触发脑震荡警告，扣除大量健康值"
            state_changes["health"] = -25
            state_changes["parent_stress"] = +30
            special_effects.append("脑震荡警告")
            special_effects.append("健康值暴跌动画")
            
        elif shake_frequency < 1.0:
            success = False
            message = "😴 摇晃太轻，没有安抚效果"
            state_changes["happiness"] = -5
            
        # 检查持续时间
        elif duration < 45:
            success = False
            message = "⏱️ 时间太短，宝宝还没完全安静下来"
            state_changes["happiness"] = +5  # 稍有改善
            
        else:
            # 成功哄睡
            success = True
            message = "😴 哄睡成功！宝宝进入睡眠状态，获得2小时免打扰时间"
            state_changes["happiness"] = +30
            state_changes["health"] = +10
            
            # 设置睡眠状态
            self.state.is_sleeping = True
            self.state.sleep_end_time = datetime.now() + timedelta(hours=2)
            
            special_effects.append("睡眠动画")
            special_effects.append("2小时免打扰提示")
        
        self._apply_state_changes(state_changes)
        
        return TaskResult(
            success=success,
            message=message,
            state_changes=state_changes,
            special_effects=special_effects
        )
    
    def execute_diaper_task(self, lift_speed: float, wipe_thoroughness: int, 
                           diaper_placement: str) -> TaskResult:
        """换尿布：上滑提腿 -> 点击擦拭 -> 拖拽新尿布"""
        
        success = True
        message = ""
        state_changes = {}
        special_effects = ["绿色毒气特效"]
        
        # 检查动作速度
        if lift_speed > 5.0:  # 动作太慢
            # 触发喷射袭击！
            if random.random() < 0.3:  # 30%概率
                success = False
                message = "💩 手慢了！触发喷射袭击事件，屏幕被糊满！"
                state_changes["cleanliness"] = +25  # 只恢复50%
                state_changes["parent_stress"] = +25
                special_effects.append("喷射袭击动画")
                special_effects.append("屏幕糊满效果")
                special_effects.append("需要擦拭屏幕")
            else:
                message = "😅 动作有点慢，但还好没出意外"
                state_changes["cleanliness"] = +40
        
        # 检查擦拭彻底程度
        if wipe_thoroughness < 5:
            message += "\n🧻 擦拭不够彻底"
            state_changes["cleanliness"] = state_changes.get("cleanliness", 50) - 10
            
        elif wipe_thoroughness > 9:
            message += "\n✨ 擦拭得很干净"
            state_changes["cleanliness"] = state_changes.get("cleanliness", 50) + 10
        
        # 检查尿布放置
        if diaper_placement == "wrong_order":  # 没擦就穿
            success = False
            message += "\n🔴 顺序错误！没擦就穿新尿布，触发尿布疹"
            state_changes["health"] = -15
            state_changes["cleanliness"] = +20  # 清洁度恢复有限
            special_effects.append("尿布疹警告")
            special_effects.append("进入生病流程")
            
        elif diaper_placement == "correct":
            if "cleanliness" not in state_changes:
                state_changes["cleanliness"] = +50
            state_changes["happiness"] = +15
            message = "✅ 换尿布成功！宝宝感觉清爽多了" if not message else message
        
        # 红屁股进度条检查
        if lift_speed > 4.0 or wipe_thoroughness < 6:
            special_effects.append("红屁股进度条警告")
        
        self._apply_state_changes(state_changes)
        
        return TaskResult(
            success=success,
            message=message,
            state_changes=state_changes,
            special_effects=special_effects
        )
    
    def execute_medicine_task(self, medicine_choice: str) -> TaskResult:
        """选药任务：观察症状，从药箱三选一"""
        
        # 症状：满脸通红，体温38.5℃ (发烧)
        correct_medicine = "fever_patch"  # 退烧贴
        
        success = False
        message = ""
        state_changes = {}
        special_effects = ["体温计显示38.5℃", "满脸通红特效"]
        
        if medicine_choice == "fever_patch":
            # 正确选择
            success = True
            message = "🩹 选择正确！退烧贴贴在额头，体温缓慢下降，健康恢复"
            state_changes["health"] = +20
            state_changes["happiness"] = +15
            special_effects.append("蓝色退烧贴出现")
            special_effects.append("体温下降动画")
            
        elif medicine_choice == "antibiotic":
            # 错误选择 - 滥用抗生素
            success = False
            message = "⚠️ 滥用药物！抗生素不能随便用，健康值-20，产生抗药性"
            state_changes["health"] = -20
            state_changes["parent_stress"] = +15
            special_effects.append("滥用药物警告")
            special_effects.append("抗药性Buff")
            
        elif medicine_choice == "hot_water":
            # 无效选择
            success = False
            message = "🔥 太烫了！热水不能直接给发烧的宝宝，哭声变大"
            state_changes["happiness"] = -10
            state_changes["health"] = -5
            special_effects.append("哭声变大")
            
        self._apply_state_changes(state_changes)
        
        return TaskResult(
            success=success,
            message=message,
            state_changes=state_changes,
            special_effects=special_effects
        )
    
    def execute_hug_task(self, press_duration: float) -> TaskResult:
        """拥抱任务：长按屏幕，手机震动模拟心跳"""
        
        success = press_duration >= 3.0
        message = ""
        state_changes = {}
        special_effects = ["粉色柔光", "心跳震动"]
        
        if success:
            message = "🤗 长按成功！孩子发出咯咯笑声，亲密度大幅提升"
            state_changes["intimacy"] = +25
            state_changes["happiness"] = +20
            special_effects.append("咯咯笑声")
            special_effects.append("亲密度提升动画")
        else:
            message = f"🤏 按压时间太短({press_duration:.1f}秒)，需要长按3秒以上"
            state_changes["happiness"] = +5  # 稍有改善
        
        self._apply_state_changes(state_changes)
        
        return TaskResult(
            success=success,
            message=message,
            state_changes=state_changes,
            special_effects=special_effects
        )
    
    # ==================== 3-12月任务实现 ====================
    
    def execute_talk_task(self, speech_keywords: List[str], voice_duration: float) -> TaskResult:
        """叽里咕噜对话：玩家说话，系统幼态化回放"""
        
        success = True
        message = ""
        state_changes = {}
        special_effects = ["声波纹路", "不懂符号气泡"]
        
        # 检查关键词
        baby_keywords = ["乖", "宝宝", "妈妈", "爸爸", "好棒", "可爱"]
        matched_keywords = [kw for kw in speech_keywords if kw in baby_keywords]
        
        if matched_keywords:
            # 宝宝尝试模仿
            imitated_word = random.choice(matched_keywords)
            message = f"👶 宝宝试图模仿说'{imitated_word}'，发出了'{imitated_word[0]}uai~'的可爱声音"
            state_changes["language_ability"] = +10
            state_changes["intimacy"] = +15
            state_changes["happiness"] = +20
            special_effects.append(f"模仿发音：{imitated_word[0]}uai~")
        else:
            message = "👶 宝宝咿呀学语地回应，但没有明确的模仿"
            state_changes["language_ability"] = +5
            state_changes["happiness"] = +10
        
        # 检查说话时长
        if voice_duration < 10:
            message += "\n⏱️ 说话时间太短，宝宝还想听更多"
            state_changes["happiness"] = state_changes.get("happiness", 0) - 5
        elif voice_duration > 60:
            message += "\n😴 说话时间太长，宝宝有点累了"
            state_changes["happiness"] = state_changes.get("happiness", 0) - 3
        
        self._apply_state_changes(state_changes)
        
        return TaskResult(
            success=success,
            message=message,
            state_changes=state_changes,
            special_effects=special_effects
        )
    
    def execute_food_task(self, food_choice: str, cutting_skill: int) -> TaskResult:
        """做辅食：选择食材 -> 切碎 -> 喂入嘴里"""
        
        success = True
        message = ""
        state_changes = {}
        special_effects = ["满脸期待的婴儿"]
        
        # 食材选择检查
        if food_choice == "pumpkin":
            # 安全选择
            message = "🎃 选择南瓜！孩子大口吃，心情+10"
            state_changes["hunger"] = -60
            state_changes["happiness"] = +10
            state_changes["health"] = +5
            special_effects.append("大口吃动画")
            
        elif food_choice == "carrot":
            # 高敏宝宝陷阱
            if self.state.baby_personality == BabyPersonality.FUSSY:
                success = False
                message = "🥕 高敏宝宝对胡萝卜过敏！直接吐在屏幕上"
                state_changes["hunger"] = +10  # 更饿了
                state_changes["happiness"] = -20
                state_changes["health"] = -10
                special_effects.append("吐在屏幕上")
                special_effects.append("需要手动擦拭屏幕")
            else:
                message = "🥕 胡萝卜还不错，宝宝慢慢吃完了"
                state_changes["hunger"] = -40
                state_changes["happiness"] = +5
                
        elif food_choice == "chili":
            # 作死选择
            success = False
            message = "🌶️ 选择辣椒！孩子脸涨红大哭，健康值骤降，触发极度愤怒状态"
            state_changes["health"] = -30
            state_changes["happiness"] = -40
            state_changes["parent_stress"] = +25
            special_effects.append("脸涨红动画")
            special_effects.append("极度愤怒状态")
            special_effects.append("大哭音效")
        
        # 切菜技巧检查
        if cutting_skill < 5:
            message += "\n🔪 切得太粗糙，宝宝有噎到风险"
            state_changes["health"] = state_changes.get("health", 0) - 5
            special_effects.append("噎到风险警告")
        elif cutting_skill > 8:
            message += "\n✨ 切得很精细，宝宝吃得很开心"
            state_changes["happiness"] = state_changes.get("happiness", 0) + 5
        
        self._apply_state_changes(state_changes)
        
        return TaskResult(
            success=success,
            message=message,
            state_changes=state_changes,
            special_effects=special_effects
        )
    
    def execute_safety_task(self, reaction_time: float, button_clicked: bool) -> TaskResult:
        """防摔倒QTE：2秒内点击"扶住"按钮"""
        
        success = button_clicked and reaction_time <= 2.0
        message = ""
        state_changes = {}
        special_effects = ["红光警报", "慢动作效果", "孩子倾斜"]
        
        if success:
            message = f"🛡️ 反应神速！在{reaction_time:.1f}秒内成功扶住孩子"
            state_changes["health"] = +5
            state_changes["happiness"] = +10
            special_effects.append("大手扶住动画")
            special_effects.append("好险！文案")
        else:
            if not button_clicked:
                message = "💥 没有点击扶住！听到'咚'的一声，孩子大哭"
            else:
                message = f"😰 反应太慢({reaction_time:.1f}秒)！来不及扶住"
            
            state_changes["health"] = -15
            state_changes["happiness"] = -25
            state_changes["parent_stress"] = +20
            special_effects.append("摔倒音效：咚")
            special_effects.append("头部出现包")
            special_effects.append("需要冷敷")
            special_effects.append("大哭动画")
        
        self._apply_state_changes(state_changes)
        
        return TaskResult(
            success=success,
            message=message,
            state_changes=state_changes,
            special_effects=special_effects
        )
    
    def execute_first_word_task(self, recorded: bool, reaction_time: float) -> TaskResult:
        """叫爹妈彩蛋：语音识别，需立刻点击录制"""
        
        # 随机选择第一个词
        first_words = ["Ma", "Ba", "Mama", "Baba"]
        word = random.choice(first_words)
        
        success = recorded and reaction_time <= 3.0
        message = ""
        state_changes = {}
        special_effects = ["满屏烟花", "录制按钮"]
        
        if success:
            message = f"🎉 珍贵时刻！宝宝说出了'{word}'，成功录制保存到收藏夹"
            state_changes["language_ability"] = +20
            state_changes["intimacy"] = +30
            state_changes["happiness"] = +25
            special_effects.append("音频保存动画")
            
            # 解锁成就
            achievement = "初次发声"
            if achievement not in self.achievements:
                self.achievements.append(achievement)
                special_effects.append(f"解锁成就：{achievement}")
        else:
            message = f"😢 错过了！宝宝说了'{word}'但没有录制，珍贵时刻无法补救"
            state_changes["language_ability"] = +5  # 仍有少量提升
            special_effects.append("错过提示")
            special_effects.append("无法补救警告")
        
        self._apply_state_changes(state_changes)
        
        return TaskResult(
            success=success,
            message=message,
            state_changes=state_changes,
            special_effects=special_effects,
            unlock_achievements=[achievement] if success else []
        )
    
    # ==================== 1-2岁任务实现 ====================
    
    def execute_danger_touch_task(self, swipe_direction: str, danger_type: str) -> TaskResult:
        """触摸禁区：手伸向插座/水壶，滑动拨开"""
        
        # 孩子手的运动方向是向前的，正确的滑动应该是相反方向
        correct_direction = "away"  # 远离危险
        success = swipe_direction == correct_direction
        
        message = ""
        state_changes = {}
        special_effects = ["危险角落背景", "孩子的手光标"]
        
        if success:
            message = f"🛡️ 成功阻止！及时拦住了孩子伸向{danger_type}的手"
            state_changes["health"] = +5
            state_changes["happiness"] = +10  # 避免了危险，心情好
            special_effects.append("成功阻止动画")
        else:
            if swipe_direction == "same":
                # 顺着滑动，加速触碰
                message = f"💥 滑动方向错误！加速了孩子触碰{danger_type}，造成严重伤害"
                state_changes["health"] = -25
                state_changes["happiness"] = -30
            else:
                message = f"😰 阻止失败！孩子触碰了{danger_type}"
                state_changes["health"] = -15
                state_changes["happiness"] = -20
            
            state_changes["parent_stress"] = +30
            special_effects.append("触碰危险物品")
            special_effects.append("受伤动画")
        
        self._apply_state_changes(state_changes)
        
        return TaskResult(
            success=success,
            message=message,
            state_changes=state_changes,
            special_effects=special_effects
        )
    
    def execute_toy_conflict_task(self, solution_choice: str) -> TaskResult:
        """玩具断案：狗叼走兔子玩偶，孩子大哭"""
        
        success = True
        message = ""
        state_changes = {}
        special_effects = ["左右分屏", "哭闹娃", "委屈狗"]
        
        if solution_choice == "A":
            # 训斥狗狗，抢回玩具
            message = "😤 训斥狗狗把兔子抢回来！孩子破涕为笑，但学会了霸道"
            state_changes["happiness"] = +20
            state_changes["social_ability"] = -10  # 同理心下降
            special_effects.append("破涕为笑")
            special_effects.append("霸道性格标记")
            
        elif solution_choice == "B":
            # 引导分享
            if self.state.baby_personality == BabyPersonality.ANGEL:
                # 天使宝宝成功
                message = "🌟 引导分享成功！孩子学会了分享，社交能力+20"
                state_changes["happiness"] = +15
                state_changes["social_ability"] = +20
                special_effects.append("分享成功动画")
            else:
                # 高敏宝宝失败
                success = False
                message = "😭 高敏宝宝无法理解分享，哭闹升级"
                state_changes["happiness"] = -15
                special_effects.append("哭闹升级")
                
        elif solution_choice == "C":
            # 各打五十大板
            message = "😐 没收玩具！哭声停止，但孩子生闷气，亲密度-20"
            state_changes["happiness"] = +5  # 不哭了
            state_changes["intimacy"] = -20
            special_effects.append("生闷气状态")
            special_effects.append("10分钟拒绝互动")
        
        self._apply_state_changes(state_changes)
        
        return TaskResult(
            success=success,
            message=message,
            state_changes=state_changes,
            special_effects=special_effects
        )
    
    def execute_bad_word_task(self, correction_method: str, bad_word: str) -> TaskResult:
        """词汇纠正：孩子说脏话"""
        
        success = True
        message = ""
        state_changes = {}
        special_effects = ["头顶冒出[*#$]气泡"]
        
        if correction_method == "A":
            # 严厉制止
            message = f"😰 严厉制止'{bad_word}'！孩子被吓哭，压力值+20，性格趋向胆小"
            state_changes["happiness"] = -20
            state_changes["parent_stress"] = +20
            state_changes["confidence"] = -10  # 胆小
            special_effects.append("被吓哭动画")
            special_effects.append("胆小性格标记")
            
        elif correction_method == "B":
            # 温和替换 (最佳选择)
            replacement = "哇塞" if bad_word == "卧槽" else "哎呀"
            message = f"🌟 温和替换成功！孩子改口说'{replacement}'，语言能力+15"
            state_changes["language_ability"] = +15
            state_changes["happiness"] = +10
            state_changes["intimacy"] = +10
            special_effects.append("改口动画")
            special_effects.append("最佳教育方式标记")
            
        elif correction_method == "C":
            # 大笑并模仿 (最坏选择)
            success = False
            message = f"😅 大笑并模仿！孩子觉得好玩，记住了'{bad_word}'，以后会频繁爆粗口"
            state_changes["language_ability"] = -10  # 学坏了
            state_changes["happiness"] = +15  # 觉得好玩
            special_effects.append("记住脏话标记")
            special_effects.append("无法撤销警告")
            special_effects.append("未来随机爆粗口")
        
        self._apply_state_changes(state_changes)
        
        return TaskResult(
            success=success,
            message=message,
            state_changes=state_changes,
            special_effects=special_effects
        )
    
    # ==================== 2-3岁任务实现 ====================
    
    def execute_dressing_task(self, completion_time: int, time_limit: int) -> TaskResult:
        """出门穿衣：限时拖拽游戏"""
        
        success = completion_time <= time_limit
        message = ""
        state_changes = {}
        special_effects = ["散落的衣物", "孩子乱跑干扰"]
        
        if success:
            if completion_time <= time_limit * 0.8:
                # 提前完成
                message = f"⚡ 效率很高！{completion_time}秒完成穿衣，可以按时出门去公园"
                state_changes["happiness"] = +25
                state_changes["confidence"] = +15
                special_effects.append("按时出门")
                special_effects.append("去公园")
            else:
                message = f"✅ 穿衣完成！用时{completion_time}秒，刚好赶上出门时间"
                state_changes["happiness"] = +15
                state_changes["confidence"] = +10
        else:
            # 超时失败
            message = f"⏰ 超时了！{completion_time}秒超过限制{time_limit}秒，孩子把衣服扔地上拒绝出门"
            state_changes["happiness"] = -25
            state_changes["confidence"] = -15
            state_changes["parent_stress"] = +20
            special_effects.append("衣服扔地上")
            special_effects.append("拒绝出门")
            special_effects.append("原定行程取消")
            special_effects.append("心情值大跌")
        
        self._apply_state_changes(state_changes)
        
        return TaskResult(
            success=success,
            message=message,
            state_changes=state_changes,
            special_effects=special_effects
        )
    
    def execute_emotion_talk_task(self, response_choice: str) -> TaskResult:
        """情感对话：孩子表达复杂情感"""
        
        # 孩子的话："妈妈，我梦见怪兽吃掉了月亮，我好怕。"
        success = True
        message = ""
        state_changes = {}
        special_effects = ["大头视角特写", "电影式字幕"]
        
        if response_choice == "A":
            # 共情路线 (自信路线)
            message = "🦸 共情回应：'别怕，我们变身超人去救月亮！'孩子眼神发光，自信+10，亲密度+20"
            state_changes["confidence"] = +10
            state_changes["intimacy"] = +20
            state_changes["imagination"] = +15
            state_changes["happiness"] = +20
            special_effects.append("眼神发光")
            special_effects.append("自信路线标记")
            
        elif response_choice == "B":
            # 讲理路线 (理性路线)
            message = "🤔 理性回应：'世界上没有怪兽，那是假的。'孩子若有所思，理性+10，但想象力-10"
            state_changes["rationality"] = +10
            state_changes["imagination"] = -10
            state_changes["happiness"] = +5
            special_effects.append("若有所思")
            special_effects.append("理性路线标记")
            
        elif response_choice == "C":
            # 敷衍路线 (冷漠路线)
            success = False
            message = "😔 敷衍回应：'梦是反的，快睡觉。'孩子失望转头，内向+10，亲密度-10"
            state_changes["confidence"] = -10  # 变内向
            state_changes["intimacy"] = -10
            state_changes["happiness"] = -15
            special_effects.append("失望转头")
            special_effects.append("冷漠路线标记")
        
        self._apply_state_changes(state_changes)
        
        return TaskResult(
            success=success,
            message=message,
            state_changes=state_changes,
            special_effects=special_effects
        )
    
    # ==================== 困难模式专属机制 ====================
    
    def trigger_midnight_alarm(self) -> TaskResult:
        """午夜凶铃：凌晨3点强制事件"""
        
        current_time = datetime.now()
        if not (2 <= current_time.hour <= 4):
            return TaskResult(False, "不在午夜时间段", {})
        
        message = "🌙 午夜凶铃！凌晨3点，即使手机静音也收到最高优先级推送"
        state_changes = {"parent_stress": +25, "parent_anxiety": +20}
        special_effects = [
            "最高优先级推送",
            "屏幕重影效果",
            "全黑画面",
            "微弱声源定位",
            "需要找开关",
            "5分钟长时间安抚",
            "不允许切换App"
        ]
        
        self._apply_state_changes(state_changes)
        
        return TaskResult(
            success=True,
            message=message,
            state_changes=state_changes,
            special_effects=special_effects
        )
    
    def trigger_phantom_cry(self) -> TaskResult:
        """幻听系统：播放假哭声"""
        
        if not self.state.is_sleeping:
            return TaskResult(False, "孩子没在睡觉，不触发幻听", {})
        
        # 激活幻听
        self.state.phantom_cry_active = True
        
        message = "👻 幻听系统激活！播放极短暂假哭声，但监控画面显示孩子在睡觉"
        state_changes = {}
        special_effects = [
            "极短暂假哭声",
            "状态栏无异常",
            "监控画面显示睡觉",
            "心理博弈开始"
        ]
        
        return TaskResult(
            success=True,
            message=message,
            state_changes=state_changes,
            special_effects=special_effects
        )
    
    def check_phantom_cry_response(self, screen_checks: int) -> TaskResult:
        """检查幻听响应：频繁检查屏幕的后果"""
        
        if not self.state.phantom_cry_active:
            return TaskResult(False, "幻听系统未激活", {})
        
        message = ""
        state_changes = {}
        special_effects = []
        
        if screen_checks >= 5:
            # 频繁检查，增加焦虑
            message = "😰 频繁检查屏幕！父母焦虑值增加，操作开始手抖"
            state_changes["parent_anxiety"] = +30
            special_effects.append("UI按钮随机轻微位移")
            special_effects.append("操作手抖效果")
        elif screen_checks >= 3:
            message = "😟 有些焦虑，但还能控制"
            state_changes["parent_anxiety"] = +15
        else:
            message = "😌 保持冷静，没有被幻听影响"
            state_changes["parent_anxiety"] = -5
        
        self._apply_state_changes(state_changes)
        
        return TaskResult(
            success=screen_checks < 5,
            message=message,
            state_changes=state_changes,
            special_effects=special_effects
        )
    
    # ==================== 辅助方法 ====================
    
    def _apply_state_changes(self, changes: Dict[str, int]):
        """应用状态变化"""
        for attr, change in changes.items():
            if hasattr(self.state, attr):
                current_value = getattr(self.state, attr)
                new_value = max(0, min(100, current_value + change))
                setattr(self.state, attr, new_value)
    
    def _get_state_dict(self) -> Dict[str, Any]:
        """获取状态字典"""
        return {
            "mode": self.state.mode.value,
            "baby_age_months": self.state.baby_age_months,
            "baby_personality": self.state.baby_personality.value,
            "health": self.state.health,
            "hunger": self.state.hunger,
            "cleanliness": self.state.cleanliness,
            "happiness": self.state.happiness,
            "intimacy": self.state.intimacy,
            "social_ability": self.state.social_ability,
            "language_ability": self.state.language_ability,
            "confidence": self.state.confidence,
            "imagination": self.state.imagination,
            "rationality": self.state.rationality,
            "parent_stress": self.state.parent_stress,
            "parent_anxiety": self.state.parent_anxiety,
            "is_sleeping": self.state.is_sleeping,
            "hell_week_day": self.state.hell_week_day,
            "achievements": self.achievements
        }
    
    def get_available_tasks(self) -> List[TaskType]:
        """获取当前年龄阶段可用的任务"""
        age_stage = self._get_current_age_stage()
        
        task_mapping = {
            AgeStage.NEWBORN_0_3: [
                TaskType.FEEDING_HUNGRY,
                TaskType.SLEEP_TIRED,
                TaskType.DIAPER_DIRTY,
                TaskType.MEDICINE_SICK,
                TaskType.HUG_HAPPY
            ],
            AgeStage.INFANT_3_12: [
                TaskType.TALK_PLAY,
                TaskType.FOOD_HUNGRY,
                TaskType.SAFETY_DANGER,
                TaskType.FIRST_WORD
            ],
            AgeStage.TODDLER_1_2: [
                TaskType.DANGER_TOUCH,
                TaskType.TOY_CONFLICT,
                TaskType.BAD_WORD
            ],
            AgeStage.PRESCHOOL_2_3: [
                TaskType.DRESSING_WILD,
                TaskType.EMOTION_TALK
            ]
        }
        
        return task_mapping.get(age_stage, [])
    
    def get_random_event(self) -> Optional[TaskType]:
        """根据性格权重获取随机事件"""
        available_tasks = self.get_available_tasks()
        if not available_tasks:
            return None
        
        # 根据性格确定事件类型权重
        personality_weights = self.event_weights[self.state.baby_personality]
        
        # 定义正面和负面事件
        positive_events = [TaskType.HUG_HAPPY, TaskType.TALK_PLAY, TaskType.FIRST_WORD]
        negative_events = [
            TaskType.FEEDING_HUNGRY, TaskType.SLEEP_TIRED, TaskType.DIAPER_DIRTY,
            TaskType.MEDICINE_SICK, TaskType.FOOD_HUNGRY, TaskType.SAFETY_DANGER,
            TaskType.DANGER_TOUCH, TaskType.TOY_CONFLICT, TaskType.BAD_WORD,
            TaskType.DRESSING_WILD
        ]
        
        # 筛选当前可用的正面和负面事件
        available_positive = [t for t in available_tasks if t in positive_events]
        available_negative = [t for t in available_tasks if t in negative_events]
        
        # 根据权重随机选择
        if random.random() < personality_weights["negative"] and available_negative:
            return random.choice(available_negative)
        elif available_positive:
            return random.choice(available_positive)
        else:
            return random.choice(available_tasks) if available_tasks else None
    
    def get_game_status(self) -> Dict[str, Any]:
        """获取完整游戏状态"""
        self._update_passive_decay()
        
        return {
            "game_state": self._get_state_dict(),
            "available_tasks": [task.value for task in self.get_available_tasks()],
            "current_age_stage": self._get_current_age_stage().value,
            "task_history_count": len(self.task_history),
            "achievements_count": len(self.achievements),
            "mode_config": self.mode_configs[self.state.mode]
        }

# ==================== Web 服务器入口 ====================

def create_web_app():
    """创建简单的 Web 应用"""
    try:
        from flask import Flask, jsonify, request
        app = Flask(__name__)
        game = HardcoreParentingGame()
        
        @app.route('/')
        def home():
            return jsonify({
                "message": "硬核育儿模拟器 API",
                "version": "1.0.0",
                "endpoints": [
                    "/start - 开始游戏",
                    "/status - 获取状态",
                    "/tasks - 获取可用任务"
                ]
            })
        
        @app.route('/start', methods=['POST'])
        def start_game():
            data = request.get_json() or {}
            mode = GameMode(data.get('mode', 'intern_parent'))
            personality = BabyPersonality(data.get('personality', 'chill_angel'))
            age = data.get('age', 0)
            
            result = game.start_game(mode, personality, age)
            return jsonify(result)
        
        @app.route('/status')
        def get_status():
            return jsonify(game.get_game_status())
        
        @app.route('/tasks')
        def get_tasks():
            tasks = game.get_available_tasks()
            return jsonify([task.value for task in tasks])
        
        return app
    except ImportError:
        # 如果没有 Flask，返回简单的控制台版本
        return None

def run_console_demo():
    """运行控制台演示"""
    print("🍼 硬核育儿模拟器启动！")
    game = HardcoreParentingGame()
    
    # 开始游戏
    result = game.start_game(GameMode.NORMAL, BabyPersonality.ANGEL, 0)
    print(f"游戏开始：{result['message']}")
    
    # 显示状态
    status = game.get_game_status()
    print(f"当前状态：健康{status['game_state']['health']}, 快乐{status['game_state']['happiness']}")
    
    # 显示可用任务
    tasks = game.get_available_tasks()
    print(f"可用任务：{[task.value for task in tasks]}")
    
    print("游戏演示完成！")

if __name__ == "__main__":
    import os
    
    # 检查是否在 Railway 环境
    port = int(os.environ.get("PORT", 5000))
    
    # 尝试创建 Web 应用
    app = create_web_app()
    
    if app:
        print(f"🚀 启动 Web 服务器，端口：{port}")
        app.run(host="0.0.0.0", port=port)
    else:
        print("📱 Flask 未安装，运行控制台演示")
        run_console_demo()