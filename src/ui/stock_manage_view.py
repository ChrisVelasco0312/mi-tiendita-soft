from textual import log, on
from textual.reactive import reactive, var
from textual.containers import Container, Grid
from textual.screen import Screen
from textual.widgets import DataTable, Header, Input, Label
from rich.text import Text

from src.business.create_stock_controller import read_stock, search_stock
from src.business.stock_mapper import stock_mapper
from src.ui.widgets.taskbar import Taskbar
from src.ui.stock_update_message import StockUpdateMessage, StockDataRefreshMessage


class StockManageView(Screen):
    CSS_PATH = "styles/stock-manage-view.tcss"

    current_data = var(read_stock(""))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compose(self):
        yield Header()
        yield Grid(
            Taskbar(id="manage_taskbar"),
            Container(
                Label("Buscar item", classes="manage-label"),
                Input(
                    id="search_by_code_input",
                    placeholder="Escribe el código del ítem",
                    classes="manage-input",
                ),
                classes="manage-container",
            ),
            Container(
                Label("Buscar por nombre", classes="manage-label"),
                Input(
                    id="search_by_name_input",
                    placeholder="Escribe el nombre del producto",
                    classes="manage-input",
                ),
                classes="manage-container",
            ),
            DataTable(id="stock_table", classes="manage-table"),
            classes="manage-grid",
            id="manage_grid",
        )

    def on_mount(self):
        self.load_stock_excel()

    def load_stock_excel(self):
        product_data = self.current_data
        table = self.query_one(DataTable)

        columns = tuple(stock_mapper(product_data.columns))
        table.add_columns(*columns, "Editar")

        for row in product_data.values:
            edit_button = Text("Editar", style="bold blue underline")
            table.add_row(*tuple(row), edit_button)

    def refresh_data(self):
        """Refresh the table data by reloading from the Excel file"""
        log("Refreshing stock data...")
        product_data = self.current_data
        table = self.query_one(DataTable)
        
        # Clear the table and reload data
        table.clear()
        for row in product_data.values:
            edit_button = Text("Editar", style="bold blue underline")
            table.add_row(*tuple(row), edit_button)

    def on_stock_data_refresh_message(self, message: StockDataRefreshMessage) -> None:
        """Handle stock data refresh message"""
        log("Received stock data refresh message")
        self.refresh_data()

    # evento para buscar por item
    @on(Input.Changed, "#search_by_code_input")
    def on_code_input_change(self, event: Input.Changed) -> None:
        filtered_table = search_stock("item_code", event.value)
        if filtered_table.empty:
            product_data = self.current_data
            table = self.query_one(DataTable)
            table.clear()
            for row in product_data.values:
                edit_button = Text("Editar", style="bold blue underline")
                table.add_row(*tuple(row), edit_button)
        else:
            table = self.query_one(DataTable)
            table.clear()
            for row in filtered_table.values:
                edit_button = Text("Editar", style="bold blue underline")
                table.add_row(*tuple(row), edit_button)

    # evento para buscar por nombre
    @on(Input.Changed, "#search_by_name_input")
    def on_name_input_change(self, event: Input.Changed) -> None:
        product_data = self.current_data
        table = self.query_one(DataTable)
        filtered_table = search_stock("product_name", event.value)

        if filtered_table.empty:
            table.clear()
            for row in product_data.values:
                edit_button = Text("Editar", style="bold blue underline")
                table.add_row(*tuple(row), edit_button)
        else:
            table.clear()
            for row in filtered_table.values:
                edit_button = Text("Editar", style="bold blue underline")
                table.add_row(*tuple(row), edit_button)

    @on(DataTable.CellSelected)
    def on_cell_selected(self, event: DataTable.CellSelected) -> None:
        product_data = self.current_data
        """Handle cell selection in the stock table."""
        table = self.query_one(DataTable)
        # Tomar el indice de la ultima columna
        last_column_index = len(table.columns) - 1
        selected_row_data = table.get_row(event.cell_key.row_key)
        
        # Validar si la celda seleccionada es la ultima columna
        if event.coordinate.column == last_column_index:
            # Enviar el mensaje con los datos del producto
            self.post_message(StockUpdateMessage({
                "item_code": selected_row_data[0],
                "category": selected_row_data[1],
                "product_name": selected_row_data[2],
                "quantity": selected_row_data[3],
                "purchase_price": selected_row_data[4],
                "sale_price": selected_row_data[5],
                "creation_date": selected_row_data[6]
            }))

        self.notify(f"Editando item con código: {selected_row_data[0]}")

        
