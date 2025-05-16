from src.business.db_operations.classes import Product


def update_excel_row(database, file_path: str, sheet_name: str, new_data: Product):
    df_update = database

    # encontrar la fila por codigo de item item_code
    is_item = df_update["item_code"] == new_data["item_code"]
    df_update.loc[is_item, "category"] = new_data["category"]
    df_update.loc[is_item, "product_name"] = new_data["product_name"]
    df_update.loc[is_item, "quantity"] = new_data["quantity"]
    df_update.loc[is_item, "purchase_price"] = new_data["purchase_price"]
    df_update.loc[is_item, "sale_price"] = new_data["sale_price"]
    df_update.loc[is_item, "creation_date"] = new_data["creation_date"]

    try:
        df_update.to_excel(file_path, sheet_name=sheet_name, index=False)
        return df_update
    except Exception as error:
        print(f"Error al actualizar los datos del archivo: {file_path} {error}")
