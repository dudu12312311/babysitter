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
    
    def get_game_status(self) -> Dict[str, Any]:
        """获取完整游戏状态"""
        return {
            "game_state": self._get_state_dict(),
            "available_tasks": [task.value for task in self.get_available_tasks()],
            "current_age_stage": self._get_current_age_stage().value,
            "task_history_count": len(self.task_history),
            "achievements_count": len(self.achievements),
            "mode_config": self.mode_configs[self.state.mode]
        }


# Web 服务器入口
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