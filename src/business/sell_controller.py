import os
from datetime import datetime

import pandas as pd

# from src.business.db_operations.search_database import search_data_by_field
from src.business.db_operations.create_sell_database import create_database_file
from src.business.db_operations.read_database import read_excel_data
from src.business.db_operations.update_sell_row import update_excel_row

FILE_PATH = "src/business/data/sell_data.xlsx"
SHEET_NAME = "SellData"


def read_sell_data():
    return read_excel_data(FILE_PATH, SHEET_NAME, "")


def create_sell(data):
    df_current_sell_data = read_sell_data()
    
    # Handle the case when database is empty (first sale)
    if df_current_sell_data.empty:
        last_id = 0  # Start with ID 0, so first sale will be ID 1
    else:
        last_id = df_current_sell_data.iloc[-1]["id"]
    
    data[0]["id"] = last_id + 1
    data[0]["date"] = datetime.now()
    df_new_sell = pd.DataFrame(data)
    df_current_sell_data = read_sell_data()
    df_combined_data = pd.concat([df_current_sell_data, df_new_sell])
    
    # Convert items and quantities columns to string to prevent Excel auto-formatting
    df_combined_data["items"] = df_combined_data["items"].astype(str)
    df_combined_data["quantities"] = df_combined_data["quantities"].astype(str)
    
    # Use xlsxwriter engine to have more control over formatting
    try:
        with pd.ExcelWriter(FILE_PATH, engine='xlsxwriter') as writer:
            df_combined_data.to_excel(writer, sheet_name=SHEET_NAME, index=False)
            
            # Get the xlsxwriter workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets[SHEET_NAME]
            
            # Define a text format to prevent Excel from auto-formatting
            text_format = workbook.add_format({'text_wrap': False, 'num_format': '@'})
            
            # Apply text format to items and quantities columns
            items_col = df_combined_data.columns.get_loc('items')
            quantities_col = df_combined_data.columns.get_loc('quantities')
            
            # Format the entire columns as text (starting from row 1 to skip headers)
            worksheet.set_column(items_col, items_col, None, text_format)
            worksheet.set_column(quantities_col, quantities_col, None, text_format)
            
    except Exception as e:
        # Fallback to regular pandas Excel writer if xlsxwriter is not available
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
            "date": [],
        }
        create_database_file(initial_sell_data)
