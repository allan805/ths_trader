# test_stock_verify.py
"""
同花顺股票/转债代码识别测试

测试流程：
1. 连接同花顺
2. 进入交易页面
3. 点击“买入”
4. 输入股票/转债代码
5. 调用 ThsTrader._verify_stock_selection()
6. 输出识别结果
7. 返回交易主页面

安全说明：
- 不输入价格
- 不输入数量
- 不点击最终“买入”按钮
- 不会提交真实委托
"""

import sys
import time
import logging

from ths.trader import ThsTrader


# ============================================================
# 日志
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ============================================================
# 测试参数
# ============================================================

TEST_CODE = "118027"


# ============================================================
# 主测试
# ============================================================

def main():
    print("=" * 60)
    print("同花顺股票/转债代码识别测试")
    print("=" * 60)
    print(f"测试代码：{TEST_CODE}")
    print()
    print("⚠️ 安全模式：")
    print("  不输入价格")
    print("  不输入数量")
    print("  不点击最终买入按钮")
    print("  不提交任何真实委托")
    print("=" * 60)

    trader = None

    try:
        # ----------------------------------------------------
        # 1. 创建交易器
        # ----------------------------------------------------
        print("\n[1] 创建 ThsTrader")

        trader = ThsTrader()

        if trader.d is None:
            raise RuntimeError("uiautomator2 设备连接失败")

        print("[OK] 同花顺控制器已经连接")

        # ----------------------------------------------------
        # 2. 进入交易页面
        # ----------------------------------------------------
        print("\n[2] 进入交易页面")

        if not trader.go_to_trade():
            raise RuntimeError("无法进入交易页面")

        print("[OK] 已进入交易页面")

        # ----------------------------------------------------
        # 3. 点击买入
        # ----------------------------------------------------
        print("\n[3] 点击“买入”")

        clicked = trader.click_by_text(
            "买入",
            timeout=5
        )

        if not clicked:
            clicked = trader.click_by_xpath(
                '//*[@text="买入"]'
            )

        if not clicked:
            raise RuntimeError("无法点击“买入”")

        trader.wait(1)

        print("[OK] 已进入买入页面")

        # ----------------------------------------------------
        # 4. 找到股票代码输入框
        # ----------------------------------------------------
        print("\n[4] 找到股票代码输入框")

        # 当前同花顺真实 UI：
        # resource-id = com.hexin.plat.android:id/auto_stockcode
        # hint       = 股票代码/简拼
        #
        # “股票代码/简拼”是 hint，不是 text，
        # 因此不能使用 click_by_text() 查找。

        code_input = trader.d(
            resourceId=(
                "com.hexin.plat.android:id/"
                "auto_stockcode"
            )
        )

        if not code_input.exists:
            raise RuntimeError(
                "无法找到股票代码输入框: "
                "com.hexin.plat.android:id/auto_stockcode"
            )

        try:
            code_input.click()
        except Exception as e:
            raise RuntimeError(
                f"无法点击股票代码输入框: {e}"
            )

        print(
            "[OK] 已通过 resource-id 定位 "
            "auto_stockcode"
        )

        trader.wait(0.5)

        print("[OK] 已定位股票代码输入框")

        # ----------------------------------------------------
        # 5. 输入代码
        # ----------------------------------------------------
        print(f"\n[5] 输入代码：{TEST_CODE}")

        if not trader.input_text(TEST_CODE, 0):
            raise RuntimeError(
                "股票代码输入失败"
            )

        print("[OK] 代码已经输入")

        # 给同花顺一点时间自动匹配
        print("\n[6] 等待同花顺自动识别")

        time.sleep(1)

        # ----------------------------------------------------
        # 6. 读取真实 UI
        # ----------------------------------------------------
        print("\n[7] 读取真实 UI")

        code_obj = trader.d(
            resourceId=(
                "com.hexin.plat.android:id/"
                "auto_stockcode"
            )
        )

        name_obj = trader.d(
            resourceId=(
                "com.hexin.plat.android:id/"
                "stockname"
            )
        )

        actual_code = ""
        stock_name = ""

        if code_obj.exists:
            actual_code = (
                code_obj.get_text() or ""
            ).strip()

        if name_obj.exists:
            stock_name = (
                name_obj.get_text() or ""
            ).strip()

        print("-" * 60)
        print(f"输入代码     : {TEST_CODE}")
        print(f"UI代码       : {actual_code}")
        print(f"UI股票名称   : {stock_name}")
        print("-" * 60)

        # ----------------------------------------------------
        # 8. 调用正式验证函数
        # ----------------------------------------------------
        print("\n[8] 调用 _verify_stock_selection()")

        verified = trader._verify_stock_selection(
            TEST_CODE,
            timeout=5
        )

        print()

        if verified:
            print("=" * 60)
            print("✅ 股票代码识别测试成功")
            print("=" * 60)
            print(f"代码：{actual_code}")
            print(f"名称：{stock_name}")
            print()
            print("验证条件：")
            print("  ✓ auto_stockcode 存在")
            print("  ✓ 代码与输入完全一致")
            print("  ✓ stockname 存在")
            print("  ✓ 股票名称非空")
            print()
            print("⚠️ 本次没有提交任何交易委托")
            print("=" * 60)
        else:
            print("=" * 60)
            print("❌ 股票代码识别测试失败")
            print("=" * 60)
            print(f"期望代码：{TEST_CODE}")
            print(f"实际代码：{actual_code}")
            print(f"股票名称：{stock_name}")
            print()
            print("⚠️ 本次没有提交任何交易委托")
            print("=" * 60)

            return 1

        # ----------------------------------------------------
        # 9. 返回交易主页面
        # ----------------------------------------------------
        print("\n[9] 返回交易主页面")

        try:
            if trader.back_from_buy():
                print("[OK] 已返回交易页面")
            else:
                print("[WARN] 返回交易页面失败")
        except Exception as e:
            print(f"[WARN] 返回交易页面异常：{e}")

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断测试")
        return 130

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ 测试失败")
        print("=" * 60)
        print(f"错误：{e}")
        print("=" * 60)

        logger.exception("测试异常")

        # 出错后尽量返回交易页面
        if trader is not None:
            try:
                trader.back_from_buy()
            except Exception:
                pass

        return 1


# ============================================================
# 程序入口
# ============================================================

if __name__ == "__main__":
    sys.exit(main())
