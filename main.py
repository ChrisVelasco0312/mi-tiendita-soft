from textual import log
from textual.app import App

from src.business.create_stock_controller import initialiaze_operations
from src.ui.ConfirmationModal import ConfirmationModal
from src.ui.create_sell_view import CreateSellView
from src.ui.home_view import HomeView
from src.ui.manage_sell_view import ManageSellView
from src.ui.NotificationModal import NotificationModal
from src.ui.stock_create_view import StockCreateView
from src.ui.stock_delete_message import (
    StockDeleteConfirmedMessage,
    StockDeleteRequestMessage,
)
from src.ui.stock_manage_view import StockManageView
from src.ui.stock_update_message import StockDataRefreshMessage, StockUpdateMessage

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
        initialiaze_operations()

        self.install_screen(HomeView(), name="home")
        self.install_screen(StockCreateView(), name="stock_register_view")
        self.install_screen(StockManageView(), name="stock_consult_view")
        self.install_screen(CreateSellView(), name="create_sell_view")
        self.install_screen(ManageSellView(), name="manage_sell_view")
        self.install_screen(NotificationModal(), name="notification_modal")
        # la pantalla de entrada es home.
        self.push_screen("home")

    def on_stock_update_message(self, message: StockUpdateMessage) -> None:
        """Función que gestiona el evento para la data de actualización"""
        # Se trae la pantalla de registro de inventario
        stock_screen = self.get_screen("stock_register_view")

        # Se determina si existe la propiedad set_edit_data en la clase screen
        if hasattr(stock_screen, "set_edit_data"):
            # se envia el dato par activar o desactivar el modo editar
            stock_screen.set_edit_data(message.payload)

        # Se muestra la pantalla de registro
        self.push_screen("stock_register_view")

    def on_stock_data_refresh_message(self, message: StockDataRefreshMessage) -> None:
        try:
            stock_manage_screen = self.get_screen("stock_consult_view")
            if hasattr(stock_manage_screen, "refresh_data"):
                stock_manage_screen.refresh_data()
        except Exception as e:
            log(f"Error refreshing stock manage view: {e}")

    def on_stock_delete_request_message(
        self, message: StockDeleteRequestMessage
    ) -> None:
        confirmation_message = f"¿Está seguro de que desea eliminar el producto '{message.product_name}' (Código: {message.item_code})?\n\nEsta acción no se puede deshacer."

        # Se crea y muestra el modal de confirmación
        confirmation_modal = ConfirmationModal(confirmation_message, message.item_code)
        self.push_screen(confirmation_modal)

    def on_stock_delete_confirmed_message(
        self, message: StockDeleteConfirmedMessage
    ) -> None:
        from src.business.create_stock_controller import delete_stock_product

        try:
            delete_stock_product(message.item_code)

            stock_manage_screen = self.get_screen("stock_consult_view")
            if hasattr(stock_manage_screen, "refresh_data"):
                stock_manage_screen.refresh_data()

            self.notify(
                f"Producto {message.item_code} eliminado exitosamente",
                severity="information",
            )

        except Exception as e:
            self.notify(f"Error al eliminar producto: {str(e)}", severity="error")
            log(f"Error deleting product {message.item_code}: {e}")


if __name__ == "__main__":
    app = MiTienditaApp()
    app.run()
