import pandas as pd


def read_excel_data(file_path: str, sheet_name: str, item_code: str):
    # se hace gestion de errores con try except para capturarlos
    try:
        # se revisa si el item_code es vacio, por lo tanto se retorna toda la tabla
        if not item_code:
            df_read = pd.read_excel(file_path, sheet_name=sheet_name)
            return df_read
        else:
            # si se proporciona el item_code se retorna un único item
            df_read = pd.read_excel(file_path, sheet_name=sheet_name)
            return df_read[df_read["item_code"] == item_code]

    except FileNotFoundError:
        print(f"Error: No se encontro el archivo {file_path}.")
    except Exception as error:
        print(f"Error al leer el archivo excel: {error}")


def search_data_by_field(
    file_path: str, sheet_name: str, field_name: str, field_value: str
):
    try:
        df_read = pd.read_excel(file_path, sheet_name=sheet_name)
        return df_read[df_read[field_name] == field_value]

    except FileNotFoundError:
        print(f"Error: No se encontro el archivo {file_path}.")
    except Exception as error:
        print(f"Error al leer el archivo excel: {error}")
