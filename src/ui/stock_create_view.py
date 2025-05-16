from textual import log, on
from textual.containers import Grid, VerticalScroll
from textual.reactive import reactive, var
from textual.screen import Screen
from textual.validation import Integer, Length, Regex, ValidationResult, Validator
from textual.widgets import Button, Header, Input, Label, Select, Static, TextArea

from src.ui.widgets.taskbar import Taskbar

# TODO: esto debe ser reemplazado por las categorías registradas.
CATEGORIES = [
    "Categoría 1",
    "Categoría 2",
    "Categoría 3",
]


# validaciones personalizadas.
class NotEmpty(Validator):
    def validate(self, value: str) -> ValidationResult:
        if not value.strip():
            return self.failure("Este campo no puede quedar vacío.")
        return self.success()


class StockCreateView(Screen):
    CSS_PATH = "styles/create-view.tcss"

    output_text = var("")

    # Se agregan variables reactivas para poder observar las validaciones
    item_code_valid = reactive(False)

    # variable reactiva para controlar el estado desabilitado del botón
    can_submit = reactive(False)

    def compose(self):
        yield Header()
        yield Grid(
            Taskbar(),
            VerticalScroll(
                Label("Selecciona una categoría", classes="styled-label"),
                Select(
                    ((category, category) for category in CATEGORIES),
                    id="category",
                    classes="styled-select",
                ),
                Static("Los campos cón * son obligatorios", classes="required-fields"),
                Label("Código de item *", classes="styled-label"),
                Input(
                    id="item_code",
                    placeholder="Ejemplo 003CA",
                    classes="styled-input",
                    validators=[NotEmpty(), Length(minimum=3, maximum=10)],
                ),
                Label("Nombre del producto *", classes="styled-label"),
                Input(
                    id="product_name",
                    placeholder="Escriba el nombre del producto",
                    classes="styled-input",
                    validators=[NotEmpty()],
                ),
                Label("Precio de compra *", classes="styled-label"),
                Input(
                    id="product_purchase_price",
                    placeholder="Ingrese el precio de compra solo números",
                    type="number",
                    classes="styled-input",
                    validators=[NotEmpty()],
                ),
                Label("Precio de precio venta *", classes="styled-label"),
                Input(
                    id="product_sale_price",
                    placeholder="Ingrese el precio de compra solo números",
                    type="number",
                    classes="styled-input",
                    validators=[NotEmpty()],
                ),
                Label("Cantidad de existencia *", classes="styled-label"),
                Input(
                    id="product_quantity",
                    placeholder="Ingrese la cantidad de existencia",
                    classes="styled-input",
                    type="number",
                    validators=[NotEmpty()],
                ),
                Label("Descripción", classes="styled-label"),
                TextArea(
                    id="product_description",
                    classes="styled-textarea",
                ),
                Label("Proveedor", classes="styled-label"),
                Input(
                    id="product_provider",
                    placeholder="Ingrese el proveedor del producto",
                    classes="styled-input",
                ),
                classes="form",
                id="form",
            ),
            Static(id="output_message", classes="styled-output"),
            Button(
                "Registrar producto",
                id="create_product",
                classes="styled-button",
                variant="primary",
            ),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        # capturamos todos los datos del producto para registrarlos
        if event.button.id == "create_product":
            output_widget = self.query_one("#output_message", Static)
            category = self.query_one("#category", Select).value
            item_code = self.query_one("#item_code", Input).value
            product_name = self.query_one("#product_name", Input).value
            product_purchase_price = self.query_one(
                "#product_purchase_price", Input
            ).value
            product_quantity = self.query_one("#product_quantity", Input).value
            product_description = self.query_one("#product_description", TextArea).text
            product_provider = self.query_one("#product_provider", Input).value
            if category and item_code and product_name and product_purchase_price:
                self.output_text = f"""[b green]Enviado[/]
                Categoría: {category}
                Nombre del producto: {product_name}
                Código de item: {item_code}
                Precio de compra: {product_purchase_price}
                Cantidad de existencia: {product_quantity}
                Descripción: {product_description}
                Proveedor: {product_provider}
                """
                output_widget.styles.border = ("ascii", "green")
            else:
                self.output_text = (
                    "[b red]Error:[/] Porfavor diligencie todos los campos obligatorios"
                )
                output_widget.styles.border = ("ascii", "red")

            log(self.output_text)

        # if event.button.id == "go_home":
        #     self.app.pop_screen()
        # elif event.button.id == "exit":
        #     self.app.exit()

    def watch_output_text(self, new_message: str) -> None:
        """Update the Static widget when output_text changes."""
        log("output text ....")
        output_widget = self.query_one("#output_message", Static)
        output_widget.update(new_message)

    # se usa el decorador on para capturar el evento
    # @on(Input.Changed, "#item_code")
    # def on_input_change(self, event: Input.Changed) -> None:
    #     log("inputting", event.value)
    #     status_widget = self.query_one("#status_message", Static)
    #     status_widget.update("Message...")
