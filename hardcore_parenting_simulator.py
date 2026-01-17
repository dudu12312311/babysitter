"""
育儿模拟器：硬核父母岗前特训 - 核心任务接口
Hardcore Parenting Simulator: Pre-Combat Training - Core Task Interface

这是一个游戏化的育儿训练系统，通过模拟真实育儿场景来训练准父母。
采用黑色幽默风格，提供三种难度模式和多人协作功能。
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime, timedelta
import random
import asyncio
import json


class GameMode(Enum):
    """游戏模式枚举"""
    EASY = "cloud_parenting"      # 云养娃
    NORMAL = "intern_parent"      # 实习父母  
    HARD = "hell_week"           # 地狱特训


class EventType(Enum):
    """游戏事件类型"""
    CRYING = "crying"
    DIAPER_CHANGE = "diaper_change"
    FEEDING = "feeding"
    SLEEP_DISRUPTION = "sleep_disruption"
    COLIC_ATTACK = "colic_attack"
    EXPLOSIVE_DIAPER = "explosive_diaper"
    MIDNIGHT_TERROR = "midnight_terror"
    # 新增特色任务
    STROLLER_TETRIS = "stroller_tetris"
    PICKY_EATER_NEGOTIATION = "picky_eater_negotiation"


class ActionType(Enum):
    """玩家行动类型"""
    COMFORT = "comfort"
    FEED = "feed"
    CHANGE_DIAPER = "change_diaper"
    ROCK_TO_SLEEP = "rock_to_sleep"
    CHECK_TEMPERATURE = "check_temperature"
    APPLY_CREAM = "apply_cream"
    # 俄罗斯方块相关
    ROTATE_ITEM = "rotate_item"
    PLACE_ITEM = "place_item"
    DISASSEMBLE = "disassemble"
    # 谈判相关
    PLAY_CARD = "play_card"
    NEGOTIATE = "negotiate"
    DISTRACT = "distract"


@dataclass
class GameState:
    """核心游戏状态"""
    comfort: int = 100          # 宝宝舒适度 (0-100)
    sanity: int = 100          # 父母理智值 (0-100)
    parenting_kpi: int = 100   # 育儿KPI (0-100)
    baby_stage: int = 0        # 婴儿成长阶段
    active_events: List[str] = field(default_factory=list)
    last_update: datetime = field(default_factory=datetime.now)
    game_mode: GameMode = GameMode.NORMAL
    session_duration: timedelta = field(default_factory=lambda: timedelta(hours=24))


@dataclass 
class GameEvent:
    """游戏事件数据结构"""
    id: str
    event_type: EventType
    severity: int              # 严重程度 (1-10)
    duration: int             # 持续时间(秒)
    required_actions: List[ActionType]
    description: str
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True


@dataclass
class PlayerAction:
    """玩家行动记录"""
    action_type: ActionType
    response_time: float      # 响应时间(秒)
    success: bool
    player_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    # 扩展数据，用于复杂任务
    extra_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TetrisItem:
    """俄罗斯方块物品"""
    name: str
    shape: List[List[int]]    # 2D形状矩阵
    rotation: int = 0         # 旋转角度 (0, 90, 180, 270)
    is_disassembled: bool = False
    priority: int = 1         # 优先级，1-5


@dataclass
class NegotiationCard:
    """谈判卡牌"""
    name: str
    card_type: str           # "strategy", "distraction", "bribe", "threat"
    effectiveness: int       # 有效性 1-10
    side_effects: Dict[str, int] = field(default_factory=dict)  # 副作用
    description: str = ""

class TaskInterface(ABC):
    """任务接口抽象基类"""
    
    @abstractmethod
    async def execute(self, game_state: GameState, player_action: Optional[PlayerAction] = None) -> GameState:
        """执行任务并返回更新后的游戏状态"""
        pass
    
    @abstractmethod
    def validate_action(self, action: PlayerAction, game_state: GameState) -> bool:
        """验证玩家行动是否有效"""
        pass
    
    @abstractmethod
    def calculate_score_impact(self, action: PlayerAction, game_state: GameState) -> Dict[str, int]:
        """计算行动对各项数值的影响"""
        pass


class GameEventManager:
    """游戏事件管理器"""
    
    def __init__(self):
        self.active_events: Dict[str, GameEvent] = {}
        self.event_handlers: Dict[EventType, Callable] = {}
        
    def register_event_handler(self, event_type: EventType, handler: Callable):
        """注册事件处理器"""
        self.event_handlers[event_type] = handler
    
    def trigger_event(self, event_type: EventType, severity: int = 5) -> GameEvent:
        """触发游戏事件"""
        event_id = f"{event_type.value}_{datetime.now().timestamp()}"
        
        event_configs = {
            EventType.CRYING: {
                "duration": random.randint(30, 300),
                "required_actions": [ActionType.COMFORT, ActionType.ROCK_TO_SLEEP],
                "description": "宝宝开始哭闹，需要安抚"
            },
            EventType.DIAPER_CHANGE: {
                "duration": random.randint(60, 180),
                "required_actions": [ActionType.CHANGE_DIAPER],
                "description": "需要更换尿布"
            },
            EventType.EXPLOSIVE_DIAPER: {
                "duration": random.randint(120, 300),
                "required_actions": [ActionType.CHANGE_DIAPER, ActionType.APPLY_CREAM],
                "description": "💥 生化危机！炸屎事件发生！"
            },
            EventType.MIDNIGHT_TERROR: {
                "duration": random.randint(300, 900),
                "required_actions": [ActionType.COMFORT, ActionType.ROCK_TO_SLEEP],
                "description": "🌙 午夜凶铃：凌晨3点的肠绞痛攻击"
            },
            EventType.STROLLER_TETRIS: {
                "duration": random.randint(180, 600),
                "required_actions": [ActionType.ROTATE_ITEM, ActionType.PLACE_ITEM, ActionType.DISASSEMBLE],
                "description": "🧩 后备箱俄罗斯方块：出行打包大挑战"
            },
            EventType.PICKY_EATER_NEGOTIATION: {
                "duration": random.randint(300, 1200),
                "required_actions": [ActionType.PLAY_CARD, ActionType.NEGOTIATE, ActionType.DISTRACT],
                "description": "🥦 挑食谈判专家：西兰花大作战"
            }
        }
        
        config = event_configs.get(event_type, {
            "duration": 60,
            "required_actions": [ActionType.COMFORT],
            "description": "未知事件"
        })
        
        event = GameEvent(
            id=event_id,
            event_type=event_type,
            severity=severity,
            duration=config["duration"],
            required_actions=config["required_actions"],
            description=config["description"]
        )
        
        self.active_events[event_id] = event
        return event
    
    def resolve_event(self, event_id: str, action: PlayerAction) -> bool:
        """解决事件"""
        if event_id not in self.active_events:
            return False
            
        event = self.active_events[event_id]
        if action.action_type in event.required_actions:
            event.is_active = False
            del self.active_events[event_id]
            return True
        return False
class CryingTask(TaskInterface):
    """哭闹安抚任务"""
    
    async def execute(self, game_state: GameState, player_action: Optional[PlayerAction] = None) -> GameState:
        if player_action and player_action.action_type in [ActionType.COMFORT, ActionType.ROCK_TO_SLEEP]:
            # 成功安抚
            if player_action.response_time <= 30:  # 30秒内响应
                game_state.comfort = min(100, game_state.comfort + 15)
                game_state.sanity = min(100, game_state.sanity + 5)
            else:
                game_state.comfort = min(100, game_state.comfort + 5)
                game_state.sanity = max(0, game_state.sanity - 5)
        else:
            # 未处理或处理不当
            game_state.comfort = max(0, game_state.comfort - 10)
            game_state.sanity = max(0, game_state.sanity - 15)
            
        return game_state
    
    def validate_action(self, action: PlayerAction, game_state: GameState) -> bool:
        return action.action_type in [ActionType.COMFORT, ActionType.ROCK_TO_SLEEP]
    
    def calculate_score_impact(self, action: PlayerAction, game_state: GameState) -> Dict[str, int]:
        impact = {"comfort": 0, "sanity": 0, "kpi": 0}
        
        if action.response_time > 30:
            impact["kpi"] -= 5  # 响应延迟扣分
        if action.response_time > 120:
            impact["kpi"] -= 15  # 严重延迟
            
        if action.success:
            impact["kpi"] += 10
        else:
            impact["kpi"] -= 8
            
        return impact


class ExplosiveDiaperTask(TaskInterface):
    """生化危机：换尿布炸弹任务"""
    
    def __init__(self):
        self.difficulty_multiplier = 2.0
        self.requires_cooperation = True
    
    async def execute(self, game_state: GameState, player_action: Optional[PlayerAction] = None) -> GameState:
        if not player_action:
            # 未处理，灾难性后果
            game_state.comfort = max(0, game_state.comfort - 25)
            game_state.sanity = max(0, game_state.sanity - 30)
            game_state.parenting_kpi = max(0, game_state.parenting_kpi - 20)
            return game_state
            
        if player_action.action_type == ActionType.CHANGE_DIAPER:
            # 检查是否有正确的处理步骤
            success_rate = 0.7 if player_action.response_time <= 60 else 0.3
            
            if random.random() < success_rate:
                game_state.comfort = min(100, game_state.comfort + 20)
                game_state.sanity = max(0, game_state.sanity - 5)  # 即使成功也有心理创伤
            else:
                # 处理失败，弄得到处都是
                game_state.comfort = max(0, game_state.comfort - 10)
                game_state.sanity = max(0, game_state.sanity - 20)
                game_state.parenting_kpi = max(0, game_state.parenting_kpi - 15)
                
        return game_state
    
    def validate_action(self, action: PlayerAction, game_state: GameState) -> bool:
        return action.action_type in [ActionType.CHANGE_DIAPER, ActionType.APPLY_CREAM]
    
    def calculate_score_impact(self, action: PlayerAction, game_state: GameState) -> Dict[str, int]:
        impact = {"comfort": 0, "sanity": 0, "kpi": 0}
        
        if action.action_type == ActionType.CHANGE_DIAPER:
            if action.success:
                impact["kpi"] += 15  # 成功处理生化危机奖励
            else:
                impact["kpi"] -= 25  # 搞砸了严重扣分
                
        return impact
class MidnightTerrorTask(TaskInterface):
    """午夜凶铃：睡眠剥夺战任务"""
    
    def __init__(self):
        self.hallucination_threshold = 30  # 理智值低于30开始出现幻觉
        self.critical_response_time = 300  # 5分钟内必须响应
    
    async def execute(self, game_state: GameState, player_action: Optional[PlayerAction] = None) -> GameState:
        # 午夜事件对理智值的持续消耗
        base_sanity_loss = 20
        
        if game_state.game_mode == GameMode.HARD:
            base_sanity_loss = 35  # 困难模式下更严重
            
        if not player_action:
            # 未响应，持续消耗理智值
            game_state.sanity = max(0, game_state.sanity - base_sanity_loss)
            game_state.comfort = max(0, game_state.comfort - 30)
            return game_state
            
        # 检查响应时间
        if player_action.response_time > self.critical_response_time:
            # 响应太慢，额外惩罚
            game_state.parenting_kpi = max(0, game_state.parenting_kpi - 20)
            
        if player_action.action_type in [ActionType.COMFORT, ActionType.ROCK_TO_SLEEP]:
            # 正确的安抚行动
            comfort_gain = 25 if player_action.response_time <= 60 else 10
            sanity_loss = 10 if player_action.response_time <= 60 else 15
            
            game_state.comfort = min(100, game_state.comfort + comfort_gain)
            game_state.sanity = max(0, game_state.sanity - sanity_loss)
            
        return game_state
    
    def validate_action(self, action: PlayerAction, game_state: GameState) -> bool:
        return action.action_type in [ActionType.COMFORT, ActionType.ROCK_TO_SLEEP]
    
    def calculate_score_impact(self, action: PlayerAction, game_state: GameState) -> Dict[str, int]:
        impact = {"comfort": 0, "sanity": 0, "kpi": 0}
        
        # 午夜事件的特殊评分规则
        if action.response_time <= 60:
            impact["kpi"] += 20  # 快速响应奖励
        elif action.response_time <= 300:
            impact["kpi"] += 5   # 及时响应
        else:
            impact["kpi"] -= 25  # 响应过慢严重扣分
            
        # 理智值过低时的额外惩罚
        if game_state.sanity < self.hallucination_threshold:
            impact["kpi"] -= 10  # 幻觉状态下操作扣分
            
        return impact
    
    def is_hallucinating(self, game_state: GameState) -> bool:
        """检查是否处于幻觉状态"""
        return game_state.sanity < self.hallucination_threshold


class StrollerTetrisTask(TaskInterface):
    """后备箱俄罗斯方块：出行打包任务"""
    
    def __init__(self):
        self.trunk_size = (8, 6)  # 后备箱尺寸 8x6
        self.items = self._generate_items()
        self.trunk_grid = [[0 for _ in range(self.trunk_size[1])] for _ in range(self.trunk_size[0])]
        self.time_pressure = True
        
    def _generate_items(self) -> List[TetrisItem]:
        """生成需要打包的物品"""
        items = [
            TetrisItem("婴儿车", [[1,1,1], [0,1,0], [0,1,0]], priority=5),
            TetrisItem("妈咪包", [[1,1], [1,1]], priority=4),
            TetrisItem("辅食机", [[1,1,1], [1,0,1]], priority=3),
            TetrisItem("备用衣物", [[1,1,1]], priority=2),
            TetrisItem("玩具箱", [[1,1], [1,0]], priority=2),
            TetrisItem("折叠椅", [[1], [1], [1], [1]], priority=1),
            TetrisItem("尿布包", [[1,1,1,1]], priority=3),
            TetrisItem("奶瓶保温袋", [[1,1]], priority=2)
        ]
        return items
    
    def _can_place_item(self, item: TetrisItem, x: int, y: int) -> bool:
        """检查物品是否可以放置在指定位置"""
        shape = self._get_rotated_shape(item)
        
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == 1:
                    new_x, new_y = x + i, y + j
                    if (new_x >= self.trunk_size[0] or new_y >= self.trunk_size[1] or 
                        new_x < 0 or new_y < 0 or self.trunk_grid[new_x][new_y] != 0):
                        return False
        return True
    
    def _get_rotated_shape(self, item: TetrisItem) -> List[List[int]]:
        """获取旋转后的物品形状"""
        shape = item.shape
        for _ in range(item.rotation // 90):
            # 90度顺时针旋转
            shape = [[shape[len(shape)-1-j][i] for j in range(len(shape))] 
                    for i in range(len(shape[0]))]
        return shape
    
    def _place_item(self, item: TetrisItem, x: int, y: int) -> bool:
        """在指定位置放置物品"""
        if not self._can_place_item(item, x, y):
            return False
            
        shape = self._get_rotated_shape(item)
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == 1:
                    self.trunk_grid[x + i][y + j] = hash(item.name) % 9 + 1
        return True
    
    async def execute(self, game_state: GameState, player_action: Optional[PlayerAction] = None) -> GameState:
        if not player_action:
            # 时间耗尽，打包失败
            game_state.parenting_kpi = max(0, game_state.parenting_kpi - 25)
            game_state.sanity = max(0, game_state.sanity - 20)
            return game_state
            
        action_data = player_action.extra_data
        
        if player_action.action_type == ActionType.ROTATE_ITEM:
            item_name = action_data.get("item_name")
            item = next((i for i in self.items if i.name == item_name), None)
            if item:
                item.rotation = (item.rotation + 90) % 360
                game_state.sanity = max(0, game_state.sanity - 2)  # 旋转消耗精力
                
        elif player_action.action_type == ActionType.PLACE_ITEM:
            item_name = action_data.get("item_name")
            x, y = action_data.get("position", (0, 0))
            item = next((i for i in self.items if i.name == item_name), None)
            
            if item and self._place_item(item, x, y):
                self.items.remove(item)
                game_state.comfort = min(100, game_state.comfort + 10)
                
                # 检查是否完成打包
                if not self.items:
                    game_state.parenting_kpi = min(100, game_state.parenting_kpi + 30)
                    game_state.sanity = min(100, game_state.sanity + 15)
            else:
                # 放置失败
                game_state.sanity = max(0, game_state.sanity - 10)
                game_state.parenting_kpi = max(0, game_state.parenting_kpi - 5)
                
        elif player_action.action_type == ActionType.DISASSEMBLE:
            item_name = action_data.get("item_name")
            item = next((i for i in self.items if i.name == item_name), None)
            if item and not item.is_disassembled:
                # 拆解物品使其更容易放置
                item.shape = [[1] for _ in range(sum(sum(row) for row in item.shape))]
                item.is_disassembled = True
                game_state.sanity = max(0, game_state.sanity - 5)
                
        return game_state
    
    def validate_action(self, action: PlayerAction, game_state: GameState) -> bool:
        return action.action_type in [ActionType.ROTATE_ITEM, ActionType.PLACE_ITEM, ActionType.DISASSEMBLE]
    
    def calculate_score_impact(self, action: PlayerAction, game_state: GameState) -> Dict[str, int]:
        impact = {"comfort": 0, "sanity": 0, "kpi": 0}
        
        if action.action_type == ActionType.PLACE_ITEM and action.success:
            impact["kpi"] += 15  # 成功放置奖励
        elif action.action_type == ActionType.PLACE_ITEM and not action.success:
            impact["kpi"] -= 10  # 放置失败扣分
            
        # 时间压力下的额外扣分
        if action.response_time > 30:
            impact["kpi"] -= 5
            
        return impact
    
    def get_packing_progress(self) -> Dict[str, Any]:
        """获取打包进度"""
        total_items = len(self.items) + sum(sum(row) for row in self.trunk_grid if any(cell != 0 for cell in row))
        packed_items = sum(sum(1 for cell in row if cell != 0) for row in self.trunk_grid)
        
        return {
            "progress": packed_items / max(total_items, 1),
            "remaining_items": [item.name for item in self.items],
            "trunk_grid": self.trunk_grid
        }


class PickyEaterNegotiationTask(TaskInterface):
    """挑食谈判专家：卡牌对战系统"""
    
    def __init__(self):
        self.target_food = "西兰花"
        self.child_resistance = 80  # 孩子的抗拒值 (0-100)
        self.child_attention = 100  # 注意力值 (0-100)
        self.child_hunger = 60     # 饥饿度 (0-100)
        self.parent_patience = 100  # 父母耐心值 (0-100)
        self.cards_deck = self._generate_cards()
        self.used_cards = []
        self.negotiation_rounds = 0
        self.max_rounds = 10
        
    def _generate_cards(self) -> List[NegotiationCard]:
        """生成谈判卡牌"""
        cards = [
            NegotiationCard(
                "飞机勺", "strategy", 7,
                {"attention": -10, "resistance": -15},
                "张开嘴巴，飞机要降落啦！"
            ),
            NegotiationCard(
                "藏在肉里", "strategy", 5,
                {"resistance": 25},  # 被发现后抗拒增加
                "偷偷把蔬菜藏在肉里，50%成功率"
            ),
            NegotiationCard(
                "看动画片", "distraction", 9,
                {"attention": -30, "bad_habit": 1},
                "100%有效，但会养成坏习惯"
            ),
            NegotiationCard(
                "威逼利诱", "bribe", 6,
                {"resistance": -20, "future_expectation": 1},
                "吃完这个给糖吃！"
            ),
            NegotiationCard(
                "营养科普", "education", 3,
                {"attention": -5},
                "西兰花含有丰富的维生素C..."
            ),
            NegotiationCard(
                "同伴示范", "social", 8,
                {"resistance": -25},
                "看，小明都在吃西兰花呢！"
            ),
            NegotiationCard(
                "饥饿战术", "patience", 4,
                {"hunger": 20, "resistance": -10},
                "不吃就饿着，看谁先妥协"
            ),
            NegotiationCard(
                "游戏化", "strategy", 7,
                {"attention": 10, "resistance": -20},
                "我们来玩吃西兰花小怪兽的游戏！"
            ),
            NegotiationCard(
                "情感绑架", "threat", 2,
                {"resistance": 30, "trust": -10},
                "你不吃妈妈就不爱你了..."
            ),
            NegotiationCard(
                "放弃", "surrender", 0,
                {"parent_dignity": -50},
                "算了，今天就不吃了..."
            )
        ]
        return cards
    
    def _calculate_card_effectiveness(self, card: NegotiationCard) -> int:
        """计算卡牌在当前状态下的有效性"""
        base_effectiveness = card.effectiveness
        
        # 根据孩子状态调整有效性
        if self.child_attention < 30 and card.card_type == "education":
            base_effectiveness = max(1, base_effectiveness - 5)  # 注意力不集中时科普无效
            
        if self.child_hunger > 80 and card.card_type == "bribe":
            base_effectiveness += 3  # 饿的时候更容易被贿赂
            
        if self.negotiation_rounds > 5:
            base_effectiveness = max(1, base_effectiveness - 2)  # 时间长了效果下降
            
        return base_effectiveness
    
    async def execute(self, game_state: GameState, player_action: Optional[PlayerAction] = None) -> GameState:
        if not player_action:
            # 超时，孩子获胜
            game_state.parenting_kpi = max(0, game_state.parenting_kpi - 20)
            game_state.sanity = max(0, game_state.sanity - 25)
            return game_state
            
        if self.negotiation_rounds >= self.max_rounds:
            # 回合数耗尽，谈判失败
            game_state.parenting_kpi = max(0, game_state.parenting_kpi - 15)
            game_state.sanity = max(0, game_state.sanity - 20)
            return game_state
            
        action_data = player_action.extra_data
        
        if player_action.action_type == ActionType.PLAY_CARD:
            card_name = action_data.get("card_name")
            card = next((c for c in self.cards_deck if c.name == card_name), None)
            
            if card and card not in self.used_cards:
                self.used_cards.append(card)
                self.negotiation_rounds += 1
                
                # 计算卡牌效果
                effectiveness = self._calculate_card_effectiveness(card)
                success_rate = min(0.9, effectiveness / 10.0)
                
                if random.random() < success_rate:
                    # 卡牌成功
                    for effect, value in card.side_effects.items():
                        if effect == "resistance":
                            self.child_resistance = max(0, min(100, self.child_resistance + value))
                        elif effect == "attention":
                            self.child_attention = max(0, min(100, self.child_attention + value))
                        elif effect == "hunger":
                            self.child_hunger = max(0, min(100, self.child_hunger + value))
                    
                    # 检查胜利条件
                    if self.child_resistance <= 20:
                        # 谈判成功！
                        game_state.parenting_kpi = min(100, game_state.parenting_kpi + 25)
                        game_state.comfort = min(100, game_state.comfort + 20)
                        game_state.sanity = min(100, game_state.sanity + 10)
                        return game_state
                else:
                    # 卡牌失败，孩子抗拒增加
                    self.child_resistance = min(100, self.child_resistance + 15)
                    self.parent_patience = max(0, self.parent_patience - 10)
                
                # 父母耐心消耗
                self.parent_patience = max(0, self.parent_patience - 5)
                if self.parent_patience <= 0:
                    # 父母崩溃
                    game_state.sanity = max(0, game_state.sanity - 30)
                    game_state.parenting_kpi = max(0, game_state.parenting_kpi - 20)
                    
        elif player_action.action_type == ActionType.NEGOTIATE:
            # 直接谈判，不使用卡牌
            self.negotiation_rounds += 1
            success_rate = max(0.1, (100 - self.child_resistance) / 100.0)
            
            if random.random() < success_rate:
                self.child_resistance = max(0, self.child_resistance - 10)
                game_state.sanity = max(0, game_state.sanity - 5)
            else:
                self.child_resistance = min(100, self.child_resistance + 10)
                game_state.sanity = max(0, game_state.sanity - 10)
                
        return game_state
    
    def validate_action(self, action: PlayerAction, game_state: GameState) -> bool:
        return action.action_type in [ActionType.PLAY_CARD, ActionType.NEGOTIATE, ActionType.DISTRACT]
    
    def calculate_score_impact(self, action: PlayerAction, game_state: GameState) -> Dict[str, int]:
        impact = {"comfort": 0, "sanity": 0, "kpi": 0}
        
        if action.action_type == ActionType.PLAY_CARD:
            card_name = action.extra_data.get("card_name", "")
            
            # 根据卡牌类型给予不同评分
            if "威逼利诱" in card_name or "情感绑架" in card_name:
                impact["kpi"] -= 5  # 不良教育方式扣分
            elif "游戏化" in card_name or "同伴示范" in card_name:
                impact["kpi"] += 10  # 正面教育方式加分
            elif "放弃" in card_name:
                impact["kpi"] -= 15  # 放弃严重扣分
                
        # 谈判轮数过多扣分
        if self.negotiation_rounds > 7:
            impact["kpi"] -= 5
            
        return impact
    
    def get_negotiation_status(self) -> Dict[str, Any]:
        """获取谈判状态"""
        return {
            "child_resistance": self.child_resistance,
            "child_attention": self.child_attention,
            "child_hunger": self.child_hunger,
            "parent_patience": self.parent_patience,
            "rounds_remaining": self.max_rounds - self.negotiation_rounds,
            "available_cards": [card.name for card in self.cards_deck if card not in self.used_cards],
            "success_probability": max(0, (100 - self.child_resistance) / 100.0)
        }


class GameModeManager:
    """游戏模式管理器"""
    
    def __init__(self):
        self.mode_configs = {
            GameMode.EASY: {
                "event_frequency": 0.3,      # 事件频率倍数
                "night_protection": True,     # 夜间保护
                "offline_pause": True,        # 离线暂停
                "sanity_decay_rate": 0.5     # 理智值衰减率
            },
            GameMode.NORMAL: {
                "event_frequency": 1.0,
                "night_protection": False,
                "offline_pause": False,
                "sanity_decay_rate": 1.0
            },
            GameMode.HARD: {
                "event_frequency": 1.8,
                "night_protection": False,
                "offline_pause": False,
                "sanity_decay_rate": 1.5,
                "force_notifications": True,  # 强制通知
                "sleep_disruption": True      # 专门在深睡期触发事件
            }
        }
    
    def get_mode_config(self, mode: GameMode) -> Dict[str, Any]:
        return self.mode_configs.get(mode, self.mode_configs[GameMode.NORMAL])
    
    def should_trigger_event(self, mode: GameMode, current_time: datetime) -> bool:
        config = self.get_mode_config(mode)
        
        # 夜间保护检查
        if config.get("night_protection") and 22 <= current_time.hour or current_time.hour <= 8:
            return False
            
        # 基于频率的随机触发
        base_probability = 0.1  # 基础10%概率每分钟
        adjusted_probability = base_probability * config["event_frequency"]
        
        return random.random() < adjusted_probability
class MultiplayerSession:
    """多人协作会话管理"""
    
    def __init__(self, session_id: str, host_player_id: str):
        self.session_id = session_id
        self.host_player_id = host_player_id
        self.players: Dict[str, Dict] = {}
        self.shared_state = GameState()
        self.is_active = True
        self.created_at = datetime.now()
        
    def add_player(self, player_id: str, player_name: str) -> bool:
        """添加玩家到会话"""
        if len(self.players) >= 2:  # 最多2人协作
            return False
            
        self.players[player_id] = {
            "name": player_name,
            "joined_at": datetime.now(),
            "individual_kpi": 100,
            "actions_count": 0
        }
        return True
    
    def remove_player(self, player_id: str):
        """移除玩家"""
        if player_id in self.players:
            del self.players[player_id]
            
    def sync_action(self, player_id: str, action: PlayerAction) -> GameState:
        """同步玩家行动"""
        if player_id in self.players:
            self.players[player_id]["actions_count"] += 1
            # 这里可以添加个人表现跟踪逻辑
            
        return self.shared_state


class ScoringSystem:
    """评分系统"""
    
    def __init__(self):
        self.score_weights = {
            "response_time": 0.3,
            "action_accuracy": 0.4,
            "cooperation": 0.2,
            "consistency": 0.1
        }
    
    def calculate_kpi(self, game_state: GameState, recent_actions: List[PlayerAction]) -> int:
        """计算综合KPI分数"""
        base_score = game_state.parenting_kpi
        
        # 响应时间评分
        avg_response_time = sum(a.response_time for a in recent_actions) / len(recent_actions) if recent_actions else 0
        if avg_response_time <= 30:
            response_bonus = 10
        elif avg_response_time <= 60:
            response_bonus = 5
        else:
            response_bonus = -5
            
        # 成功率评分
        success_rate = sum(1 for a in recent_actions if a.success) / len(recent_actions) if recent_actions else 0
        accuracy_bonus = int(success_rate * 20) - 10
        
        # 理智值影响
        sanity_penalty = 0
        if game_state.sanity < 30:
            sanity_penalty = -15
        elif game_state.sanity < 50:
            sanity_penalty = -5
            
        final_score = base_score + response_bonus + accuracy_bonus + sanity_penalty
        return max(0, min(100, final_score))
    
    def get_performance_feedback(self, kpi_score: int) -> str:
        """获取表现反馈"""
        if kpi_score >= 90:
            return "🏆 育儿大师！你已经掌握了硬核父母的精髓！"
        elif kpi_score >= 75:
            return "👍 表现优秀！继续保持这种状态！"
        elif kpi_score >= 60:
            return "😅 还不错，但还有提升空间..."
        elif kpi_score >= 50:
            return "⚠️ 及格线边缘，需要加油了！"
        else:
            return "💀 建议重新学习育儿知识，或者考虑请保姆..."


class AchievementSystem:
    """成就系统"""
    
    def __init__(self):
        self.achievements = {
            "bomb_defuser": {
                "name": "拆弹专家",
                "description": "在生化危机事件中未沾染任何衣物",
                "condition": lambda stats: stats.get("explosive_diaper_perfect", 0) >= 1
            },
            "time_master": {
                "name": "时间管理大师", 
                "description": "一边喂奶一边完成了工作邮件回复",
                "condition": lambda stats: stats.get("multitask_success", 0) >= 1
            },
            "survival_mode": {
                "name": "生存模式",
                "description": "在困难模式下坚持7天",
                "condition": lambda stats: stats.get("hard_mode_days", 0) >= 7
            },
            "sanity_keeper": {
                "name": "理智守护者",
                "description": "理智值从未低于50",
                "condition": lambda stats: stats.get("min_sanity", 100) >= 50
            },
            "tetris_master": {
                "name": "打包大师",
                "description": "完美完成后备箱俄罗斯方块挑战",
                "condition": lambda stats: stats.get("tetris_perfect", 0) >= 1
            },
            "negotiation_expert": {
                "name": "谈判专家",
                "description": "在挑食谈判中不使用威逼利诱获胜",
                "condition": lambda stats: stats.get("clean_negotiation_win", 0) >= 1
            },
            "card_master": {
                "name": "卡牌大师",
                "description": "在一次谈判中使用超过5张不同卡牌",
                "condition": lambda stats: stats.get("max_cards_used", 0) >= 5
            },
            "efficiency_king": {
                "name": "效率之王",
                "description": "在3分钟内完成俄罗斯方块打包",
                "condition": lambda stats: stats.get("tetris_speed_record", 999) <= 180
            }
        }
    
    def check_achievements(self, player_stats: Dict[str, Any]) -> List[str]:
        """检查并返回新获得的成就"""
        earned = []
        for achievement_id, achievement in self.achievements.items():
            if achievement_id not in player_stats.get("earned_achievements", []):
                if achievement["condition"](player_stats):
                    earned.append(achievement_id)
        return earned
class HardcoreParentingSimulator:
    """育儿模拟器主控制器"""
    
    def __init__(self):
        self.game_state = GameState()
        self.event_manager = GameEventManager()
        self.mode_manager = GameModeManager()
        self.scoring_system = ScoringSystem()
        self.achievement_system = AchievementSystem()
        self.active_sessions: Dict[str, MultiplayerSession] = {}
        self.player_stats: Dict[str, Dict] = {}
        
        # 注册任务处理器
        self.task_handlers = {
            EventType.CRYING: CryingTask(),
            EventType.EXPLOSIVE_DIAPER: ExplosiveDiaperTask(),
            EventType.MIDNIGHT_TERROR: MidnightTerrorTask(),
            EventType.STROLLER_TETRIS: StrollerTetrisTask(),
            EventType.PICKY_EATER_NEGOTIATION: PickyEaterNegotiationTask()
        }
    
    async def start_game(self, player_id: str, mode: GameMode = GameMode.NORMAL) -> GameState:
        """开始游戏"""
        self.game_state = GameState(game_mode=mode)
        
        # 初始化玩家统计
        if player_id not in self.player_stats:
            self.player_stats[player_id] = {
                "total_playtime": 0,
                "actions_taken": 0,
                "earned_achievements": [],
                "best_kpi": 0,
                "min_sanity": 100
            }
        
        return self.game_state
    
    async def process_action(self, player_id: str, action: PlayerAction, 
                           session_id: Optional[str] = None) -> Dict[str, Any]:
        """处理玩家行动"""
        result = {
            "success": False,
            "new_state": self.game_state,
            "score_impact": {},
            "message": "",
            "achievements": []
        }
        
        # 查找对应的活跃事件
        active_event = None
        for event in self.event_manager.active_events.values():
            if action.action_type in event.required_actions:
                active_event = event
                break
        
        if not active_event:
            result["message"] = "当前没有需要这个行动的事件"
            return result
        
        # 获取对应的任务处理器
        task_handler = self.task_handlers.get(active_event.event_type)
        if not task_handler:
            result["message"] = "未找到对应的任务处理器"
            return result
        
        # 验证行动
        if not task_handler.validate_action(action, self.game_state):
            result["message"] = "无效的行动"
            return result
        
        # 执行任务
        self.game_state = await task_handler.execute(self.game_state, action)
        
        # 计算分数影响
        score_impact = task_handler.calculate_score_impact(action, self.game_state)
        
        # 更新KPI
        for key, value in score_impact.items():
            if key == "kpi":
                self.game_state.parenting_kpi = max(0, min(100, self.game_state.parenting_kpi + value))
        
        # 解决事件
        event_resolved = self.event_manager.resolve_event(active_event.id, action)
        
        # 更新玩家统计
        self.player_stats[player_id]["actions_taken"] += 1
        self.player_stats[player_id]["min_sanity"] = min(
            self.player_stats[player_id]["min_sanity"], 
            self.game_state.sanity
        )
        
        # 检查成就
        new_achievements = self.achievement_system.check_achievements(self.player_stats[player_id])
        if new_achievements:
            self.player_stats[player_id]["earned_achievements"].extend(new_achievements)
        
        # 检查失败条件
        if self.game_state.comfort <= 0:
            result["message"] = "💀 任务失败！宝宝舒适度归零！"
        elif self.game_state.parenting_kpi < 50:
            result["message"] = "⚠️ 警告：育儿KPI过低，面临剥夺抚养权风险！"
        
        result.update({
            "success": event_resolved,
            "new_state": self.game_state,
            "score_impact": score_impact,
            "achievements": new_achievements,
            "message": result["message"] or self.scoring_system.get_performance_feedback(self.game_state.parenting_kpi)
        })
        
        return result
    
    async def trigger_random_event(self) -> Optional[GameEvent]:
        """触发随机事件"""
        current_time = datetime.now()
        
        if not self.mode_manager.should_trigger_event(self.game_state.game_mode, current_time):
            return None
        
        # 根据时间和模式选择事件类型
        possible_events = [EventType.CRYING, EventType.DIAPER_CHANGE, EventType.FEEDING]
        
        # 困难模式下的特殊事件
        if self.game_state.game_mode == GameMode.HARD:
            if 2 <= current_time.hour <= 5:  # 凌晨时段
                possible_events.extend([EventType.MIDNIGHT_TERROR, EventType.COLIC_ATTACK])
            possible_events.extend([EventType.EXPLOSIVE_DIAPER, EventType.STROLLER_TETRIS, EventType.PICKY_EATER_NEGOTIATION])
        elif self.game_state.game_mode == GameMode.NORMAL:
            # 普通模式偶尔触发特色任务
            if random.random() < 0.3:
                possible_events.extend([EventType.STROLLER_TETRIS, EventType.PICKY_EATER_NEGOTIATION])
        
        event_type = random.choice(possible_events)
        severity = random.randint(3, 8) if self.game_state.game_mode != GameMode.HARD else random.randint(6, 10)
        
        return self.event_manager.trigger_event(event_type, severity)
    
    def get_game_status(self) -> Dict[str, Any]:
        """获取当前游戏状态"""
        return {
            "game_state": {
                "comfort": self.game_state.comfort,
                "sanity": self.game_state.sanity,
                "parenting_kpi": self.game_state.parenting_kpi,
                "mode": self.game_state.game_mode.value
            },
            "active_events": [
                {
                    "id": event.id,
                    "type": event.event_type.value,
                    "description": event.description,
                    "severity": event.severity,
                    "required_actions": [action.value for action in event.required_actions]
                }
                for event in self.event_manager.active_events.values()
            ],
            "is_hallucinating": self.game_state.sanity < 30
        }