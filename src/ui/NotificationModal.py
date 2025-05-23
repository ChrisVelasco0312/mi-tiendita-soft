from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class NotificationModal(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Container(
            Container(
                Label(self.app.stock_data_message, id="message"),
                id="message-box",
            ),
            Container(
                Button("Crear Otro", id="create_other"),
                Button("Cancel", id="cancel"),
                id="actions",
            ),
            id="modal-box",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "create_other":
            self.app.pop_screen()
        else:
            self.app.pop_screen()
            self.app.push_screen("home")
