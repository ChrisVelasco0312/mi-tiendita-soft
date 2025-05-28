from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Button, DataTable, Input
from src.business.create_stock_controller import read_stock, update_stock_product, delete_stock_product


class StockManageView(Screen):
    def compose(self):
        self.tabla = DataTable(zebra_stripes=True)
        self.tabla.add_columns("item_code", "category", "product_name", "quantity", "sale_price")

        self.status = Static("Selecciona un producto para editar o eliminar.", id="status")

        self.load_data()

        yield Container(
            Static("Inventario Actual", id="titulo"),
            self.tabla,
            Horizontal(
                Button("Editar", id="editar"),
                Button("Eliminar", id="eliminar"),
                Button("Actualizar", id="actualizar"),
                Button("Volver", id="volver"),
            ),
            self.status
        )

    def load_data(self):
        self.tabla.clear()
        productos_df = read_stock("")  # Devuelve un DataFrame
        productos = productos_df.to_dict(orient="records")  # Convertir a lista de dicts
        for p in productos:
            self.tabla.add_row(
                str(p["item_code"]),
                p["category"],
                p["product_name"],
                str(p["quantity"]),
                str(p["sale_price"])
            )

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "volver":
            self.app.pop_screen()
            return

        selected = self.tabla.cursor_row
        if selected is None:
            self.status.update("Debes seleccionar un producto.")
            return

        item_data = self.tabla.get_row(selected)
        item_code = item_data[0]

        if event.button.id == "eliminar":
            delete_stock_product(item_code)
            self.status.update(f"Producto {item_code} eliminado.")
            self.load_data()

        elif event.button.id == "editar":
            self.app.push_screen(EditItemView(item_data))

        elif event.button.id == "actualizar":
            self.load_data()
            self.status.update("Inventario actualizado.")


class EditItemView(Screen):
    def __init__(self, item_data):
        super().__init__()
        self.item_data = item_data

    def compose(self):
        self.inputs = {
            "item_code": Input(value=self.item_data[0], placeholder="Código", id="item_code"),
            "category": Input(value=self.item_data[1], placeholder="Categoría", id="category"),
            "product_name": Input(value=self.item_data[2], placeholder="Nombre", id="product_name"),
            "quantity": Input(value=self.item_data[3], placeholder="Cantidad", id="quantity"),
            "sale_price": Input(value=self.item_data[4], placeholder="Precio", id="sale_price"),
        }
        self.status = Static("", id="status")

        yield Container(
            Static("Editar Producto"),
            Vertical(*self.inputs.values()),
            Horizontal(
                Button("Guardar Cambios", id="guardar"),
                Button("Cancelar", id="cancelar"),
            ),
            self.status
        )

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "guardar":
            try:
                updated_data = {
                    "item_code": self.inputs["item_code"].value,
                    "category": self.inputs["category"].value,
                    "product_name": self.inputs["product_name"].value,
                    "quantity": int(self.inputs["quantity"].value),
                    "sale_price": float(self.inputs["sale_price"].value),
                }

                update_stock_product(updated_data)
                self.status.update("Producto actualizado correctamente.")
                self.app.pop_screen()

            except Exception as e:
                self.status.update(f"Error al actualizar: {e}")

        elif event.button.id == "cancelar":
            self.app.pop_screen()