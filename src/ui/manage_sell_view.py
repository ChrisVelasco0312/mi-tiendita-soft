from textual.screen import Screen
from textual.containers import Container
from textual.widgets import Static, Button


class ManageSellView(Screen):
    def compose(self):
        yield Container(
            Static("Consultar Venta"),
            Button("Volver a inicio", id="go_home")
        )
    
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "go_home":
            self.app.pop_screen() 