from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Button


class Taskbar(Widget):
    DEFAULT_CSS = '''
        /* Base styles that are generic enough to not cause conflicts */
        Taskbar {
          width: 100%;
          /* Minimal styling to ensure visibility */
          min-height: 1;
        }
        
        Taskbar Horizontal {
          width: 100%;
        }
        
        Taskbar #title {
          width: auto;
        }
        
        Taskbar .back-button {
          border: round;
        }
        
        Taskbar .exit-button {
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
    
    
