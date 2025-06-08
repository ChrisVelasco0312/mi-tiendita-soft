from rich.text import Text
from textual import log, on
from textual.containers import Container, Grid, Horizontal, Vertical
from textual.reactive import var
from textual.screen import Screen
from textual.widgets import DataTable, Header, Input, Label

from src.business.create_stock_controller import search_stock, read_stock
from src.business.sell_controller import read_sell_data
from src.ui.widgets.taskbar import Taskbar


class ManageSellView(Screen):
    CSS_PATH = "styles/stock-manage-view.tcss"

    current_data = var(read_sell_data())
    selected_sell_data = var(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compose(self):
        yield Header()
        yield Grid(
            Taskbar(id="manage_taskbar"),
            # Contenedor horizontal para ambas tablas - now taking more space
            Horizontal(
                Container(
                    Label("Historial de ventas", classes="manage-label"),
                    DataTable(id="sell_table", classes="manage-table"),
                    classes="table-container",
                ),
                Container(
                    Label("Detalle de venta seleccionada", classes="manage-label"),
                    Label("Selecciona una venta para ver la fecha", id="sell_date_label", classes="date-label"),
                    DataTable(id="detail_table", classes="manage-table"),
                    classes="table-container",
                ),
                classes="tables-horizontal",
            ),
            classes="manage-grid",
            id="manage_grid",
        )

    def on_mount(self):
        self.load_stock_excel()
        self.setup_detail_table()

    def setup_detail_table(self):
        """Configura la tabla de detalle con las columnas apropiadas."""
        detail_table = self.query_one("#detail_table", DataTable)
        detail_table.add_columns("Código", "Producto", "Precio", "Cantidad", "Total")

    def load_stock_excel(self):
        sell_data = read_sell_data()
        sell_data = sell_data[["id", "total", "date"]]
        table = self.query_one("#sell_table", DataTable)

        column_translations = {
            "id": "# Venta",
            "total": "Total",
            "date": "Fecha",
        }

        columns = []

        for column in sell_data.columns:
            column_name = column_translations[column]
            columns.append(column_name)

        columns = tuple(columns)

        table.add_columns(*columns, "Detalle")

        for row in sell_data.values:
            agregar_button = Text("ver detalle", style="bold green underline")
            table.add_row(*tuple(row), agregar_button)

    def refresh_data(self):
        """Refresh the table data by reloading from the Excel file"""
        log("Refreshing stock data...")
        sell_data = read_sell_data()
        sell_data = sell_data[["id", "total", "date"]]
        table = self.query_one("#sell_table", DataTable)

        # Clear the table and reload data
        table.clear()
        for row in sell_data.values:
            agregar_button = Text("ver detalle", style="bold green underline")
            table.add_row(*tuple(row), agregar_button)

    def load_sell_detail(self, sell_id):
        """Carga el detalle de la venta seleccionada en la tabla de detalle."""
        # Obtener los datos completos de la venta
        sell_data = read_sell_data()
        selected_sell = sell_data[sell_data["id"] == sell_id].iloc[0]
        
        # Update the date label
        date_label = self.query_one("#sell_date_label", Label)
        sell_date = selected_sell["date"]
        date_label.update(f"Fecha: {sell_date}")
        
        log(f"Selected sell data: {selected_sell}")
        
        # Parsear los items y cantidades
        items = selected_sell["items"].split("-") if selected_sell["items"] else []
        quantities = selected_sell["quantities"].split("-") if selected_sell["quantities"] else []
        
        log(f"Items: {items}")
        log(f"Quantities: {quantities}")
        
        # Obtener datos del stock para los items
        stock_data = read_stock("")
        detail_table = self.query_one("#detail_table", DataTable)
        
        log(f"Stock data columns: {stock_data.columns.tolist()}")
        log(f"Sample item codes from stock: {stock_data['item_code'].head().tolist()}")
        
        # Limpiar la tabla de detalle
        detail_table.clear()
        
        # Agregar cada item con su información
        for i, item_code in enumerate(items):
            if i < len(quantities):
                quantity = int(quantities[i])
                
                log(f"Searching for item_code: '{item_code}' (type: {type(item_code)})")
                
                # Buscar la información del producto en el stock - try both string and int conversion
                product_info = stock_data[stock_data["item_code"] == item_code]
                
                # If no match, try converting to string or int
                if product_info.empty:
                    # Try as string
                    product_info = stock_data[stock_data["item_code"] == str(item_code)]
                    
                if product_info.empty:
                    # Try as int if possible
                    try:
                        item_code_int = int(item_code)
                        product_info = stock_data[stock_data["item_code"] == item_code_int]
                    except (ValueError, TypeError):
                        pass
                
                log(f"Found product info: {not product_info.empty}")
                
                if not product_info.empty:
                    product = product_info.iloc[0]
                    product_name = product["product_name"]
                    price = float(product["sale_price"])
                    total = price * quantity
                    
                    detail_table.add_row(
                        str(item_code),
                        str(product_name),
                        f"{price:.2f}",
                        str(quantity),
                        f"{total:.2f}"
                    )
                else:
                    # Si no se encuentra el producto en el stock
                    detail_table.add_row(
                        str(item_code),
                        "Producto no encontrado",
                        "0.00",
                        str(quantity),
                        "0.00"
                    )

    @on(DataTable.CellSelected)
    def on_cell_selected(self, event: DataTable.CellSelected) -> None:
        """Handle cell selection in the sell table."""
        # Solo manejar clicks en la tabla de ventas principales
        if event.data_table.id != "sell_table":
            return
            
        table = self.query_one("#sell_table", DataTable)
        # Tomar el indice de la ultima columna
        last_column_index = len(table.columns) - 1
        selected_row_data = table.get_row(event.cell_key.row_key)
        selected_row_id = selected_row_data[0]

        # Validar si la celda seleccionada es la ultima columna (botón "ver detalle")
        if event.coordinate.column == last_column_index:
            # Cargar el detalle de la venta seleccionada
            self.load_sell_detail(selected_row_id)
            self.notify(f"Mostrando detalle de venta #{selected_row_id}")
