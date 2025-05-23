from datetime import datetime

from src.business.category_controller import get_all_categories
from src.business.create_stock_controller import (
    create_item_code,
    create_stock_product,
    delete_stock_product,
    initialiaze_operations,
    read_stock,
    update_stock_product,
)

# initialiaze_operations()
# print(read_stock("AB_001"))

print(create_item_code("Alimentos y bebidas"))


# new_product_data = [
#     {
#         # El item_code solo se usa para encontrar el registro
#         "item_code": "AB_002",
#         "category": "Alimento y bebidas",
#         "product_name": "Arroz Doña Nieves 1k",
#         "quantity": 20,
#         "purchase_price": 3500,
#         "sale_price": 4500,
#         "creation_date": datetime.now(),
#     }
# ]

# updated_row_data = {
#     # El item_code solo se usa para encontrar el registro
#     "item_code": "AB_002",
#     "category": "Alimento y bebidas",
#     "product_name": "Papitas pobres rizadas",
#     "quantity": 25,
#     "purchase_price": 1500,
#     "sale_price": 3000,
#     "creation_date": datetime.now(),
# }
#
# update_stock_product(updated_row_data)

# create_stock_product(new_product_data)

# print(delete_stock_product("AB_002"))
