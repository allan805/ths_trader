import time
import uiautomator2 as u2
from ths.trader import ThsTrader

CODE = "118027"
PRICE = "88.677"
QUANTITY = "10"


def main():
    print("=" * 60)
    print("安全诊断：执行到第一次「买 入」")
    print("=" * 60)

    trader = ThsTrader()
    trader.d = u2.connect("127.0.0.1:41373")

    print("\n[1] 进入交易页面")
    if not trader.go_to_trade():
        print("❌ 无法进入交易页面")
        return

    print("[OK] 已进入交易页面")

    print("\n[2] 点击「买入」")
    if not trader.click_by_text("买入", timeout=5):
        print("❌ 找不到「买入」")
        return

    trader.wait(1)

    print("[OK] 已进入买入页面")

    print("\n[3] 输入股票代码")
    if not trader.input_text(CODE, 0):
        print("❌ 股票代码输入失败")
        return

    if not trader._verify_stock_selection(CODE, timeout=5):
        print("❌ 股票识别失败")
        return

    print("[OK] 股票识别成功")

    print("\n[4] 输入价格")
    if not trader.input_text(PRICE, 1):
        print("❌ 价格输入失败")
        return

    print("[OK] 价格输入成功")

    print("\n[5] 输入数量")
    if not trader.input_text(QUANTITY, 2):
        print("❌ 数量输入失败")
        return

    print("[OK] 数量输入成功")

    time.sleep(1)

    print("\n" + "=" * 60)
    print("当前页面所有可见文字")
    print("=" * 60)

    xml = trader.d.dump_hierarchy()

    import xml.etree.ElementTree as ET

    root = ET.fromstring(xml)

    for node in root.iter():
        text = node.attrib.get("text", "").strip()
        desc = node.attrib.get("content-desc", "").strip()
        resource = node.attrib.get("resource-id", "").strip()
        cls = node.attrib.get("class", "").strip()
        clickable = node.attrib.get("clickable", "").strip()
        enabled = node.attrib.get("enabled", "").strip()

        if text or desc:
            print(
                f"text={text!r} "
                f"desc={desc!r} "
                f"class={cls} "
                f"clickable={clickable} "
                f"enabled={enabled} "
                f"id={resource}"
            )

    print("\n" + "=" * 60)
    print("所有可能的「买入」节点")
    print("=" * 60)

    found = False

    for node in root.iter():
        text = node.attrib.get("text", "").strip()
        desc = node.attrib.get("content-desc", "").strip()

        if "买" in text or "买" in desc:
            found = True
            print(node.attrib)

    if not found:
        print("❌ XML 中没有找到包含「买」的节点")

    path = trader.screenshot("buy_before_confirm_debug.png")
    print("\n截图:", path)

    print("\n" + "=" * 60)
    print("⏸ 当前停留在买入页面")
    print("⏸ 没有点击任何买入按钮")
    print("=" * 60)

    input("\n按 Enter 返回...")

    trader.back()
    time.sleep(0.5)


if __name__ == "__main__":
    main()
