from textual import on
from textual.containers import Container, Grid
from textual.screen import Screen
from textual.widgets import DataTable, Header, Input, Label

from src.business.create_stock_controller import read_stock, search_stock
from src.business.stock_mapper import stock_mapper
from src.ui.widgets.taskbar import Taskbar


class StockManageView(Screen):
    CSS_PATH = "styles/stock-manage-view.tcss"

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
        product_data = read_stock("")
        table = self.query_one(DataTable)

        columns = tuple(stock_mapper(product_data.columns))
        table.add_columns(*columns)

        for row in product_data.values:
            table.add_row(*tuple(row))

    @on(Input.Changed, "#search_by_code_input")
    def on_code_input_change(self, event: Input.Changed) -> None:
        product_data = read_stock("")
        table = self.query_one(DataTable)
        filtered_table = search_stock("item_code", event.value)

        if filtered_table.empty:
            table.clear()
            for row in product_data.values:
                table.add_row(*tuple(row))
        else:
            table.clear()
            for row in filtered_table.values:
                table.add_row(*tuple(row))
                
    @on(Input.Changed, "#search_by_name_input")
    def on_name_input_change(self, event: Input.Changed) -> None:
        product_data = read_stock("")
        table = self.query_one(DataTable)
        filtered_table = search_stock("product_name", event.value)

        if filtered_table.empty:
            table.clear()
            for row in product_data.values:
                table.add_row(*tuple(row))
        else:
            table.clear()
            for row in filtered_table.values:
                table.add_row(*tuple(row))
