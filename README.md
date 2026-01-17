# 育儿模拟器：硬核父母岗前特训

> "在只要孩子不哭，尊严算什么？" 

一个游戏化的育儿训练系统，通过模拟真实育儿场景来训练准父母和新手父母。采用黑色幽默风格，提供三种难度模式和多人协作功能。

## 🎮 核心特性

### 三种游戏模式
- **简单模式 (云养娃)**: 离线暂停，夜间保护，适合观光客
- **普通模式 (实习父母)**: 平衡的游戏体验，适合大多数玩家  
- **困难模式 (地狱特训)**: 7天实时挑战，午夜凶铃，真正的硬核体验

### 核心数值系统
- **宝宝舒适度 (0-100)**: 归零则任务失败
- **父母理智值 (0-100)**: 过低时出现幻觉效果，操作会受影响
- **育儿KPI (0-100)**: 低于50分触发"剥夺抚养权"警告

### 特色任务模式
- **生化危机：换尿布炸弹** - 非对称信息博弈，考验协作能力
- **午夜凶铃：睡眠剥夺战** - 凌晨3点的肠绞痛攻击，测试极限
- **后备箱俄罗斯方块** - 出行打包解谜，物理堆叠挑战
- **挑食谈判专家** - 卡牌对战系统，心理博弈大师

## 🚀 快速开始

### 环境要求
- Python 3.8+
- asyncio 支持

### 安装依赖
```bash
# 基础依赖（系统自带）
# 无需额外安装，使用Python标准库
```

### 基础使用

```python
import asyncio
from hardcore_parenting_simulator import (
    HardcoreParentingSimulator, 
    GameMode, 
    ActionType, 
    PlayerAction
)

async def basic_example():
    # 创建游戏实例
    simulator = HardcoreParentingSimulator()
    
    # 开始游戏
    player_id = "player_001"
    game_state = await simulator.start_game(player_id, GameMode.NORMAL)
    
    # 触发事件
    event = await simulator.trigger_random_event()
    if event:
        print(f"事件: {event.description}")
        
        # 玩家响应
        action = PlayerAction(
            action_type=ActionType.COMFORT,
            response_time=30.0,
            success=True,
            player_id=player_id
        )
        
        result = await simulator.process_action(player_id, action)
        print(f"结果: {result['message']}")

# 运行示例
asyncio.run(basic_example())
```

## 📋 API 文档

### 主要类

#### `HardcoreParentingSimulator`
主控制器类，管理整个游戏流程。

**主要方法:**
- `start_game(player_id, mode)` - 开始游戏
- `process_action(player_id, action)` - 处理玩家行动
- `trigger_random_event()` - 触发随机事件
- `get_game_status()` - 获取当前游戏状态

#### `GameState`
游戏状态数据结构。

**属性:**
- `comfort: int` - 宝宝舒适度 (0-100)
- `sanity: int` - 父母理智值 (0-100)  
- `parenting_kpi: int` - 育儿KPI (0-100)
- `game_mode: GameMode` - 当前游戏模式

#### `PlayerAction`
玩家行动记录。

**属性:**
- `action_type: ActionType` - 行动类型
- `response_time: float` - 响应时间(秒)
- `success: bool` - 是否成功
- `player_id: str` - 玩家ID

### 事件类型 (EventType)
- `CRYING` - 哭闹
- `DIAPER_CHANGE` - 换尿布
- `EXPLOSIVE_DIAPER` - 生化危机
- `MIDNIGHT_TERROR` - 午夜恐怖
- `STROLLER_TETRIS` - 后备箱俄罗斯方块
- `PICKY_EATER_NEGOTIATION` - 挑食谈判
- `FEEDING` - 喂食
- `COLIC_ATTACK` - 肠绞痛

### 行动类型 (ActionType)
- `COMFORT` - 安抚
- `FEED` - 喂食
- `CHANGE_DIAPER` - 换尿布
- `ROCK_TO_SLEEP` - 摇睡
- `CHECK_TEMPERATURE` - 检查体温
- `APPLY_CREAM` - 涂护臀膏
- `ROTATE_ITEM` - 旋转物品 (俄罗斯方块)
- `PLACE_ITEM` - 放置物品 (俄罗斯方块)
- `DISASSEMBLE` - 拆解物品 (俄罗斯方块)
- `PLAY_CARD` - 出牌 (谈判)
- `NEGOTIATE` - 直接谈判
- `DISTRACT` - 分散注意力

## 🎯 使用示例

