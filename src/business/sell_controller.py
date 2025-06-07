import os
import pandas as pd
from datetime import datetime
from src.business.db_operations.read_database import read_excel_data
from src.business.db_operations.update_sell_row import update_excel_row

# from src.business.db_operations.search_database import search_data_by_field
from src.business.db_operations.create_sell_database import create_database_file


FILE_PATH = "src/business/data/sell_data.xlsx"
SHEET_NAME = "SellData"

def read_sell_data():
    return read_excel_data(FILE_PATH, SHEET_NAME, "")

def create_sell(data):
    df_current_sell_data = read_sell_data()
    last_id = df_current_sell_data.iloc[-1]["id"]
    data[0]["id"] = last_id + 1
    data[0]["date"] = datetime.now()
    df_new_sell = pd.DataFrame(data)
    df_current_sell_data = read_sell_data()
    df_combined_data = pd.concat([df_current_sell_data, df_new_sell])
    df_combined_data.to_excel(FILE_PATH, sheet_name=SHEET_NAME, index=False)
    return df_combined_data

def update_sell(updated_data):
    df_current_sell_data = read_sell_data()
    updated_row = update_excel_row(
        df_current_sell_data, FILE_PATH, SHEET_NAME, updated_data
    )
    return updated_row


def initialize_sell_db():
    if os.path.exists(FILE_PATH):
        return "La base de datos ya ha sido creada"
    else:
        initial_sell_data = {
            "id": [],
            "items": [],
            "quantities": [],
            "total": [],
            "date": []
        }
        create_database_file(initial_sell_data)

