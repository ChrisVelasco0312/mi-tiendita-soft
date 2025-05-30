from textual import log, on
from textual.containers import Container, Grid
from textual.screen import Screen
from textual.widgets import DataTable, Header, Input, Label

from src.business.create_stock_controller import read_stock, search_stock
from src.business.stock_mapper import stock_mapper
from src.ui.widgets.taskbar import Taskbar


class StockManageView(Screen):
    CSS_PATH = "styles/manage-view.tcss"

    def compose(self):
        yield Header()
        yield Grid(
            Taskbar(),
            Container(
                Label("Buscar item"),
                Input(
                    id="search_input",
                    placeholder="Escribe el código del ítem",
                ),
            ),
            Container(
                Label("Buscar por nombre"),
                Input(
                    id="search_input",
                    placeholder="Escribe el nombre del producto",
                ),
            ),
            DataTable(id="stock_table"),
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

    @on(Input.Changed, "#search_input")
    def on_input_change(self, event: Input.Changed) -> None:
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
