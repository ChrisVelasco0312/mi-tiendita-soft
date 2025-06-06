from textual import log, on
from textual.reactive import reactive, var
from textual.containers import Container, Grid, Horizontal
from textual.screen import Screen
from textual.widgets import DataTable, Header, Input, Label
from rich.text import Text

from src.business.create_stock_controller import read_stock, search_stock
from src.business.stock_mapper import stock_mapper
from src.ui.widgets.taskbar import Taskbar


class CreateSellView(Screen):
    CSS_PATH = "styles/stock-manage-view.tcss"

    current_data = var(read_stock(""))
    sell_items = var([])  # Lista para almacenar items agregados a la venta

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compose(self):
        yield Header()
        yield Grid(
            Taskbar(id="manage_taskbar"),
            Container(
                Label("Buscar item", classes="manage-label"),
                Input(
                    id="search_by_code_input",
                    placeholder="Escribe el código del ítem",
                    classes="manage-input",
                ),
                classes="manage-container",
            ),
            Container(
                Label("Buscar por nombre", classes="manage-label"),
                Input(
                    id="search_by_name_input",
                    placeholder="Escribe el nombre del producto",
                    classes="manage-input",
                ),
                classes="manage-container",
            ),
            # Contenedor horizontal para ambas tablas
            Horizontal(
                Container(
                    Label("Inventario disponible", classes="manage-label"),
                    DataTable(id="stock_table", classes="manage-table"),
                    classes="table-container",
                ),
                Container(
                    Label("Productos a vender", classes="manage-label"),
                    DataTable(id="sell_table", classes="manage-table"),
                    classes="table-container",
                ),
                classes="tables-horizontal",
            ),
            classes="manage-grid",
            id="manage_grid",
        )

    def on_mount(self):
        self.load_stock_excel()
        self.setup_sell_table()

    def setup_sell_table(self):
        """Setup the sell table with appropriate columns."""
        sell_table = self.query_one("#sell_table", DataTable)
        sell_table.add_columns("Código", "Producto", "Precio", "Cantidad", "Total", "Reducir", "Quitar")

    def load_stock_excel(self):
        product_data = read_stock("")
        table = self.query_one("#stock_table", DataTable)

        columns = tuple(stock_mapper(product_data.columns))
        table.add_columns(*columns, "Agregar")

        for row in product_data.values:
            agregar_button = Text("Agregar", style="bold green underline")
            table.add_row(*tuple(row), agregar_button)

    def refresh_data(self):
        """Refresh the table data by reloading from the Excel file"""
        log("Refreshing stock data...")
        product_data = read_stock("")
        table = self.query_one("#stock_table", DataTable)
        
        # Limpia la tabla y recarga los datos
        table.clear()
        for row in product_data.values:
            agregar_button = Text("Agregar", style="bold green underline")
            table.add_row(*tuple(row), agregar_button)

    def add_product_to_sell(self, product_row):
        """Add a product to the sell table and reduce inventory."""
        sell_table = self.query_one("#sell_table", DataTable)
        stock_table = self.query_one("#stock_table", DataTable)
        
        # Extrae la información del producto según el mapeo correcto de columnas
        product_code = product_row[0]  # item_code
        product_name = product_row[2] if len(product_row) > 2 else "N/A"  # product_name
        product_price = product_row[5] if len(product_row) > 5 else 0.0  # sale_price
        available_quantity = int(product_row[3]) if len(product_row) > 3 else 0  # quantity
        
        # Verifica si hay suficiente inventario
        if available_quantity <= 0:
            self.notify(f"Sin inventario disponible para: {product_name}", severity="warning")
            return
        
        # Verifica si el producto ya existe en la tabla de ventas
        existing_row_key = None
        for row_key in sell_table.rows.keys():
            row_data = sell_table.get_row(row_key)
            if row_data[0] == product_code:  # Mismo código de producto
                existing_row_key = row_key
                break
        
        if existing_row_key:
            # Actualiza la cantidad y el total para el producto existente
            current_row = sell_table.get_row(existing_row_key)
            current_quantity = int(current_row[3]) + 1
            new_total = float(product_price) * current_quantity
            
            # Obtiene las claves de las columnas correctas
            columns = list(sell_table.columns.keys())
            cantidad_column_key = columns[3]  # "Cantidad"
            total_column_key = columns[4]     # "Total"
            
            # Actualiza la fila usando las claves de columna apropiadas
            sell_table.update_cell(existing_row_key, cantidad_column_key, str(current_quantity))
            sell_table.update_cell(existing_row_key, total_column_key, f"{new_total:.2f}")
        else:
            # Agrega un nuevo producto a la tabla de ventas
            quantity = 1
            total = float(product_price) * quantity
            reducir_button = Text("Reducir", style="bold yellow underline")
            quitar_button = Text("Quitar", style="bold red underline")
            
            sell_table.add_row(
                str(product_code),
                str(product_name),
                f"{product_price:.2f}",
                str(quantity),
                f"{total:.2f}",
                reducir_button,
                quitar_button
            )
        
        # Reduce la cantidad en el inventario (tabla de stock)
        self.reduce_stock_quantity(product_code, 1)
        
        # Actualiza la lista de items de la venta con los datos de la tabla
        self.update_sell_items()

    def reduce_stock_quantity(self, product_code, quantity_to_reduce):
        """Reduce the quantity in the stock table."""
        stock_table = self.query_one("#stock_table", DataTable)
        
        # Encuentra la fila del producto en el inventario
        for row_key in stock_table.rows.keys():
            row_data = stock_table.get_row(row_key)
            if row_data[0] == product_code:  # Mismo código de producto
                current_quantity = int(row_data[3])
                new_quantity = max(0, current_quantity - quantity_to_reduce)
                
                # Obtiene la clave de la columna de cantidad (índice 3)
                columns = list(stock_table.columns.keys())
                quantity_column_key = columns[3]
                
                # Actualiza la cantidad en el inventario
                stock_table.update_cell(row_key, quantity_column_key, str(new_quantity))
                break

    def increase_stock_quantity(self, product_code, quantity_to_add):
        """Increase the quantity in the stock table."""
        stock_table = self.query_one("#stock_table", DataTable)
        
        # Encuentra la fila del producto en el inventario
        for row_key in stock_table.rows.keys():
            row_data = stock_table.get_row(row_key)
            if row_data[0] == product_code:  # Mismo código de producto
                current_quantity = int(row_data[3])
                new_quantity = current_quantity + quantity_to_add
                
                # Obtiene la clave de la columna de cantidad (índice 3)
                columns = list(stock_table.columns.keys())
                quantity_column_key = columns[3]
                
                # Actualiza la cantidad en el inventario
                stock_table.update_cell(row_key, quantity_column_key, str(new_quantity))
                break

    def reduce_product_in_sell(self, row_key):
        """Reduce quantity of product in sell table by 1."""
        sell_table = self.query_one("#sell_table", DataTable)
        row_data = sell_table.get_row(row_key)
        product_code = row_data[0]
        product_name = row_data[1]
        product_price = float(row_data[2])
        current_quantity = int(row_data[3])
        
        if current_quantity > 1:
            # Reduce quantity by 1
            new_quantity = current_quantity - 1
            new_total = product_price * new_quantity
            
            # Obtiene las claves de las columnas correctas
            columns = list(sell_table.columns.keys())
            cantidad_column_key = columns[3]  # "Cantidad"
            total_column_key = columns[4]     # "Total"
            
            # Actualiza la fila
            sell_table.update_cell(row_key, cantidad_column_key, str(new_quantity))
            sell_table.update_cell(row_key, total_column_key, f"{new_total:.2f}")
            
            # Aumenta la cantidad en el inventario
            self.increase_stock_quantity(product_code, 1)
        else:
            # Si la cantidad es 1, elimina el producto completamente
            self.remove_product_from_sell(row_key)
        
        self.update_sell_items()

    def remove_product_from_sell(self, row_key):
        """Elimina el producto completamente de la tabla de ventas."""
        sell_table = self.query_one("#sell_table", DataTable)
        row_data = sell_table.get_row(row_key)
        product_code = row_data[0]
        product_name = row_data[1]
        quantity_to_return = int(row_data[3])
        
        # Devuelve toda la cantidad al inventario
        self.increase_stock_quantity(product_code, quantity_to_return)
        
        sell_table.remove_row(row_key)
        self.update_sell_items()

    def update_sell_items(self):
        """Actualiza la lista de items de la venta con los datos de la tabla"""
        sell_table = self.query_one("#sell_table", DataTable)
        items = []
        
        for row_key in sell_table.rows.keys():
            row_data = sell_table.get_row(row_key)
            items.append({
                'code': row_data[0],
                'name': row_data[1],
                'price': float(row_data[2]),
                'quantity': int(row_data[3]),
                'total': float(row_data[4])
            })
        
        self.sell_items = items

    # evento para buscar por item
    @on(Input.Changed, "#search_by_code_input")
    def on_code_input_change(self, event: Input.Changed) -> None:
        filtered_table = search_stock("item_code", event.value)
        if filtered_table.empty:
            product_data = self.current_data
            table = self.query_one("#stock_table", DataTable)
            table.clear()
            for row in product_data.values:
                agregar_button = Text("Agregar", style="bold green underline")
                table.add_row(*tuple(row), agregar_button)
        else:
            table = self.query_one("#stock_table", DataTable)
            table.clear()
            for row in filtered_table.values:
                agregar_button = Text("Agregar", style="bold green underline")
                table.add_row(*tuple(row), agregar_button)

    # evento para buscar por nombre
    @on(Input.Changed, "#search_by_name_input")
    def on_name_input_change(self, event: Input.Changed) -> None:
        product_data = self.current_data
        table = self.query_one("#stock_table", DataTable)
        filtered_table = search_stock("product_name", event.value)

        if filtered_table.empty:
            table.clear()
            for row in product_data.values:
                agregar_button = Text("Agregar", style="bold green underline")
                table.add_row(*tuple(row), agregar_button)
        else:
            table.clear()
            for row in filtered_table.values:
                agregar_button = Text("Agregar", style="bold green underline")
                table.add_row(*tuple(row), agregar_button)

    @on(DataTable.CellSelected)
    def on_cell_selected(self, event: DataTable.CellSelected) -> None:
        """Maneja la selección de celdas en ambas tablas."""
        # Determine which table was clicked
        table = event.data_table
        
        if table.id == "stock_table":
            # Maneja los clicks en la tabla de inventario (Agregar productos)
            last_column_index = len(table.columns) - 1
            
            if event.coordinate.column == last_column_index:
                # "Agregar" botón clickeado
                selected_row_data = table.get_row(event.cell_key.row_key)
                self.add_product_to_sell(selected_row_data)
                
        elif table.id == "sell_table":
            # Maneja los clicks en la tabla de ventas (Reducir/Eliminar productos)
            last_column_index = len(table.columns) - 1
            second_to_last_column_index = len(table.columns) - 2
            
            if event.coordinate.column == second_to_last_column_index:
                # "Reducir" button clicked
                self.reduce_product_in_sell(event.cell_key.row_key)
            elif event.coordinate.column == last_column_index:
                # "Quitar" button clicked
                self.remove_product_from_sell(event.cell_key.row_key) 
