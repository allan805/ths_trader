from ths.trader import ThsTrader
import time

print("=" * 60)
print("测试：买入页面三个 EditText 的实际顺序")
print("不会点击最终买入按钮")
print("=" * 60)

trader = ThsTrader()

try:
    if not trader.go_to_trade():
        raise RuntimeError("无法进入交易页面")

    print("\n[1] 点击买入")

    if not trader.click_by_text("买入", timeout=5):
        raise RuntimeError("无法点击买入")

    trader.wait(1)

    print("\n[2] 当前 EditText")

    for i in range(10):
        try:
            obj = trader.d(
                className="android.widget.EditText",
                instance=i
            )

            if not obj.exists:
                continue

            print(
                f"instance={i}"
                f"  text={obj.get_text()!r}"
                f"  hint={obj.info.get('hint')!r}"
                f"  resource-id={obj.info.get('resourceName')!r}"
            )

        except Exception as e:
            print(f"instance={i}  ERROR: {e}")

    print("\n[3] 测试结束，不输入任何东西")

finally:
    try:
        trader.back_from_buy()
    except Exception as e:
        print(f"返回交易页面失败: {e}")

print("\n完成")
