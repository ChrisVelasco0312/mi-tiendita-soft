from textual import log, on
from textual.containers import Grid, VerticalScroll
from textual.reactive import reactive, var
from textual.screen import Screen
from textual.validation import Integer, Length, Regex, ValidationResult, Validator
from textual.widgets import Button, Header, Input, Label, Select, Static, TextArea
from src.business.create_stock_controller import create_stock_product, read_categories

from src.ui.widgets.taskbar import Taskbar

# TODO: esto debe ser reemplazado por las categorías registradas.





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

        def categorias(self):
            categorias = read_categories() or ["Sin categoría"]
            print(f"Categorías cargadas: {categorias}")  # <- Esto debe verse en la terminal
            return categorias

        
        yield Header()
        yield Grid(
            Taskbar(),
            VerticalScroll(
                Static("Los campos cón * son obligatorios", classes="required-fields"),
                Label("Código de item *", classes="styled-label"),
                Input(
                    id="item_code",
                    placeholder="Ejemplo 003CA",
                    classes="styled-input",
                    validators=[NotEmpty(), Length(minimum=3, maximum=10)],
                ),
                
                # Pruebas de cargar categorias del documento excel.
                Label("Selecciona una categoría", classes="styled-label"),
                Select(
                    ((categoria, categoria) for categoria in read_categories() or ["Sin categoría"]),
                     id="categoria",  
                     classes="styled-select",
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
        if event.button.id == "create_product":
            output_widget = self.query_one("#output_message", Static)

            # Captura los datos requeridos en el formulario.
            category = self.query_one("#category", Select).value
            item_code = self.query_one("#item_code", Input).value
            product_name = self.query_one("#product_name", Input).value
            product_purchase_price = self.query_one("#product_purchase_price", Input).value
            product_sale_price = self.query_one("#product_sale_price", Input).value
            product_quantity = self.query_one("#product_quantity", Input).value
            product_description = self.query_one("#product_description", TextArea).text
            product_provider = self.query_one("#product_provider", Input).value

            # Se verifica que los campos requeridos estén.
            if all([category, item_code, product_name, product_purchase_price, product_sale_price, product_quantity]):
                try:
                    # Creacion de un nuevo producto
                    create_stock_product({
                        "item_code": item_code,
                        "product_name": product_name,
                        "category": category,
                        "purchase_price": float(product_purchase_price),
                        "sale_price": float(product_sale_price),
                        "quantity": int(product_quantity),
                        "description": product_description,
                        "provider": product_provider,
                    })

                    self.output_text = "[b green]Producto registrado correctamente.[/]"
                    output_widget.styles.border = ("ascii", "green")

                    # Opcional: limpiar los campos luego de registrar
                    self.clear_form()

                except ValueError as e:
                    self.output_text = f"[b red]Error:[/] {str(e)}"
                    output_widget.styles.border = ("ascii", "red")

                except Exception as e:
                    self.output_text = "[b red]Error:[/] No se pudo registrar el producto."
                    log(str(e))
                    output_widget.styles.border = ("ascii", "red")
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