### 基础游戏流程
```python
import asyncio
from hardcore_parenting_simulator import (
    HardcoreParentingSimulator, 
    GameMode, 
    ActionType, 
    PlayerAction
)

async def basic_example():
    simulator = HardcoreParentingSimulator()
    player_id = "player_001"
    game_state = await simulator.start_game(player_id, GameMode.NORMAL)
    
    # 触发事件并响应
    event = await simulator.trigger_random_event()
    if event:
        action = PlayerAction(
            action_type=ActionType.COMFORT,
            response_time=30.0,
            success=True,
            player_id=player_id
        )
        result = await simulator.process_action(player_id, action)
        print(f"结果: {result['message']}")

asyncio.run(basic_example())
```

### 后备箱俄罗斯方块示例
```python
# 旋转物品
rotate_action = PlayerAction(
    action_type=ActionType.ROTATE_ITEM,
    response_time=5.0,
    success=True,
    player_id="player_001",
    extra_data={"item_name": "婴儿车"}
)

# 放置物品
place_action = PlayerAction(
    action_type=ActionType.PLACE_ITEM,
    response_time=10.0,
    success=True,
    player_id="player_001",
    extra_data={
        "item_name": "婴儿车",
        "position": (2, 1)  # x, y坐标
    }
)
```

### 挑食谈判专家示例
```python
# 使用卡牌
card_action = PlayerAction(
    action_type=ActionType.PLAY_CARD,
    response_time=15.0,
    success=True,
    player_id="player_001",
    extra_data={"card_name": "飞机勺"}
)

# 直接谈判
negotiate_action = PlayerAction(
    action_type=ActionType.NEGOTIATE,
    response_time=20.0,
    success=True,
    player_id="player_001"
)
```

### 运行完整演示
```bash
python example_usage.py
```

### 运行测试
```bash
python test_simulator.py
```

## 🏆 成就系统

- **拆弹专家**: 在生化危机事件中未沾染任何衣物
- **时间管理大师**: 一边喂奶一边完成工作邮件回复
- **生存模式**: 在困难模式下坚持7天
- **理智守护者**: 理智值从未低于50
- **打包大师**: 完美完成后备箱俄罗斯方块挑战
- **谈判专家**: 在挑食谈判中不使用威逼利诱获胜
- **卡牌大师**: 在一次谈判中使用超过5张不同卡牌
- **效率之王**: 在3分钟内完成俄罗斯方块打包

## 🎮 游戏模式详解

### 简单模式：云养娃
- 离线时游戏暂停
- 22:00-08:00 夜间保护
- 事件频率降低70%
- 适合体验可爱宝宝的"观光客"

### 普通模式：实习父母  
- 正常推送通知
- 勿扰模式下静音
- 夜间事件频率降低50%
- 平衡游戏体验与正常生活

### 困难模式：地狱特训
- 7天实时同步挑战
- 强制重要警告权限
- 午夜凶铃：凌晨3点强制高分贝哭声
- 专门在深睡期发起突袭
- 通往白金成就的唯一途径

## 🔧 扩展开发

### 添加新任务类型

```python
class CustomTask(TaskInterface):
    async def execute(self, game_state: GameState, player_action: Optional[PlayerAction] = None) -> GameState:
        # 实现自定义逻辑
        return game_state
    
    def validate_action(self, action: PlayerAction, game_state: GameState) -> bool:
        # 验证行动有效性
        return True
    
    def calculate_score_impact(self, action: PlayerAction, game_state: GameState) -> Dict[str, int]:
        # 计算分数影响
        return {"kpi": 0}
```

### 添加新成就

```python
simulator.achievement_system.achievements["new_achievement"] = {
    "name": "新成就",
    "description": "完成特定条件",
    "condition": lambda stats: stats.get("custom_metric", 0) >= 10
}
```

## 🤝 多人协作

系统支持双人协作模式，模拟真实的夫妻育儿场景：

```python
# 创建多人会话
session = MultiplayerSession("session_001", "host_player")
session.add_player("player_002", "Partner")

# 同步行动
session.sync_action("player_001", action)
```

## 📊 评分系统

评分基于多个维度：
- **响应时间** (30%): 越快响应分数越高
- **行动准确性** (40%): 选择正确行动类型
- **协作能力** (20%): 多人模式下的配合
- **一致性** (10%): 长期表现稳定性

## ⚠️ 注意事项

1. **困难模式警告**: 会真实影响睡眠，请谨慎选择
2. **理智值管理**: 低于30时会出现幻觉效果，影响操作
3. **失败条件**: 宝宝舒适度归零或KPI低于50分会触发相应后果
4. **数据持久化**: 游戏进度会自动保存

## 🎨 设计理念

这款系统不回避育儿的痛苦和混乱，而是用游戏化的机制将这些压力具象化。对于情侣而言，这是检验双方抗压能力、沟通效率和情绪价值的最佳试金石。

**核心理念**: 在游戏中体验真实育儿的挑战，在挑战中学习科学育儿的方法。

---

*"准备好接受硬核父母的挑战了吗？记住：在只要孩子不哭，尊严算什么？"* 💪