import time
import uiautomator2 as u2

SERIAL = "127.0.0.1:41373"
CODE = "118027"
PRICE = "88.677"
QUANTITY = "10"

d = u2.connect(SERIAL)

print("=" * 50)
print("安全测试：股票代码 / 价格 / 数量输入")
print("不会点击买入按钮")
print("=" * 50)

# 1. 确认当前进入同花顺交易页面
print("[1] 当前页面")
print("package:", d.app_current())

# 2. 找股票代码输入框
print("[2] 查找股票代码输入框")

code_input = d(
    resourceId="com.hexin.plat.android:id/auto_stockcode"
)

if not code_input.exists:
    print("❌ 找不到股票代码输入框")
    raise SystemExit(1)

print("✅ 找到股票代码输入框")

# 3. 使用 Android ADB 键盘输入股票代码
print("[3] 输入股票代码:", CODE)

code_input.click()
time.sleep(0.2)
code_input.clear_text()
time.sleep(0.2)

import subprocess

result = subprocess.run(
    [
        "adb",
        "-s",
        SERIAL,
        "shell",
        "input",
        "text",
        CODE
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    timeout=5
)

if result.returncode != 0:
    print("❌ ADB 输入失败")
    print(result.stderr)
    raise SystemExit(1)

time.sleep(1)

# 4. 检查股票识别
actual_code = code_input.get_text()
name_input = d(
    resourceId="com.hexin.plat.android:id/stockname"
)

stock_name = ""
if name_input.exists:
    stock_name = name_input.get_text()

print("[4] 股票代码:", actual_code)
print("[4] 股票名称:", stock_name)

if actual_code != CODE:
    print("❌ 股票代码不正确")
    raise SystemExit(1)

if not stock_name or stock_name == "股票名称":
    print("❌ 同花顺没有真正识别股票")
    raise SystemExit(1)

print(f"✅ 股票识别成功：{CODE} -> {stock_name}")

# 5. 输入价格
print("[5] 输入价格:", PRICE)

price_input = d(
    className="android.widget.EditText",
    instance=1
)

if not price_input.exists:
    print("❌ 找不到价格输入框")
    raise SystemExit(1)

price_input.click()
price_input.clear_text()
price_input.set_text(PRICE)

# 6. 输入数量
print("[6] 输入数量:", QUANTITY)

quantity_input = d(
    className="android.widget.EditText",
    instance=2
)

if not quantity_input.exists:
    print("❌ 找不到数量输入框")
    raise SystemExit(1)

quantity_input.click()
quantity_input.clear_text()
quantity_input.set_text(QUANTITY)

time.sleep(0.5)

# 7. 最终检查
print("[7] 最终表单")

print("股票代码:", code_input.get_text())
print("股票名称:", stock_name)
print("价格:", price_input.get_text())
print("数量:", quantity_input.get_text())

buy_button = d(text="买 入")

print("买入按钮存在:", buy_button.exists)

print()
print("=" * 50)
print("✅ 安全测试完成")
print("⚠️ 本测试没有点击买入按钮")
print("=" * 50)
