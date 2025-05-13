# -*- coding: utf-8 -*-
"""
A simple interactive form example using Textual (simplified layout).
"""
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button, Input
from textual.containers import VerticalScroll, Horizontal
from textual.message import Message
from textual.reactive import var

print('--- Preparing Textual App ---')

# Simplified CSS without Grid and without comments
FORM_CSS = """
Screen {
    align: center middle;
}

VerticalScroll {
    border: thick $accent;
    padding: 1 2;
    width: 60;
    height: auto;
    max-height: 80%;
}

Horizontal {
    height: auto;
    margin-bottom: 1;
    align: left middle;
}

#button-row {
    align: center middle;
    margin-top: 1;
}

.label {
    width: 10;
    margin-right: 2;
    text-align: right;
}

Input {
    width: 1fr;
}

#output_message {
    margin-top: 2;
    padding: 1;
    width: 100%;
    height: auto;
    min-height: 3;
    border: round $accent-lighten-2;
    text-align: center;
}
"""

class InteractiveFormApp(App):
    """A simple Textual form app."""

    TITLE = "Formulario Interactivo (Simple)"
    CSS = FORM_CSS

    output_text = var("")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with VerticalScroll(id="form-container"):
            yield Horizontal(
                Static("Name:", classes="label"),
                Input(placeholder="Your name", id="name_input")
            )
            yield Horizontal(
                Static("Email:", classes="label"),
                Input(placeholder="Your email", id="email_input")
            )
            yield Horizontal(
                Button("Submit", variant="primary", id="submit_button"),
                Button("Cancel", variant="error", id="cancel_button"),
                id="button-row"
            )
            yield Static(id="output_message", classes="output")
        yield Footer()

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self.query_one("#name_input").focus()

    def watch_output_text(self, new_message: str) -> None:
        """Update the Static widget when output_text changes."""
        output_widget = self.query_one("#output_message", Static)
        output_widget.update(new_message)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Called when a button is pressed."""
        if event.button.id == "submit_button":
            name_input = self.query_one("#name_input", Input)
            email_input = self.query_one("#email_input", Input)
            name = name_input.value
            email = email_input.value

            if name and email:
                self.output_text = f"[b green]Submitted![/] Name: '{name}', Email: '{email}'"
            else:
                self.output_text = "[b red]Error:[/b red] Please fill in both fields."
                if not name:
                    name_input.focus()
                else:
                    email_input.focus()

        elif event.button.id == "cancel_button":
            self.query_one("#name_input", Input).value = ""
            self.query_one("#email_input", Input).value = ""
            self.output_text = "Form cancelled."
            self.query_one("#name_input").focus()

# --- Main execution ---

def main():
    """Runs the Textual app."""
    app = InteractiveFormApp()
    app.run()

if __name__ == "__main__":
    main()