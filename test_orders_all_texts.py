from ths.trader import ThsTrader
import xml.etree.ElementTree as ET


def main():
    trader = ThsTrader()

    try:
        trader.connect()

        print("=" * 70)
        print("检查同花顺「当日委托」全部文本节点")
        print("只读操作，不下单")
        print("=" * 70)

        if not trader.go_to_trade():
            print("❌ 无法进入交易页面")
            return

        print("\n[1] 点击 查询")

        if not trader.click_by_text("查询", timeout=5):
            print("❌ 找不到 查询")
            return

        trader.wait(2)

        print("\n[2] 点击 当日委托")

        if not trader.click_by_text("当日委托", timeout=5):
            print("❌ 找不到 当日委托")
            return

        trader.wait(3)

        print("\n[3] 保存截图")

        screenshot = trader.screenshot(
            "orders_today_all_texts.png"
        )

        print(f"截图: {screenshot}")

        print("\n[4] 获取 XML")

        hierarchy = trader.d.dump_hierarchy()

        xml_path = "ths/screenshots/orders_all_texts.xml"

        with open(
            xml_path,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(hierarchy)

        print(f"XML: {xml_path}")

        root = ET.fromstring(hierarchy)

        print("\n" + "=" * 70)
        print("所有非空 text / content-desc / hint 节点")
        print("=" * 70)

        count = 0

        for node in root.iter():

            text = node.attrib.get(
                "text",
                ""
            ).strip()

            desc = node.attrib.get(
                "content-desc",
                ""
            ).strip()

            hint = node.attrib.get(
                "hint",
                ""
            ).strip()

            if not text and not desc and not hint:
                continue

            count += 1

            print("\nNODE", count)

            print(
                "class        =",
                repr(node.attrib.get("class", ""))
            )

            print(
                "resource-id  =",
                repr(node.attrib.get("resource-id", ""))
            )

            print(
                "text         =",
                repr(text)
            )

            print(
                "content-desc =",
                repr(desc)
            )

            print(
                "hint         =",
                repr(hint)
            )

            print(
                "bounds       =",
                repr(node.attrib.get("bounds", ""))
            )

        print("\n" + "=" * 70)
        print(
            f"共发现 {count} 个非空文本相关节点"
        )
        print("=" * 70)

    finally:

        print("\n[5] 尝试返回交易主页面")

        try:
            trader.back_to_trade_main()
        except Exception as e:
            print(
                f"⚠️ 返回交易页面失败: {e}"
            )


if __name__ == "__main__":
    main()
