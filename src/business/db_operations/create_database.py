import pandas as pd

from src.business.db_operations.classes import ProductData


def create_database_file(filename: str, data: ProductData):
    """
    definimos un diccionario
    para la data de la tabla excel
    """
    df_initial = pd.DataFrame(data)

    # Se define el nombre del archivo
    filename = "src/business/data/product_stock_data.xlsx"
    sheet_name_original = "ProductData"

    # Guardamos el archivo excel
    try:
        df_initial.to_excel(filename, sheet_name=sheet_name_original, index=False)
        print(f"{filename} fué creado con éxito con la hoja {sheet_name_original}")
    except PermissionError:
        print("PermissionError: No se pudo crear el archivo")
        exit()
    except Exception as e:
        print(f"Error mientras se creaba el archivo: {e}")
        exit()
