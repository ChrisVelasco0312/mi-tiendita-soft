from textual.message import Message

class StockUpdateMessage(Message):
    def __init__(self, payload):
        self.payload = payload
        super().__init__()
