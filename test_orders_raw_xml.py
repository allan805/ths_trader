from ths.trader import ThsTrader
import xml.etree.ElementTree as ET
import re

trader = ThsTrader()

print("=" * 70)
print("检查同花顺「当日委托」原始 XML")
print("只读操作，不下单")
print("=" * 70)

try:
    if not trader.go_to_trade():
        raise RuntimeError("无法进入交易页面")

    if not trader.click_by_text("查询", timeout=5):
        if not trader.click_by_text("委托查询", timeout=3):
            raise RuntimeError("无法找到查询按钮")

    trader.wait(2)

    if not trader.click_by_text("当日委托", timeout=3):
        print("⚠️ 未找到「当日委托」，继续检查当前页面")

    trader.wait(2)

    hierarchy = trader.d.dump_hierarchy()

    path = "ths/screenshots/orders_raw.xml"

    with open(path, "w", encoding="utf-8") as f:
        f.write(hierarchy)

    print(f"\n✅ XML 已保存：{path}")

    root = ET.fromstring(hierarchy)

    print("\n" + "=" * 70)
    print("所有包含数字/代码特征的节点")
    print("=" * 70)

    patterns = re.compile(
        r"^\d{6}$|^\d{5,6}$|"
        r"\d{6,8}"
    )

    found = 0

    for node in root.iter():
        text = node.attrib.get("text", "").strip()
        desc = node.attrib.get("content-desc", "").strip()
        rid = node.attrib.get("resource-id", "").strip()
        hint = node.attrib.get("hint", "").strip()
        cls = node.attrib.get("class", "").strip()

        combined = " ".join([text, desc, rid, hint])

        if (
            patterns.search(text)
            or patterns.search(desc)
            or "code" in combined.lower()
            or "stock" in combined.lower()
            or "证券" in combined
            or "股票" in combined
        ):
            print("\nNODE")
            print(f"  text         = {text!r}")
            print(f"  content-desc = {desc!r}")
            print(f"  resource-id  = {rid!r}")
            print(f"  hint         = {hint!r}")
            print(f"  class        = {cls!r}")
            found += 1

    print("\n" + "=" * 70)
    print(f"共发现 {found} 个疑似代码/股票相关节点")
    print("=" * 70)

finally:
    try:
        trader.back_to_trade_main()
    except Exception:
        pass
