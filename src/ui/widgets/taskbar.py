from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Horizontal
from textual.widgets import Label, Button



class Taskbar(Widget):
    CSS = '../styles/taskbar.tcss'

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Button("← Volver", id="go_home", classes="back-button"),
            Label("Mi Tiendita App", id="title"),
            Button("cerrar", id="exit", classes="exit-button"),
        )

