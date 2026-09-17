from ths.trader import Trader

trader = Trader()
trader.connect()

try:
    print("=" * 70)
    print("检查「当日委托」页面所有可见 TextView")
    print("只读，不下单")
    print("=" * 70)

    if not trader.go_to_trade():
        raise RuntimeError("无法进入交易页面")

    if not trader.click_by_text("查询", timeout=5):
        raise RuntimeError("无法点击查询")

    trader.wait(2)

    if not trader.click_by_text("当日委托", timeout=5):
        raise RuntimeError("无法点击当日委托")

    trader.wait(3)

    trader.screenshot("orders_all_text.png")

    print("\n" + "=" * 70)
    print("所有 TextView")
    print("=" * 70)

    elements = trader.d(
        className="android.widget.TextView"
    )

    count = elements.count

    print(f"\nTextView 总数: {count}\n")

    for i in range(count):
        try:
            elem = elements[i]

            text = elem.get_text()

            info = elem.info

            print("-" * 70)
            print(f"index       : {i}")
            print(f"text        : {repr(text)}")
            print(f"resource-id : {info.get('resourceName')}")
            print(f"bounds      : {info.get('bounds')}")

        except Exception as e:
            print(f"index={i} ERROR: {e}")

    print("\n" + "=" * 70)
    print("检查结束")
    print("=" * 70)

finally:
    try:
        trader.back_to_trade_main()
    except Exception:
        pass
