import os
from datetime import datetime

import pandas as pd

from src.business.db_operations.create_database import create_database_file
from src.business.db_operations.read_database import read_excel_data
from src.business.db_operations.update_row_database import update_excel_row

FILE_PATH = "src/business/data/product_stock_data.xlsx"
SHEET_NAME = "ProductData"


def create_stock_product(data):
    # creamos un dataframe para crear un registro compatible con la tabla de pandas
    df_new_product = pd.DataFrame(data)
    # leemos el estado actual de la base de datos
    df_current_stock_data = read_excel_data(FILE_PATH, SHEET_NAME, "")
    # combinamos los datos con el método concat
    df_combined_data = pd.concat([df_current_stock_data, df_new_product])
    # escribimos el archivo excel con los datos combinados
    df_combined_data.to_excel(FILE_PATH, sheet_name=SHEET_NAME, index=False)
    return df_combined_data


def read_stock(item_code: str):
    # leer stock y devolver tabla de datos
    # si item_code es vacío retorna todos los items
    # si no retorna el item o mensaje nulo
    return read_excel_data(FILE_PATH, SHEET_NAME, item_code)


def update_stock_product(updated_data):
    df_current_stock_data = read_excel_data(FILE_PATH, SHEET_NAME, "")
    # busca el producto por item y actualiza el registro con los datos
    updated_row = update_excel_row(
        df_current_stock_data, FILE_PATH, SHEET_NAME, updated_data
    )
    return updated_row


def delete_stock_product(item_code: str):
    # busca el producto por item y lo elimina
    df_current_stock_data = read_excel_data(FILE_PATH, SHEET_NAME, "")
    item_index = df_current_stock_data[
        df_current_stock_data["item_code"] == item_code
    ].index

    deleted_db = df_current_stock_data.drop(item_index)
    deleted_db.to_excel(FILE_PATH, sheet_name=SHEET_NAME, index=False)

    return deleted_db


def initialiaze_operations():
    # validamos que el archivo exista
    if os.path.exists(FILE_PATH):
        print(f"El archivo {FILE_PATH} existe")
        current_stock_data = read_excel_data(FILE_PATH, "ProductData")
        # se preparan los datos a actualizar de 1 sola columna
        updated_product_stock_data = {
            # El item_code solo se usa para encontrar el registro
            "item_code": "AB_001",
            "category": "Alimento y bebidas",
            "product_name": "Arroz Doña Nieves 1k",
            "quantity": 20,
            "purchase_price": 3500,
            "sale_price": 4500,
            "creation_date": datetime.now(),
        }
        updated_stock_data = update_excel_row(
            current_stock_data,
            FILE_PATH,
            "ProductData",
            updated_product_stock_data,
        )
        print(updated_stock_data)
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
