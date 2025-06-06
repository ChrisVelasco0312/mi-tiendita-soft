import pandas as pd

from src.business.db_operations.classes import CategoryData, ProductData, SellData


def create_database_file(
    stock_file: str, product_data: ProductData, category_data: CategoryData, sell_data: SellData
):
    """
    definimos un diccionario
    para la data de la tabla excel
    """

    # Se define el nombre del archivo
    stock_file = "src/business/data/product_stock_data.xlsx"
    category_file = "src/business/data/category_data.xlsx"
    sell_file = "src/business/data/sell_data.xlsx"
    product_sheet = "ProductData"
    category_sheet = "CategoryData"
    sell_sheet = "SellData"

    df_initial = pd.DataFrame(product_data)
    pd_new_dataframe = pd.DataFrame(category_data)
    df_sell_dataframe = pd.DataFrame(sell_data)

    # Guardamos el archivo excel
    try:
        df_initial.to_excel(stock_file, sheet_name=product_sheet, index=False)
        pd_new_dataframe.to_excel(category_file, sheet_name=category_sheet, index=False)
        df_initial.to_excel(sell_file, sheet_name=sell_sheet, index=False)

        print(
            f"{stock_file} fué creado con éxito con las hojas {product_sheet} y {category_sheet}"
        )
    except PermissionError:
        print("PermissionError: No se pudo crear el archivo")
        exit()
    except Exception as e:
        print(f"Error mientras se creaba el archivo: {e}")
        exit()
