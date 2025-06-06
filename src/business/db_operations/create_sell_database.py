import pandas as pd

from src.business.db_operations.classes import  SellData


def create_database_file(
    sell_data: SellData
):
    """
    definimos un diccionario
    para la data de la tabla excel
    """

    # Se define el nombre del archivo
    sell_file = "src/business/data/sell_data.xlsx"
    sell_sheet = "SellData"

    df_sell_dataframe = pd.DataFrame(sell_data)

    # Guardamos el archivo excel
    try:
        df_sell_dataframe.to_excel(sell_file, sheet_name=sell_sheet, index=False)

        print(
            f"{sell_file} fué creado con éxito con las hojas {sell_sheet}"
        )
    except PermissionError:
        print("PermissionError: No se pudo crear el archivo")
        exit()
    except Exception as e:
        print(f"Error mientras se creaba el archivo: {e}")
        exit()
