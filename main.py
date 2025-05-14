from textual.app import App 
from src.ui.home_view import HomeView
from src.ui.stock_create_view import StockCreateView
from src.ui.stock_manage_view import StockManageView
from src.ui.create_sell_view import CreateSellView
from src.ui.manage_sell_view import ManageSellView
import sys
print("sys.path", sys.path)

LAYOUT_CSS = '''
Vertical {
    align: center middle;
}
'''

class MiTienditaApp(App):
    BINDINGS = [("d", "toggle_dark", "Togle dark mode")]
    CSS = LAYOUT_CSS

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def on_mount(self):
        self.install_screen(HomeView(), name="home")
        self.install_screen(StockCreateView(), name="stock_register_view")
        self.install_screen(StockManageView(), name="stock_consult_view")
        self.install_screen(CreateSellView(), name="create_sell_view")
        self.install_screen(ManageSellView(), name="manage_sell_view")
        self.push_screen("home")

if __name__ == "__main__":
    app = MiTienditaApp()
    app.run()
