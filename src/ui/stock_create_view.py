from textual.containers import Grid
from textual.screen import Screen
from textual.widgets import Button, Select

from src.ui.widgets.taskbar import Taskbar

CATEGORIES = [
    "Categoría 1",
    "Categoría 2",
    "Categoría 3",
]


class StockCreateView(Screen):
    CSS_PATH = "styles/create-view.tcss"

    def compose(self):
        yield Grid(Taskbar(), Select(((category, category) for category in CATEGORIES)))

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "go_home":
            self.app.pop_screen()
        elif event.button.id == "exit":
            self.app.exit()
