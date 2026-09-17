from ths.trader import ThsTrader
import time

CODE = "118027"
PRICE = "88.677"
QUANTITY = "10"

print("=" * 60)
print("测试：完整填写买入表单")
print("不会点击最终买入按钮，不会产生真实委托")
print("=" * 60)

trader = ThsTrader()

try:
    # 1. 进入交易页面
    print("\n[1] 进入交易页面")

    if not trader.go_to_trade():
        raise RuntimeError("无法进入交易页面")

    # 2. 点击买入
    print("\n[2] 点击买入")

    if not trader.click_by_text("买入", timeout=5):
        raise RuntimeError("无法点击买入")

    trader.wait(1)

    # 3. 找代码输入框
    print("\n[3] 输入股票代码")

    code_input = trader.d(
        resourceId="com.hexin.plat.android:id/auto_stockcode"
    )

    if not code_input.exists:
        raise RuntimeError("找不到 auto_stockcode")

    code_input.click()

    if not trader.input_text(CODE, 0):
        raise RuntimeError("代码输入失败")

    trader.wait(1)

    # 4. 验证股票
    print("\n[4] 验证股票识别")

    if not trader._verify_stock_selection(CODE):
        raise RuntimeError("股票识别失败")

    # 5. 输入价格
    print("\n[5] 输入价格")

    if not trader.input_text(PRICE, 1):
        raise RuntimeError("价格输入失败")

    # 6. 输入数量
    print("\n[6] 输入数量")

    if not trader.input_text(QUANTITY, 2):
        raise RuntimeError("数量输入失败")

    trader.wait(0.5)

    # 7. 读取当前三个输入框
    print("\n[7] 读取最终表单")

    for i in range(3):
        obj = trader.d(
            className="android.widget.EditText",
            instance=i
        )

        if obj.exists:
            print(
                f"instance={i}  "
                f"text={obj.get_text()!r}"
            )
        else:
            print(f"instance={i}  不存在")

    # 8. 检查最终按钮
    print("\n[8] 检查最终买入按钮")

    buy_button = trader.d(text="买 入")

    print(f"「买 入」按钮存在: {buy_button.exists}")

    if buy_button.exists:
        print(f"可点击: {buy_button.info.get('clickable')}")
        print(f"bounds: {buy_button.info.get('bounds')}")

    # 9. 截图
    print("\n[9] 保存截图")

    screenshot = trader.screenshot(
        "test_order_form_before_submit.png"
    )

    print(f"截图: {screenshot}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("⚠️ 没有点击「买 入」")
    print("⚠️ 没有产生委托")
    print("=" * 60)

finally:
    print("\n[10] 返回交易页面")

    try:
        trader.back_from_buy()
    except Exception as e:
        print(f"返回失败: {e}")

    print("\n测试结束")
