def stock_mapper(data: list):
    stock_map = {
        "item_code": "item",
        "category": "Categoría",
        "product_name": "Nombre",
        "quantity": "Cantidad",
        "purchase_price": "Precio Compra",
        "sale_price": "Precio Venta",
        "creation_date": "Fecha de Creación",
    }

    new_columns = []

    for column in data:
        column_name = stock_map[column]
        new_columns.append(column_name)

    return new_columns
