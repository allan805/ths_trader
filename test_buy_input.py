import time
import subprocess
import uiautomator2 as u2

SERIAL = "127.0.0.1:41373"
CODE = "118027"
PRICE = "88.677"
QUANTITY = "10"

d = u2.connect(SERIAL)

print("=" * 60)
print("测试：ADB 键盘输入股票代码 → 点击模拟买入")
print("=" * 60)

# 进入同花顺
d.app_start("com.hexin.plat.android")
time.sleep(2)

# 点击交易
if d(text="交易").exists:
    d(text="交易").click()
    time.sleep(2)

# 点击买入
if d(text="买入").exists:
    d(text="买入").click()
    time.sleep(1)

# 找股票代码输入框
code_input = d(resourceId="com.hexin.plat.android:id/auto_stockcode")

if not code_input.exists:
    print("❌ 找不到股票代码输入框")
    raise SystemExit(1)

print("[1] 找到股票代码输入框")

# 点击输入框
code_input.click()
time.sleep(0.3)

# 清空
code_input.clear_text()
time.sleep(0.2)

# 重点：不用 set_text()
# 使用 Android 真正的 input text
result = subprocess.run(
    [
        "adb", "-s", SERIAL,
        "shell", "input", "text", CODE
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

if result.returncode != 0:
    print("❌ ADB 输入失败")
    print(result.stderr)
    raise SystemExit(1)

print(f"[2] 已通过 Android 键盘输入：{CODE}")

# 给同花顺股票匹配时间
time.sleep(2)

# 读取实际 UI
actual_code = ""
stock_name = ""

try:
    actual_code = code_input.get_text().strip()
except Exception:
    pass

name_obj = d(resourceId="com.hexin.plat.android:id/stockname")

if name_obj.exists:
    try:
        stock_name = name_obj.get_text().strip()
    except Exception:
        pass

print(f"[3] 股票代码：{actual_code}")
print(f"[4] 股票名称：{stock_name}")

if stock_name == "股票名称" or not stock_name:
    print("❌ 同花顺仍然没有真正识别股票")
    print("不点击买入")
    d.screenshot("test_buy_input_failed.png")
    raise SystemExit(2)

print(f"✅ 股票识别成功：{actual_code} -> {stock_name}")

# 价格
price_input = d(className="android.widget.EditText", instance=1)

if price_input.exists:
    price_input.click()
    price_input.clear_text()
    price_input.set_text(PRICE)

# 数量
quantity_input = d(className="android.widget.EditText", instance=2)

if quantity_input.exists:
    quantity_input.click()
    quantity_input.clear_text()
    quantity_input.set_text(QUANTITY)

time.sleep(1)

print("[5] 价格：", price_input.get_text() if price_input.exists else "找不到")
print("[6] 数量：", quantity_input.get_text() if quantity_input.exists else "找不到")

# 最后确认模拟买入按钮
buy_button = d(text="买 入(模拟炒股)")

if not buy_button.exists:
    print("❌ 找不到「买 入(模拟炒股)」按钮")
    d.screenshot("test_buy_button_missing.png")
    raise SystemExit(3)

print("[7] 找到「买 入(模拟炒股)」")
print("[8] 点击模拟买入")

buy_button.click()

print("[9] 已点击「买 入(模拟炒股)」")
print("[10] 等待委托确认窗口...")
time.sleep(1)

confirm_button = d(text="确认买入")

if confirm_button.exists:
    print("[11] 找到「确认买入」")
    confirm_button.click()
    print("[12] 已点击「确认买入」")
else:
    print("❌ 没找到「确认买入」")
    d.screenshot("test_confirm_missing.png")
    raise SystemExit(4)

time.sleep(3)


# 读取弹窗/页面
texts = []

try:
    hierarchy = d.dump_hierarchy()
    import xml.etree.ElementTree as ET

    root = ET.fromstring(hierarchy)

    for node in root.iter():
        text = node.attrib.get("text", "").strip()
        if text:
            texts.append(text)
except Exception as e:
    print("读取 UI 失败：", e)

print()
print("=" * 60)
print("点击买入后的实际页面文字")
print("=" * 60)

for text in texts:
    print(text)

d.screenshot("test_buy_after_click.png")

# 特别检查几个关键结果
if "请输入股票代码" in texts:
    print()
    print("❌ 仍然是：请输入股票代码")
    print("说明 Android input text 仍没有触发股票选择")

elif any(x in texts for x in ["委托成功", "委托已报", "已报", "申报成功", "申报已报"]):
    print()
    print("✅ 检测到模拟委托成功/已报")

elif any(x in texts for x in ["资金不足", "可用资金不足", "数量不足", "委托失败", "下单失败"]):
    print()
    print("⚠️ 同花顺返回交易失败信息")
    print("这是实际交易页面返回的结果")

else:
    print()
    print("⚠️ 已点击模拟买入，但暂未识别到明确结果")
    print("请查看 test_buy_after_click.png")

print()
print("测试结束")
