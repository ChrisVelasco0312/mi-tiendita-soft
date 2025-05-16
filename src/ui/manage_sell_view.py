from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Button, Collapsible
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Static
from textual.containers import Container


PRODUCTOS = [
    {"id": 1, "nombre": "Pan", "cantidad": 20, "vendido": 5000, "fecha_venta": "2025-05-10"},
    {"id": 2, "nombre": "Leche", "cantidad": 10, "vendido": 3000, "fecha_venta": "2025-05-14"},
    {"id": 3, "nombre": "Arroz", "cantidad": 3, "vendido": 7500, "fecha_venta": "2025-05-13"},
    {"id": 4, "nombre": "Huevos", "cantidad": 5, "vendido": 600, "fecha_venta": "2025-05-13"},
    {"id": 5, "nombre": "Jugo Hit", "cantidad": 4, "vendido": 12000, "fecha_venta": "2025-05-13"},
]



class ManageSellView(Screen):

    def compose(self):
        tabla = DataTable(zebra_stripes=True)
        tabla.add_columns("ID", "Nombre", "Cantidad", "Total Vendido", "Fecha Venta")
        for p in PRODUCTOS:
            tabla.add_row(str(p["id"]), p["nombre"], str(p["cantidad"]), str(p["vendido"]), p["fecha_venta"])

        yield Container(
            Static("CONSULTAR VENTAS"),
            Static("Ventas Realizadas"),
            tabla,
            Button("Volver", id="volver"),
            Button("Generar Venta")
        )

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "volver":
            self.app.pop_screen()
        elif event.button.id == "generar_venta":
            self.app.push_screen()

