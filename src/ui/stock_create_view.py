from datetime import datetime

from textual import log
from textual.containers import Grid, VerticalScroll
from textual.reactive import reactive, var
from textual.screen import Screen
from textual.validation import ValidationResult, Validator
from textual.widgets import Button, Header, Input, Label, Select, Static

from src.business.category_controller import get_all_categories
from src.business.create_stock_controller import create_item_code, create_stock_product
from src.ui.widgets.taskbar import Taskbar

CATEGORIES = get_all_categories()


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
                Static("Todos los campos son obligatorios", classes="required-fields"),
                Label("Selecciona una categoría", classes="styled-label"),
                Select(
                    ((category, category) for category in CATEGORIES),
                    id="category",
                    classes="styled-select",
                ),
                Label("Nombre del producto", classes="styled-label"),
                Input(
                    id="product_name",
                    placeholder="Escriba el nombre del producto",
                    classes="styled-input",
                    validators=[NotEmpty()],
                ),
                Label("Precio de compra", classes="styled-label"),
                Input(
                    id="product_purchase_price",
                    placeholder="Ingrese el precio de compra solo números",
                    type="number",
                    classes="styled-input",
                    validators=[NotEmpty()],
                ),
                Label("Precio de precio venta", classes="styled-label"),
                Input(
                    id="product_sale_price",
                    placeholder="Ingrese el precio de compra solo números",
                    type="number",
                    classes="styled-input",
                    validators=[NotEmpty()],
                ),
                Label("Cantidad de existencia", classes="styled-label"),
                Input(
                    id="product_quantity",
                    placeholder="Ingrese la cantidad de existencia",
                    classes="styled-input",
                    type="number",
                    validators=[NotEmpty()],
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
            item_code = ""
            if isinstance(category, str):
                item_code = create_item_code(category)
            product_name = self.query_one("#product_name", Input).value
            product_purchase_price = self.query_one(
                "#product_purchase_price", Input
            ).value
            product_sale_price = self.query_one("#product_sale_price", Input).value
            product_quantity = self.query_one("#product_quantity", Input).value
            if all(
                [
                    isinstance(category, str),
                    item_code,
                    product_name,
                    product_purchase_price,
                    product_sale_price,
                    product_quantity,
                ]
            ):
                new_product_data = [
                    {
                        "item_code": item_code,
                        "category": category,
                        "product_name": product_name,
                        "quantity": product_quantity,
                        "purchase_price": product_purchase_price,
                        "sale_price": product_sale_price,
                        "creation_date": datetime.now(),
                    }
                ]

                create_stock_product(new_product_data)
                self.app.push_screen("notification_modal")

                output_text = "[b green]Enviado[/]"

                data_message = (
                    f"Producto Creado Con Éxito Item: {item_code} {product_name}"
                )
                self.app.stock_data_message = data_message.strip()
                self.output_text = output_text
                output_widget.styles.border = ("ascii", "green")
                self.app.refresh()
                self.clean_data()
                self.output_text = ""
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

    def clean_data(self) -> None:
        self.query_one("#category", Select).clear()
        self.query_one("#product_name", Input).clear()
        self.query_one("#product_purchase_price", Input).clear()
        self.query_one("#product_sale_price", Input).clear()
        self.query_one("#product_quantity", Input).clear()

    # se usa el decorador on para capturar el evento
    # @on(Input.Changed, "#item_code")
    # def on_input_change(self, event: Input.Changed) -> None:
    #     log("inputting", event.value)
    #     status_widget = self.query_one("#status_message", Static)
    #     status_widget.update("Message...")
