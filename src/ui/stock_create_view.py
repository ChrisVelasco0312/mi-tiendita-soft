from datetime import datetime

from textual import log
from textual.containers import Grid, VerticalScroll
from textual.reactive import reactive, var
from textual.screen import Screen
from textual.validation import ValidationResult, Validator
from textual.widgets import Button, Header, Input, Label, Select, Static

from src.business.category_controller import get_all_categories 
from src.business.create_stock_controller import create_item_code, create_stock_product, update_stock_product
from src.ui.widgets.taskbar import Taskbar
from src.ui.stock_update_message import StockUpdateMessage, StockDataRefreshMessage

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
    
    current_stock_item = reactive({
        "item_code" :"",
        "category": "",
        "product_name" : "",
        "purchase_price": "",
        "sale_price": 0,
        "quantity": 0,
        "creation_date": "",
        "edit_mode": False
    })

    # Se agregan variables reactivas para poder observar las validaciones
    item_code_valid = reactive(False)

    # variable reactiva para controlar el estado desabilitado del botón
    can_submit = reactive(False)

    def __init__(self):
        super().__init__(id="stock_create_view")
        self.data = {}

    def compose(self):
        yield Header()
        yield Grid(
            Taskbar(id="create_taskbar"),
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
            id="create_grid",
        )

    def watch_current_stock_item(self, old_value, new_value):
        """Watch for changes in current_stock_item reactive variable"""
        if new_value["edit_mode"] and self.is_mounted:
            log(f"Edit mode activated for item: {new_value['item_code']}")
            self.query_one("#product_name", Input).value = str(new_value["product_name"])
            self.query_one("#product_purchase_price", Input).value = str(new_value["purchase_price"])
            self.query_one("#product_sale_price", Input).value = str(new_value["sale_price"])
            self.query_one("#product_quantity", Input).value = str(new_value["quantity"])
            self.query_one("#category", Select).value = str(new_value["category"])

    def on_mount(self):
        """Handle screen mounting and populate fields if in edit mode"""
        if self.current_stock_item["edit_mode"]:
            log(f"Mounting in edit mode for item: {self.current_stock_item['item_code']}")
            self.query_one("#product_name", Input).value = str(self.current_stock_item["product_name"])
            self.query_one("#product_purchase_price", Input).value = str(self.current_stock_item["purchase_price"])
            self.query_one("#product_sale_price", Input).value = str(self.current_stock_item["sale_price"])
            self.query_one("#product_quantity", Input).value = str(self.current_stock_item["quantity"])
            self.query_one("#category", Select).value = str(self.current_stock_item["category"])
            
            # Update the button text to indicate edit mode
            button = self.query_one("#create_product", Button)
            button.label = "Actualizar producto"

    def on_screen_suspend(self):
        self.current_stock_item["edit_mode"] = False
        button = self.query_one("#create_product", Button)
        button.label = "Registrar producto"
        self.clean_data()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        # capturamos todos los datos del producto para registrarlos
        if event.button.id == "create_product":
            output_widget = self.query_one("#output_message", Static)
            category = self.query_one("#category", Select).value
            item_code = ""

            # se valida si la categoria ha sido seleccionada
            if isinstance(category, str):
                item_code = create_item_code(category)

            product_name = self.query_one("#product_name", Input).value
            product_purchase_price = self.query_one(
                "#product_purchase_price", Input
            ).value
            product_sale_price = self.query_one("#product_sale_price", Input).value
            product_quantity = self.query_one("#product_quantity", Input).value

            # detectamos si los campos han sido llenados
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
                if self.current_stock_item["edit_mode"]:
                    # Handle edit mode - update existing product
                    update_product_data = {
                        "item_code": self.current_stock_item["item_code"],
                        "category": category,
                        "product_name": product_name,
                        "quantity": product_quantity,
                        "purchase_price": product_purchase_price,
                        "sale_price": product_sale_price,
                        "creation_date": datetime.now()
                    }
                    log(f"Update mode: {update_product_data}")
                    update_stock_product(update_product_data)
                    
                    # Post message to refresh stock data in other views
                    self.post_message(StockDataRefreshMessage())
                    
                    # self.app.stock_data_message = f"Producto '{product_name}' actualizado correctamente"
                    
                    self.notify("Producto actualizado correctamente!")
                    self.app.pop_screen()
                else:
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
                    
                    # Actualiza mensaje de éxito
                    self.app.stock_data_message = f"Producto '{product_name}' creado correctamente"
                    
                    self.app.push_screen("notification_modal")
                    self.app.refresh()
                    self.clean_data()

            else:
                self.output_text = (
                    "[b red]Error:[/] Porfavor diligencie todos los campos obligatorios"
                )
                output_widget.styles.border = ("ascii", "red")

            log(self.output_text)

    def set_edit_data(self, data):
        """Set the edit data and populate form fields"""
        log(f"Setting edit data: {data}")
        
        # Convert numpy types to Python native types
        item_code = str(data.get("item_code", ""))
        category = str(data.get("category", ""))
        product_name = str(data.get("product_name", ""))
        purchase_price = str(data.get("purchase_price", ""))
        sale_price = int(data.get("sale_price", 0)) if data.get("sale_price") else 0
        quantity = int(data.get("quantity", 0)) if data.get("quantity") else 0
        creation_date = str(data.get("creation_date", ""))
        
        # Update the reactive state to indicate edit mode
        self.current_stock_item = {
            "item_code": item_code,
            "category": category,
            "product_name": product_name,
            "purchase_price": purchase_price,
            "sale_price": sale_price,
            "quantity": quantity,
            "creation_date": creation_date,
            "edit_mode": True
        }

        # Store the item code for later use
        self.edit_item_code = item_code

    def clean_data(self) -> None:
        self.query_one("#category", Select).clear()
        self.query_one("#product_name", Input).clear()
        self.query_one("#product_purchase_price", Input).clear()
        self.query_one("#product_sale_price", Input).clear()
        self.query_one("#product_quantity", Input).clear()

        # Reset the output widget
        output_widget = self.query_one("#output_message", Static)
        output_widget.update("")
        output_widget.styles.border = None
        item_code_valid = True
