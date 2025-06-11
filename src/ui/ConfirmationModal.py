from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class ConfirmationModal(ModalScreen):
    CSS_PATH = "styles/create-view.tcss"
    
    def __init__(self, message: str, item_code: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message
        self.item_code = item_code

    def compose(self) -> ComposeResult:
        yield Container(
            Container(
                Label(self.message, id="confirmation-message"),
                id="confirmation-message-box",
            ),
            Container(
                Button("Sí, Eliminar", id="confirm_delete", variant="error"),
                Button("Cancelar", id="cancel_delete"),
                id="confirmation-actions",
            ),
            id="confirmation-modal-box",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm_delete":
            # Import here to avoid circular imports
            from src.ui.stock_delete_message import StockDeleteConfirmedMessage
            
            # Send confirmation message with item_code
            self.post_message(StockDeleteConfirmedMessage(self.item_code))
            self.app.pop_screen()
        else:
            # User cancelled, just close the modal
            self.app.pop_screen()
