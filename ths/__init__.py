class ThsTrader:
    def __init__(self):
        self.device_serial = config.DEVICE_SERIAL
        self.d = None
        self.package = config.THS_PACKAGE
        self.trade_mode: TradeMode = "real"
        self.save_screenshot: bool = True

        # Android 手机状态控制
        self.phone = PhoneController()

        self.connect()
