from textual.message import Message


class StockDeleteRequestMessage(Message):
    """Message to request deletion of a stock item with confirmation"""
    def __init__(self, item_code: str, product_name: str):
        self.item_code = item_code
        self.product_name = product_name
        super().__init__()


class StockDeleteConfirmedMessage(Message):
    """Message sent when user confirms deletion"""
    def __init__(self, item_code: str):
        self.item_code = item_code
        super().__init__() 