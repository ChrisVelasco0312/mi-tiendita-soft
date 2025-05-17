from textual.screen import Screen
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, DataTable, Static
from textual.containers import Container
from src.business.create_stock_controller import read_stock  


class StockManageView(Screen):

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("Consulta de Inventario", id="title"),
            Input(placeholder="Ingrese código del ítem", id="item_input"),
            Button("Filtrar", id="filter_button"),
            Button("Volver", id="back_button"),
            DataTable(id="inventory_table"),
        )
        yield Footer()


    def on_mount(self):
        self.table = self.query_one("#inventory_table", DataTable)
        self.table.add_columns(
            "Código", "Nombre", "Categoría", "Cantidad",
            "Precio Compra", "Precio Venta", "Creación"
        )
        self.load_data()

    def load_data(self, item_code: str = ""):
        #usamos read_stock para llamar los productos del archivo .xlsx
        data = read_stock(item_code)  #usamos tu función real
        self.table.clear()
        for _, row in data.iterrows():  
            self.table.add_row(
                str(row["item_code"]),
                str(row["product_name"]),
                str(row["category"]),
                str(row["quantity"]),
                str(row["purchase_price"]),
                str(row["sale_price"]),
                str(row["creation_date"]),
            )

    def on_button_pressed(self, event):
        if event.button.id == "filter_button":
            item_code = self.query_one("#item_input", Input).value
            self.load_data(item_code)

    def on_button_pressed(self, event):
        if event.button.id == "filter_button":
        # Botno para filtrar los productos por medio de numero de item.
            item_code = self.query_one("#item_input", Input).value
            self.load_data(item_code)
        elif event.button.id == "back_button":
        # Volver a la pantalla anterior o cerrar la pantalla actual
            self.app.pop_screen()


if __name__ == "__main__":
    app = StockManageView()
    app.run()