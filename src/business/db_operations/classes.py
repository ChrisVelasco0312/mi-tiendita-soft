from dataclasses import dataclass
from datetime import date
from typing import List, TypedDict


class ProductData(TypedDict):
    item_code: List[str]
    category: List[str]
    product_name: List[str]
    quantity: List[float]
    purchase_price: List[int]
    sale_price: List[int]
    creation_date: List[date]


class Product(TypedDict):
    item_code: str
    category: str
    product_name: str
    quantity: float
    purchase_price: int
    sale_price: int
    creation_date: date
