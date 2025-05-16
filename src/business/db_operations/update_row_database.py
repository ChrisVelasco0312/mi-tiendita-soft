def update_excel_row(database, item_code: str, file_path: str, sheet_name: str):
    df_update = database

    # encontrar la fila
    df_update.loc[df_update["item_code"] == item_code, "product_name"] = "Updated Name"
    try:
        df_update.to_excel(file_path, sheet_name=sheet_name, index=False)
        return df_update
    except Exception as error:
        print(f"Error al actualizar los datos del archivo: {file_path} {error}")
