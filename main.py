from textual import log
from textual.app import App

from src.business.create_stock_controller import initialiaze_operations
from src.ui.create_sell_view import CreateSellView
from src.ui.home_view import HomeView
from src.ui.manage_sell_view import ManageSellView
from src.ui.NotificationModal import NotificationModal
from src.ui.ConfirmationModal import ConfirmationModal
from src.ui.stock_create_view import StockCreateView
from src.ui.stock_manage_view import StockManageView
from src.ui.stock_update_message import StockDataRefreshMessage, StockUpdateMessage
from src.ui.stock_delete_message import StockDeleteRequestMessage, StockDeleteConfirmedMessage

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
        if hasattr(stock_screen, "set_edit_data"):
            stock_screen.set_edit_data(message.payload)

        # Navigate to the screen
        self.push_screen("stock_register_view")

    def on_stock_data_refresh_message(self, message: StockDataRefreshMessage) -> None:
        """Handle stock data refresh message and refresh the stock manage view"""
        log("Received stock data refresh message")

        # Get the stock_consult_view screen and refresh its data
        try:
            stock_manage_screen = self.get_screen("stock_consult_view")
            if hasattr(stock_manage_screen, "refresh_data"):
                stock_manage_screen.refresh_data()
                log("Stock manage view refreshed")
        except Exception as e:
            log(f"Error refreshing stock manage view: {e}")

    def on_stock_delete_request_message(self, message: StockDeleteRequestMessage) -> None:
        """Handle stock delete request message and show confirmation modal"""
        log(f"Received stock delete request for: {message.item_code} - {message.product_name}")
        
        confirmation_message = f"¿Está seguro de que desea eliminar el producto '{message.product_name}' (Código: {message.item_code})?\n\nEsta acción no se puede deshacer."
        
        # Create and show confirmation modal
        confirmation_modal = ConfirmationModal(confirmation_message, message.item_code)
        self.push_screen(confirmation_modal)

    def on_stock_delete_confirmed_message(self, message: StockDeleteConfirmedMessage) -> None:
        """Handle confirmed stock deletion"""
        log(f"Confirmed deletion for item: {message.item_code}")
        
        # Import here to avoid circular imports
        from src.business.create_stock_controller import delete_stock_product
        
        try:
            # Delete the product from the database
            delete_stock_product(message.item_code)
            
            # Refresh the stock manage view
            stock_manage_screen = self.get_screen("stock_consult_view")
            if hasattr(stock_manage_screen, "refresh_data"):
                stock_manage_screen.refresh_data()
            
            # Show success notification
            self.notify(f"Producto {message.item_code} eliminado exitosamente", severity="information")
            log(f"Product {message.item_code} deleted successfully")
            
        except Exception as e:
            # Show error notification
            self.notify(f"Error al eliminar producto: {str(e)}", severity="error")
            log(f"Error deleting product {message.item_code}: {e}")


if __name__ == "__main__":
    app = MiTienditaApp()
    app.run()
