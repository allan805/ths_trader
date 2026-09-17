from ths.trader import ThsTrader
import time

print("=" * 60)
print("测试：go_to_trade() 导航")
print("不会买入、不会卖出、不会输入股票代码")
print("=" * 60)

trader = ThsTrader()

start = time.time()

try:
    result = trader.go_to_trade()
    elapsed = time.time() - start

    print()
    print("=" * 60)
    print(f"go_to_trade() 返回: {result}")
    print(f"总耗时: {elapsed:.2f} 秒")
    print(f"_trade_ready: {trader._trade_ready}")
    print("=" * 60)

    if result:
        print("✅ 交易页面导航成功")
    else:
        print("❌ 交易页面导航失败")

finally:
    print("\n测试结束")
