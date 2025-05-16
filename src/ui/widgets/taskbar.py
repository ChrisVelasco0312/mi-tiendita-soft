from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Button


class Taskbar(Widget):
    DEFAULT_CSS = '''
        Horizontal {
          width: 100%;
        }
        #title {
          width: auto;
        }
        .back-button {
          border: round;
        }
        .exit-button {
          align: center middle;
          background: red;
        }
    '''

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Button("← Volver", id="go_home", classes="back-button"),
            Button("cerrar aplicación", id="exit", classes="exit-button"),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "go_home":
            self.app.pop_screen()
        elif event.button.id == "exit":
            self.app.exit()
    
    
