from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Button


class Taskbar(Widget):
    CSS = "../styles/taskbar.tcss"

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Button("← Volver", id="go_home", classes="back-button"),
            Button("cerrar", id="exit", classes="exit-button"),
        )
