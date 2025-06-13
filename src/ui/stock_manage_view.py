from rich.text import Text
from textual import log, on
from textual.containers import Container, Grid
from textual.reactive import var
from textual.screen import Screen
from textual.widgets import DataTable, Header, Input, Label

from src.business.create_stock_controller import read_stock, search_stock
from src.business.stock_mapper import stock_mapper
from src.ui.stock_delete_message import StockDeleteRequestMessage
from src.ui.stock_update_message import StockDataRefreshMessage, StockUpdateMessage
from src.ui.widgets.taskbar import Taskbar


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
        product_data = read_stock("")
        table = self.query_one(DataTable)

        columns = tuple(stock_mapper(product_data.columns))
        table.add_columns(*columns, "Editar", "Eliminar")

        for row in product_data.values:
            edit_button = Text("Editar", style="bold blue underline")
            delete_button = Text("Eliminar", style="bold red underline")
            table.add_row(*tuple(row), edit_button, delete_button)

    def refresh_data(self):
        # Vuelve a cargar la tabla desde el excel
        log("Refreshing stock data...")
        product_data = read_stock("")
        table = self.query_one(DataTable)

        # Borra la tabla y recarga los datos
        table.clear()
        for row in product_data.values:
            edit_button = Text("Editar", style="bold blue underline")
            delete_button = Text("Eliminar", style="bold red underline")
            table.add_row(*tuple(row), edit_button, delete_button)

    def on_stock_data_refresh_message(self, message: StockDataRefreshMessage) -> None:
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
                delete_button = Text("Eliminar", style="bold red underline")
                table.add_row(*tuple(row), edit_button, delete_button)
        else:
            table = self.query_one(DataTable)
            table.clear()
            for row in filtered_table.values:
                edit_button = Text("Editar", style="bold blue underline")
                delete_button = Text("Eliminar", style="bold red underline")
                table.add_row(*tuple(row), edit_button, delete_button)

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
                delete_button = Text("Eliminar", style="bold red underline")
                table.add_row(*tuple(row), edit_button, delete_button)
        else:
            table.clear()
            for row in filtered_table.values:
                edit_button = Text("Editar", style="bold blue underline")
                delete_button = Text("Eliminar", style="bold red underline")
                table.add_row(*tuple(row), edit_button, delete_button)

    @on(DataTable.CellSelected)
    def on_cell_selected(self, event: DataTable.CellSelected) -> None:
        # evento para gestional la selección de celdas
        table = self.query_one(DataTable)
        # Tomar el indice de la ultima columna (Delete) y la penúltima (Edit)
        last_column_index = len(table.columns) - 1  # Botón de borrar
        second_to_last_column_index = len(table.columns) - 2  # Botón de editar
        selected_row_data = table.get_row(event.cell_key.row_key)

        # Validar si la celda seleccionada es la penúltima columna (Edit)
        if event.coordinate.column == second_to_last_column_index:
            # Enviar el mensaje con los datos del producto para edición
            self.post_message(
                StockUpdateMessage(
                    {
                        "item_code": selected_row_data[0],
                        "category": selected_row_data[1],
                        "product_name": selected_row_data[2],
                        "quantity": selected_row_data[3],
                        "purchase_price": selected_row_data[4],
                        "sale_price": selected_row_data[5],
                        "creation_date": selected_row_data[6],
                    }
                )
            )
            self.notify(f"Editando item con código: {selected_row_data[0]}")

        # Validar si la celda seleccionada es la última columna (Delete)
        elif event.coordinate.column == last_column_index:
            # Enviar mensaje para solicitar eliminación con confirmación
            item_code = selected_row_data[0]
            product_name = selected_row_data[2]
            self.post_message(StockDeleteRequestMessage(item_code, product_name))
            self.notify(f"Solicitando eliminación de: {product_name}")
