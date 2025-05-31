from textual import log
from textual.app import App 
from textual.reactive import reactive

from src.business.create_stock_controller import initialiaze_operations
from src.ui.create_sell_view import CreateSellView
from src.ui.home_view import HomeView
from src.ui.manage_sell_view import ManageSellView
from src.ui.NotificationModal import NotificationModal
from src.ui.stock_create_view import StockCreateView
from src.ui.stock_manage_view import StockManageView
from src.ui.stock_update_message import StockUpdateMessage

LAYOUT_CSS = """
Vertical {
    align: center middle;
}
"""

# Punto de entrada de la aplicación.
class MiTienditaApp(App):
    BINDINGS = [("d", "toggle_dark", "Togle dark mode")]
    CSS = LAYOUT_CSS
    
    # estas variables se convierten en estado global
    stock_data_message: str = ""

    # se habilita la función para intercalar entre tema dark y light
    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    # función del ciclo de vida de una app textual
    # se montan todas las pantallas (screen)
    def on_mount(self):
        create_datab = initialiaze_operations()
        log(create_datab)

        self.install_screen(HomeView(), name="home")
        self.install_screen(StockCreateView(), name="stock_register_view")
        self.install_screen(StockManageView(), name="stock_consult_view")
        self.install_screen(CreateSellView(), name="create_sell_view")
        self.install_screen(ManageSellView(), name="manage_sell_view")
        self.install_screen(NotificationModal(), name="notification_modal")
        # la pantalla de entrada es home.
        self.push_screen("home")

    def on_stock_update_message(self, message: StockUpdateMessage) -> None:
        """Handle stock update message and pass data to stock_register_view"""
        log(f"Received stock update message: {message.payload}")
        
        # Get the stock_register_view screen
        stock_screen = self.get_screen("stock_register_view")
        
        # Set the edit mode data
        if hasattr(stock_screen, 'set_edit_data'):
            stock_screen.set_edit_data(message.payload)
        
        # Navigate to the screen
        self.push_screen("stock_register_view")


if __name__ == "__main__":
    app = MiTienditaApp()
    app.run()
