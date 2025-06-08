import pandas as pd
from src.business.db_operations.classes import Sell


def update_excel_row(database, file_path: str, sheet_name: str, new_data: Sell):
    df_update = database
    print(df_update)

    # encontrar la fila por codigo de item item_code
    is_item = df_update["id"] == new_data["id"]
    print(df_update["id"])
    
    # encuentra cada uno de los datos para el item encontrado y le asigna el nuevo valor
    df_update.loc[is_item, "items"] = new_data["items"]
    df_update.loc[is_item, "quantities"] = new_data["quantities"]
    df_update.loc[is_item, "total"] = new_data["total"]
    
    # Convert items and quantities columns to string to prevent Excel auto-formatting
    df_update["items"] = df_update["items"].astype(str)
    df_update["quantities"] = df_update["quantities"].astype(str)
    
    try:
        # Use xlsxwriter engine to have more control over formatting
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            df_update.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Get the xlsxwriter workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            
            # Define a text format to prevent Excel from auto-formatting
            text_format = workbook.add_format({'text_wrap': False, 'num_format': '@'})
            
            # Apply text format to items and quantities columns
            items_col = df_update.columns.get_loc('items')
            quantities_col = df_update.columns.get_loc('quantities')
            
            # Format the entire columns as text
            worksheet.set_column(items_col, items_col, None, text_format)
            worksheet.set_column(quantities_col, quantities_col, None, text_format)
            
        return df_update
    except Exception as error:
        # Fallback to regular pandas Excel writer if xlsxwriter is not available
        print(f"Warning: xlsxwriter not available, using default Excel writer: {error}")
        try:
            df_update.to_excel(file_path, sheet_name=sheet_name, index=False)
            return df_update
        except Exception as fallback_error:
            print(f"Error al actualizar los datos del archivo: {file_path} {fallback_error}")
            return None
