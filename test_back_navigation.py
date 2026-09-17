from ths.trader import ThsTrader
import time

print("=" * 60)
print("测试：买入页面 → Android Back → 交易主页面")
print("注意：不会输入股票代码，不会输入价格，不会下单")
print("=" * 60)

trader = ThsTrader()

try:
    print("\n[1] 进入交易页面")
    if not trader.go_to_trade():
        raise RuntimeError("无法进入交易页面")

    print("[OK] 已进入交易主页面")

    print("\n[2] 点击买入")
    if not trader.click_by_text("买入", timeout=5):
        raise RuntimeError("无法点击买入")

    trader.wait(1)

    print("[OK] 已进入买入页面")

    print("\n[3] 测试 back_from_buy()")

    start = time.time()

    result = trader.back_from_buy()

    elapsed = time.time() - start

    print()
    print("=" * 60)
    print(f"返回结果: {result}")
    print(f"耗时: {elapsed:.2f} 秒")
    print("=" * 60)

    if result:
        print("✅ 买入页面返回交易主页面成功")
    else:
        print("❌ 返回失败")

finally:
    print("\n测试结束")
