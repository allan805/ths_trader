import time
from ths.trader import ThsTrader

CODE = "118027"

print("=" * 60)
print("股票搜索诊断")
print(f"股票代码：{CODE}")
print("注意：本测试不会提交任何买入/卖出订单")
print("=" * 60)

trader = ThsTrader()

print("[1] 进入交易页面")
if not trader.go_to_trade():
    raise RuntimeError("无法进入交易页面")

print("[2] 点击买入")
if not trader.click_by_text("买入", timeout=5):
    raise RuntimeError("找不到“买入”按钮")

trader.wait(2)

print("[3] 点击股票代码输入框")
if not trader.click_by_text("股票代码/简拼", timeout=5):
    raise RuntimeError("找不到“股票代码/简拼”输入框")

print(f"[4] 输入股票代码：{CODE}")
trader.input_text(CODE, 0)

trader.wait(2)

print("[5] 读取搜索前页面")
before = trader._get_visible_texts()
print("当前文本：")
for i, text in enumerate(before):
    print(f"  [{i}] {text}")

print("[6] 点击搜索")
# 这里仅触发股票搜索，不选择搜索结果
if not trader.click_by_text("搜索", timeout=3):
    print("没有找到“搜索”按钮，继续读取当前页面")

trader.wait(3)

print("[7] 搜索结果页面文本")
texts = trader._get_visible_texts()

for i, text in enumerate(texts):
    print(f"  [{i}] {text}")

print("[8] 保存 UI XML")
path = trader.screenshot("stock_search_test.png")
print(f"截图：{path}")

dump = trader.d.dump_hierarchy()
xml_path = "ths/screenshots/stock_search_test.xml"

with open(xml_path, "w", encoding="utf-8") as f:
    f.write(dump)

print(f"XML：{xml_path}")

print()
print("=" * 60)
print("诊断完成")
print("没有点击搜索结果")
print("没有提交买入")
print("=" * 60)
