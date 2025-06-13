import os
import re
from datetime import datetime

import pandas as pd

from src.business.db_operations.create_database import create_database_file
from src.business.db_operations.read_database import (
    read_excel_data,
    search_data_by_field,
)
from src.business.db_operations.update_row_database import update_excel_row

STOCK_FILE_PATH = "src/business/data/product_stock_data.xlsx"
CATEGORY_FILE_PATH = "src/business/data/category_data.xlsx"

SHEET_NAME = "ProductData"


def create_stock_product(data):
    # creamos un dataframe para crear un registro compatible con la tabla de pandas
    df_new_product = pd.DataFrame(data)
    # leemos el estado actual de la base de datos
    df_current_stock_data = read_excel_data(STOCK_FILE_PATH, SHEET_NAME, "")
    # combinamos los datos con el método concat
    df_combined_data = pd.concat([df_current_stock_data, df_new_product])
    # escribimos el archivo excel con los datos combinados
    df_combined_data.to_excel(STOCK_FILE_PATH, sheet_name=SHEET_NAME, index=False)
    return df_combined_data


def read_stock(item_code: str):
    # leer stock y devolver tabla de datos
    # si item_code es vacío retorna todos los items
    # si no retorna el item o mensaje nulo
    return read_excel_data(STOCK_FILE_PATH, SHEET_NAME, item_code)


def search_stock(field: str, value):
    return search_data_by_field(STOCK_FILE_PATH, SHEET_NAME, field, value)


def update_stock_product(updated_data):
    df_current_stock_data = read_excel_data(STOCK_FILE_PATH, SHEET_NAME, "")
    # busca el producto por item y actualiza el registro con los datos
    updated_row = update_excel_row(
        df_current_stock_data, STOCK_FILE_PATH, SHEET_NAME, updated_data
    )
    return updated_row


def delete_stock_product(item_code: str):
    # busca el producto por item y lo elimina
    df_current_stock_data = read_excel_data(STOCK_FILE_PATH, SHEET_NAME, "")
    item_index = df_current_stock_data[
        df_current_stock_data["item_code"] == item_code
    ].index

    deleted_db = df_current_stock_data.drop(item_index)
    deleted_db.to_excel(STOCK_FILE_PATH, sheet_name=SHEET_NAME, index=False)

    return deleted_db


def create_item_code(category_name: str):
    item_letters = ""
    for letters in category_name.split():
        item_letters += letters[0]

    item_letters = item_letters.upper()

    # leer datos tabla actual
    filtered_data = search_data_by_field(
        STOCK_FILE_PATH, SHEET_NAME, "category", category_name
    )

    if not filtered_data.empty:
        filtered_category_item_codes = filtered_data["item_code"]

        # se usa iloc[-1] para traer la última fila de la tabla
        last_item_code = filtered_category_item_codes.iloc[-1]

        consecutive_num = re.findall(r"\d+", last_item_code)[0]

        new_consecutive = int(consecutive_num) + 1
        new_item_code = f"{new_consecutive}{item_letters}"
        return new_item_code
    else:
        return f"1{item_letters}"


def initialiaze_operations():
    # validamos que el archivo exista
    if os.path.exists(STOCK_FILE_PATH):
        return "La base de datos ya ha sido creada"
    else:
        # si no existe lo creamos de 0
        print(f"El archivo {STOCK_FILE_PATH} no existe")
        initial_product_stock_data = {
            "item_code": ["1AYB", "2AYB", "3AYB", "4AYB"],
            "category": [
                "Alimentos y bebidas",
                "Alimentos y bebidas",
                "Alimentos y bebidas",
                "Alimentos y bebidas",
            ],
            "product_name": [
                "Arroz Diana x 1 Kilogramo",
                "Aceite de oliva x 1 Litro",
                "Leche Colanta x 1 litro",
                "Pan Integral Unidad",
            ],
            "quantity": [7, 3, 8, 4],
            "purchase_price": [2500, 8000, 2500, 1000],
            "sale_price": [3500, 12000, 3500, 1500],
            "creation_date": [
                datetime.now(),
                datetime.now(),
                datetime.now(),
                datetime.now(),
            ],
        }

        initial_category_data = {
            "id": [0, 1, 2, 3, 4, 5, 6],
            "name": [
                "Alimentos y bebidas",
                "Aseo personal",
                "Dulcería",
                "Limpieza",
                "Papelería",
                "Medicamentos",
                "Otros",
            ],
        }

        create_database_file(
            STOCK_FILE_PATH, initial_product_stock_data, initial_category_data
        )
        print("La base de datos se ha creado")
