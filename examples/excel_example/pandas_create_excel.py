import pandas as pd

"""
definimos un diccionario
para la data de la tabla excel
"""
data = {
    "Nombre": ["Fausto", "Meiko", "Mora", "Ofelia", "Iggy", "Matias"],
    "Edad": [5, 10, 10, 5, 9, 3],
    "Ciudad": ["Londres", "Paris", "Tokio", "Berlin", "Amsterdam", "Kioto"],
}
df_initial = pd.DataFrame(data)

# Se define el nombre del archivo
filename = "pandas_sample_data.xlsx"
sheet_name_original = "PetData"

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
