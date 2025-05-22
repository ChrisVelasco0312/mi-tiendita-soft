from src.business.db_operations.read_database import read_excel_data

FILE_PATH = "src/business/data/product_stock_data.xlsx"
SHEET_NAME = "CategoryData"


def get_all_categories():
    data = read_excel_data(FILE_PATH, SHEET_NAME, "")
    if data is None:
        return ""
    if "name" in data:
        return data["name"]
