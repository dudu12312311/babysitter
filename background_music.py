#!/usr/bin/env python3
"""
背景音乐系统
为育儿模拟器添加背景音乐和音效
"""

import os
from pathlib import Path

# 尝试导入 pygame
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("警告: pygame 未安装，音乐功能不可用")


class BackgroundMusicPlayer:
    """背景音乐播放器"""
    
    def __init__(self, music_folder="music"):
        """
        初始化音乐播放器
        
        Args:
            music_folder: 音乐文件夹路径
        """
        self.music_folder = music_folder
        self.is_initialized = False
        self.is_playing = False
        self.current_track = None
        self.volume = 0.5  # 默认音量 50%
        
        # 创建音乐文件夹
        os.makedirs(music_folder, exist_ok=True)
        
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init()
                self.is_initialized = True
                print("✓ 音乐系统初始化成功")
            except Exception as e:
                print(f"✗ 音乐系统初始化失败: {e}")
        else:
            print("✗ pygame 未安装，请运行: pip install pygame")
    
    def get_music_files(self):
        """获取音乐文件列表"""
        if not os.path.exists(self.music_folder):
            return []
        
        music_extensions = ['.mp3', '.wav', '.ogg', '.flac']
        music_files = []
        
        for file in os.listdir(self.music_folder):
            if any(file.lower().endswith(ext) for ext in music_extensions):
                music_files.append(file)
        
        return sorted(music_files)
    
    def play(self, music_file=None, loop=True):
        """
        播放音乐
        
        Args:
            music_file: 音乐文件名（如果为 None，播放第一个找到的音乐）
            loop: 是否循环播放
        """
        if not self.is_initialized:
            return {"success": False, "message": "音乐系统未初始化"}
        
        try:
            # 如果没有指定文件，使用第一个音乐文件
            if music_file is None:
                music_files = self.get_music_files()
                if not music_files:
                    return {
                        "success": False,
                        "message": f"在 {self.music_folder} 文件夹中没有找到音乐文件"
                    }
                music_file = music_files[0]
            
            # 构建完整路径
            music_path = os.path.join(self.music_folder, music_file)
            
            if not os.path.exists(music_path):
                return {
                    "success": False,
                    "message": f"音乐文件不存在: {music_path}"
                }
            
            # 加载并播放音乐
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1 if loop else 0)  # -1 表示无限循环
            
            self.is_playing = True
            self.current_track = music_file
            
            return {
                "success": True,
                "message": f"正在播放: {music_file}",
                "track": music_file,
                "volume": self.volume
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"播放失败: {str(e)}"
            }
    
    def pause(self):
        """暂停音乐"""
        if not self.is_initialized:
            return {"success": False, "message": "音乐系统未初始化"}
        
        try:
            pygame.mixer.music.pause()
            self.is_playing = False
            return {"success": True, "message": "音乐已暂停"}
        except Exception as e:
            return {"success": False, "message": f"暂停失败: {str(e)}"}
    
    def resume(self):
        """恢复播放"""
        if not self.is_initialized:
            return {"success": False, "message": "音乐系统未初始化"}
        
        try:
            pygame.mixer.music.unpause()
            self.is_playing = True
            return {"success": True, "message": "音乐已恢复"}
        except Exception as e:
            return {"success": False, "message": f"恢复失败: {str(e)}"}
    
    def stop(self):
        """停止音乐"""
        if not self.is_initialized:
            return {"success": False, "message": "音乐系统未初始化"}
        
        try:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.current_track = None
            return {"success": True, "message": "音乐已停止"}
        except Exception as e:
            return {"success": False, "message": f"停止失败: {str(e)}"}
    
    def set_volume(self, volume):
        """
        设置音量
        
        Args:
            volume: 音量 (0.0 - 1.0)
        """
        if not self.is_initialized:
            return {"success": False, "message": "音乐系统未初始化"}
        
        try:
            volume = max(0.0, min(1.0, volume))  # 限制在 0-1 之间
            pygame.mixer.music.set_volume(volume)
            self.volume = volume
            return {
                "success": True,
                "message": f"音量已设置为: {int(volume * 100)}%",
                "volume": volume
            }
        except Exception as e:
            return {"success": False, "message": f"设置音量失败: {str(e)}"}
    
    def get_status(self):
        """获取播放状态"""
        return {
            "is_initialized": self.is_initialized,
            "is_playing": self.is_playing,
            "current_track": self.current_track,
            "volume": self.volume,
            "available_tracks": self.get_music_files()
        }


# 使用示例
if __name__ == "__main__":
    print("=" * 60)
    print("背景音乐系统测试")
    print("=" * 60)
    
    # 创建播放器
    player = BackgroundMusicPlayer()
    
    # 检查状态
    status = player.get_status()
    print(f"\n系统状态:")
    print(f"  初始化: {status['is_initialized']}")
    print(f"  可用音乐: {len(status['available_tracks'])} 首")
    
    if status['available_tracks']:
        print(f"\n音乐列表:")
        for i, track in enumerate(status['available_tracks'], 1):
            print(f"  {i}. {track}")
        
        # 播放第一首音乐
        print(f"\n尝试播放音乐...")
        result = player.play()
        print(f"  {result['message']}")
        
        if result['success']:
            print(f"\n控制选项:")
            print(f"  1. 暂停 - player.pause()")
            print(f"  2. 恢复 - player.resume()")
            print(f"  3. 停止 - player.stop()")
            print(f"  4. 调整音量 - player.set_volume(0.5)")
    else:
        print(f"\n请将音乐文件放入 'music' 文件夹")
        print(f"支持格式: MP3, WAV, OGG, FLAC")
