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
from src.business.sell_controller import (
    create_sell,
    initialize_sell_db,
    read_sell_data,
    update_sell,
)

# initialiaze_operations()
# print(read_stock("AB_001"))

# print(create_item_code("Alimentos y bebidas"))


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

initialize_sell_db()
# print(read_sell_data())

# new_sell_data = [
#     {
#         "items": "AB5-CA5-TA1",
#         "quantities": "40-50-60",
#         "total": 1200000,
#     }
# ]
#
# create_sell(new_sell_data)

# updated_sell_row = {
#     "id": 1,
#     "items": "AB1-AB2-AB3",
#     "quantities": "1-4-10",
#     "total": 54200,
# }
#
# update_sell(updated_sell_row)
