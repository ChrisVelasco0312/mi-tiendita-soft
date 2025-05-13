from textual.screen import Screen
from textual.containers import Container
from textual.widgets import Static, Button


class StockCreateView(Screen):
    def compose(self):
        yield Container(
            Static("Registrar producto"),
            Button("Volver a inicio", id="go_home")
        )
    
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "go_home":
            self.app.pop_screen() 