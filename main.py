from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.containers import Vertical, Horizontal, Container
from textual.widgets import Footer, Header, Button, Collapsible, Static

LAYOUT_CSS = '''
Vertical {
    align: center middle;
}
'''

class HomeView(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(classes="column"):
                with Collapsible(title='Inventario', collapsed=True):
                    yield Button("Registro de Inventario", variant="primary", id="stock_register_button")
                    yield Button("Consulta de Inventario", variant="primary", id="stock_consult_button")
            with Vertical(classes="column"):
                with Collapsible(title='Venta', collapsed=True):
                    yield Button("Generar Venta", variant="primary", id="generate_sell_button")
                    yield Button("Consultar Venta", variant="primary", id="get_sell_button")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "stock_register_button":
            self.app.push_screen("stock_register_view")
        elif event.button.id == "stock_consult_button":
            print('Venta')

class StockRegisterView(Screen):
    def compose(self):
        yield Container(
            Static("Registrar producto"),
            Button("Volver a inicio", id="go_home")
        )
    
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "go_home":
            self.app.pop_screen()

class MiTienditaApp(App):
    BINDINGS = [("d", "toggle_dark", "Togle dark mode")]
    CSS = LAYOUT_CSS

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def on_mount(self):
        self.install_screen(HomeView(), name="home")
        self.install_screen(StockRegisterView(), name="stock_register_view")
        self.push_screen("home")

if __name__ == "__main__":
    app = MiTienditaApp()
    app.run()
