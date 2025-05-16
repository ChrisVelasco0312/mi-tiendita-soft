import pandas as pd


def read_excel_data(file_path: str, sheet_name: str):
    try:
        df_read = pd.read_excel(file_path, sheet_name=sheet_name)
        return df_read
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo {file_path}.")
    except Exception as error:
        print(f"Error al leer el archivo excel: {error}")
