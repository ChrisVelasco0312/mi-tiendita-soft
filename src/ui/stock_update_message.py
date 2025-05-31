from textual.message import Message

class StockUpdateMessage(Message):
    def __init__(self, payload):
        self.payload = payload
        super().__init__()

class StockDataRefreshMessage(Message):
    """Message to notify that stock data has been updated and views should refresh"""
    def __init__(self):
        super().__init__()
