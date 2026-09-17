# config.py
import os
from pathlib import Path
import subprocess

# 项目根目录
BASE_DIR = Path(__file__).parent




def _detect_serial():
    """从 adb devices 自动获取当前已连接的设备序列号"""
    #try:
    #    out = subprocess.check_output(["adb", "devices"], text=True)
    #    for line in out.splitlines():
    #        parts = line.split()
    #        # 形如: 127.0.0.1:42035  device
    #        if len(parts) == 2 and parts[1] == "device":
    #            return parts[0]
    #except Exception:
    #    pass
    #return None

#DEVICE_SERIAL = _detect_serial() or "127.0.0.1:5555"  # 连不上时的兜底值
DEVICE_SERIAL = "127.0.0.1:5533"

class Config:
    # 设备配置
    #DEVICE_SERIAL = "SM02G4061994156"  # 当前连接的手机
    DEVICE_SERIAL = DEVICE_SERIAL

    # 同花顺配置
    THS_PACKAGE = "com.hexin.plat.android"

    # 截图配置
    SCREENSHOT_DIR = BASE_DIR / "screenshots"

    # 超时配置（秒）
    DEFAULT_TIMEOUT = 10
    PAGE_LOAD_TIMEOUT = 3

    # 创建目录
    SCREENSHOT_DIR.mkdir(exist_ok=True)


config = Config()
