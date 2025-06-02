from textual import log
from textual.app import ComposeResult
from textual.containers import Horizontal, Grid, Container
from textual.widget import Widget
from textual.widgets import Button


class Taskbar(Widget):
    DEFAULT_CSS = '''
        /* Base styles that are generic enough to not cause conflicts */
        Taskbar {
          width: 100%;
          /* Minimal styling to ensure visibility */
          height: 100%;
        }
        
        Taskbar Grid {
          width: 100%;
          grid-size: 3 1;
          grid-columns: 1fr 3fr 1fr;
        }
        
        Taskbar #title {
          width: auto;
        }
        
        Taskbar .back-button {
          border: round;
        }

        Taskbar #button_1 {
         align: left middle; 
         column-span: 1;
        }

        Taskbar #button_2 {
          align: right middle;
          column-span: 1;
        }
        
        Taskbar .exit-button {
        }
    '''

    def compose(self) -> ComposeResult:
        yield Grid(
            Container(
                Button("← Volver", id="go_home", classes="back-button"),
                id="button_1"
            ),
            Container(
                Button("cerrar aplicación", variant="error", id="exit", classes="exit-button"),
                id="button_2"
            )
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "go_home":
            self.app.pop_screen()
        elif event.button.id == "exit":
            self.app.exit()
    
    
