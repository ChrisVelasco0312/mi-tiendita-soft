import os
from datetime import datetime

from src.business.db_operations.create_database import create_database_file
from src.business.db_operations.read_database import read_excel_data

FILE_PATH = "src/business/data/product_stock_data.xlsx"


def initialiaze_operations():
    # validamos que el archivo exista
    if os.path.exists(FILE_PATH):
        print(f"El archivo {FILE_PATH} existe")
        current_stock_data = read_excel_data(FILE_PATH, "ProductData")
        print(current_stock_data)
    else:
        # si no existe lo creamos de 0
        print(f"El archivo {FILE_PATH} no existe")
        initial_product_stock_data = {
            "item_code": ["AB_001"],
            "category": ["Alimento y bebidas"],
            "product_name": ["Arroz Diana x 1 Kilogramo"],
            "quantity": [7],
            "purchase_price": [2500],
            "sale_price": [3500],
            "creation_date": [datetime.now()],
        }
        create_database_file(FILE_PATH, initial_product_stock_data)
