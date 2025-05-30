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

        # Si el valor del campo es vacío, se retorna el dataframe completo
        if not field_value:
            return df_read

        # Usa el nombre del campo para filtrar el dataframe
        if field_name in df_read.columns:
            # Convierte el campo a string para que funcione el método .str
            filtered_df = df_read[
                df_read[field_name]
                .astype(str)
                .str.contains(field_value, case=False, na=False)
            ]
            return filtered_df
        else:
            return pd.DataFrame()

    except FileNotFoundError:
        print(f"Error: No se encontro el archivo {file_path}.")
    except Exception as error:
        print(f"Error al leer el archivo excel: {error}")
        return pd.DataFrame()
