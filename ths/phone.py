# phone.py
"""
Android 手机状态控制。

功能：
1. 检查 ADB
2. 唤醒手机
3. 判断 Android 锁屏
4. 使用 ~/.ths_secure/pin.enc 自动解密锁屏密码
5. 自动滑动锁屏
6. 自动输入数字密码
7. 确认手机已经解锁

密码不会写入明文文件。
"""

import os
import subprocess
import time
import logging


logger = logging.getLogger(__name__)


class PhoneController:

    def __init__(self):
        self.secure_dir = os.path.expanduser("~/.ths_secure")

        self.pin_file = os.path.join(
            self.secure_dir,
            "pin.enc",
        )

        self.key_file = os.path.join(
            self.secure_dir,
            "pin.key",
        )

        # 当前手机 1080 x 2400
        self.swipe_x = 540
        self.swipe_start_y = 2100
        self.swipe_end_y = 800
        self.swipe_duration = 500

    # =========================================================
    # ADB
    # =========================================================

    def _get_serial(self):
        try:
            from ths.config import config
            return getattr(config, "DEVICE_SERIAL", None)
        except Exception:
            return None

    def _adb(self, *args, check=True, timeout=10):
        """执行 adb 命令。"""

        serial = self._get_serial()

        cmd = ["adb"]

        if serial:
            cmd += ["-s", serial]

        cmd += list(args)

        logger.info("ADB: %s", " ".join(cmd))

        return subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=check,
            timeout=timeout,
        )

    def check_adb(self) -> bool:
        """检查当前 ADB 设备是否在线。"""

        try:
            result = subprocess.run(
                ["adb", "devices"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5,
            )

            serial = self._get_serial()

            for line in result.stdout.splitlines():
                parts = line.split()

                if len(parts) == 2 and parts[1] == "device":
                    if serial is None or parts[0] == serial:
                        return True

            return False

        except Exception as e:
            logger.error("ADB 检查失败: %s", e)
            return False

    # =========================================================
    # 屏幕
    # =========================================================

    def wake_screen(self):
        """唤醒屏幕。"""

        self._adb(
            "shell",
            "input",
            "keyevent",
            "KEYCODE_WAKEUP",
        )

        time.sleep(1)

    def is_locked(self) -> bool:
        """判断 Android 是否处于锁屏状态。"""

        try:
            result = self._adb(
                "shell",
                "dumpsys",
                "window",
                check=False,
                timeout=10,
            )

            text = result.stdout

            return (
                "mDreamingLockscreen=true" in text
                or "mKeyguardShowing=true" in text
            )

        except Exception as e:
            logger.warning("无法判断锁屏状态: %s", e)

            # 无法确认时，为安全起见认为锁屏
            return True

    # =========================================================
    # 密码
    # =========================================================

    def get_pin(self) -> str:
        """
        使用 OpenSSL 解密锁屏密码。

        不打印密码内容。
        """

        if not os.path.isfile(self.pin_file):
            raise RuntimeError(
                f"找不到加密密码文件: {self.pin_file}"
            )

        if not os.path.isfile(self.key_file):
            raise RuntimeError(
                f"找不到加密密钥文件: {self.key_file}"
            )

        result = subprocess.run(
            [
                "openssl",
                "enc",
                "-d",
                "-aes-256-cbc",
                "-pbkdf2",
                "-iter",
                "200000",
                "-in",
                self.pin_file,
                "-pass",
                f"file:{self.key_file}",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "锁屏密码解密失败: "
                + result.stderr.decode(errors="replace")
            )

        pin = result.stdout.decode("utf-8").strip()

        if not pin:
            raise RuntimeError("解密得到的密码为空")

        if not pin.isdigit():
            raise RuntimeError(
                "当前自动解锁只支持纯数字锁屏密码"
            )

        return pin

    # =========================================================
    # 自动解锁
    # =========================================================

    def unlock(self) -> bool:
        """自动解锁 Android。"""

        logger.info("🔐 手机处于锁屏状态")

        pin = self.get_pin()

        logger.info(
            "🔑 已读取加密密码（%d 位）",
            len(pin),
        )

        # -----------------------------------------------------
        # 唤醒
        # -----------------------------------------------------

        logger.info("💡 唤醒屏幕")

        self.wake_screen()

        # -----------------------------------------------------
        # 再检查
        # -----------------------------------------------------

        if not self.is_locked():
            logger.info("✅ 手机已经解锁")
            return True

        # -----------------------------------------------------
        # 滑动锁屏
        # -----------------------------------------------------

        logger.info("👆 滑动锁屏")

        self._adb(
            "shell",
            "input",
            "swipe",
            str(self.swipe_x),
            str(self.swipe_start_y),
            str(self.swipe_x),
            str(self.swipe_end_y),
            str(self.swipe_duration),
        )

        time.sleep(0.8)

        # -----------------------------------------------------
        # 输入密码
        # -----------------------------------------------------

        logger.info("🔑 输入锁屏密码")

        self._adb(
            "shell",
            "input",
            "text",
            pin,
        )

        # -----------------------------------------------------
        # 提交
        # -----------------------------------------------------

        self._adb(
            "shell",
            "input",
            "keyevent",
            "KEYCODE_ENTER",
        )

        time.sleep(2)

        # -----------------------------------------------------
        # 验证
        # -----------------------------------------------------

        if self.is_locked():
            logger.error("❌ 自动解锁失败")
            return False

        logger.info("✅ 手机解锁成功")

        return True

    # =========================================================
    # 对外接口
    # =========================================================

    def ensure_ready(self) -> bool:
        """
        确保手机已经可以操作。

        ADB
          ↓
        唤醒
          ↓
        检查锁屏
          ↓
        自动解锁
        """

        if not self.check_adb():
            raise RuntimeError("ADB 设备未连接")

        # WAKEUP 不会主动熄屏
        self.wake_screen()

        if not self.is_locked():
            logger.info("📱 手机已解锁")
            return True

        return self.unlock()
