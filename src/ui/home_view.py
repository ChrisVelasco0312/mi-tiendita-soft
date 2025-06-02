from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Vertical, Horizontal
from textual.widgets import Footer, Header, Button, Collapsible


class HomeView(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(classes="column"):
                with Collapsible(title='Inventario', collapsed=True):
                    yield Button("Registro de Inventario", variant="primary", id="stock_create_button")
                    yield Button("Consulta de Inventario", variant="primary", id="stock_manage_button")
            with Vertical(classes="column"):
                with Collapsible(title='Venta', collapsed=True):
                    yield Button("Generar Venta", variant="primary", id="create_sell_button")
                    yield Button("Consultar Venta", variant="primary", id="manage_sell_button")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "stock_create_button":
            self.app.push_screen("stock_register_view")
        elif event.button.id == "stock_manage_button":
            self.app.push_screen("stock_consult_view")
        elif event.button.id == "create_sell_button":
            self.app.push_screen("create_sell_view")
        elif event.button.id == "manage_sell_button":
            self.app.push_screen("manage_sell_view") 
