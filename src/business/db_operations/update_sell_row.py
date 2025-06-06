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
    
    try:
        df_update.to_excel(file_path, sheet_name=sheet_name, index=False)
        return df_update
    except Exception as error:
        print(f"Error al actualizar los datos del archivo: {file_path} {error}")
