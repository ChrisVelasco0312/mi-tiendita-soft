from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Button, DataTable, Input
from textual.reactive import reactive
from textual import events
import csv, os
from datetime import datetime
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter


# Ruta al archivo Excel en la carpeta "src/business/data"
EXCEL_PATH = os.path.join("src", "business", "data", "product_stock_data.xlsx")


# Datos de prueba para ventas
PRODUCTOS = [
    {"id": 1, "nombre": "Pan", "cantidad": 20, "vendido": 50, "precio": 2000, "fecha_venta": "2025-05-10"},
    {"id": 2, "nombre": "Leche", "cantidad": 10, "vendido": 80, "precio": 1500, "fecha_venta": "2025-05-14"},
    {"id": 3, "nombre": "Huevos", "cantidad": 5, "vendido": 120, "precio": 600, "fecha_venta": "2025-05-13"},
]


class CreateSellView(Screen):
    codigo = reactive("")
    cantidad = reactive("")
    total = reactive("0")
    producto = reactive(None)

    def compose(self):
        self.codigo_input = Input(placeholder="Código del ítem", id="codigo")
        self.cantidad_input = Input(placeholder="Cantidad a vender", id="cantidad")
        self.total_display = Static("Total a pagar: $0.00", id="total")
        self.detalles_producto = Static("", id="detalles")
        self.mensaje_resultado = Static("", id="mensaje")

        yield Container(
            Horizontal(
                Button("Volver", id="volver"),
                Button("Realizar Venta", id="realizar_venta")
            ),
            Static("Generar Nueva Venta"),
            self.codigo_input,
            self.detalles_producto,
            self.cantidad_input,
            self.total_display,
            self.mensaje_resultado
        )

    def on_input_submitted(self, event: Input.Submitted):
        if event.input.id == "codigo":
            try:
                pid = int(event.value)
                for p in PRODUCTOS:
                    if p["id"] == pid:
                        self.producto = p
                        self.detalles_producto.update(
                            f"Nombre: {p['nombre']} | Disponible: {p['cantidad']} | Precio: ${p['precio']:.2f}"
                        )
                        break
                else:
                    self.producto = None
                    self.detalles_producto.update("Producto no encontrado.")
            except ValueError:
                self.detalles_producto.update("Código inválido.")

        elif event.input.id == "cantidad":
            if self.producto:
                try:
                    cant = int(event.value)
                    total = cant * self.producto["precio"]
                    self.total = f"{total:.2f}"
                    self.cantidad = str(cant)
                    self.total_display.update(f"Total a pagar: ${self.total}")
                except ValueError:
                    self.total_display.update("Cantidad inválida.")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "volver":
            self.app.pop_screen()

        elif event.button.id == "realizar_venta":
            if self.producto and self.cantidad.isdigit():
                cantidad_vendida = int(self.cantidad)
                if cantidad_vendida <= self.producto["cantidad"]:
                    fecha_venta_actual = datetime.now().strftime("%Y-%m-%d")

                    self.producto["cantidad"] -= cantidad_vendida
                    self.producto["vendido"] += cantidad_vendida
                    self.producto["fecha_venta"] = fecha_venta_actual

                    # Crear carpeta si no existe
                    os.makedirs(os.path.dirname(EXCEL_PATH), exist_ok=True)

                    # Guardar en Excel en la pagina "SalesData"
                    if os.path.exists(EXCEL_PATH):
                        wb = load_workbook(EXCEL_PATH)
                    else:
                        wb = Workbook()

                    if "SalesData" in wb.sheetnames:
                        ws = wb["SalesData"]
                    else:
                        ws = wb.create_sheet("SalesData")

                    # Escribir encabezado si está vacío
                    if ws.max_row == 1 and ws.cell(row=1, column=1).value is None:
                        ws.append(["ID", "Nombre", "Cantidad Vendida", "Total", "Fecha de Venta"])

                    ws.append([
                        self.producto["id"],
                        self.producto["nombre"],
                        cantidad_vendida,
                        float(self.total),
                        fecha_venta_actual
                    ])

                    wb.save(EXCEL_PATH)

                    self.mensaje_resultado.update("Venta realizada exitosamente.")
                else:
                    self.mensaje_resultado.update("Cantidad mayor a stock disponible.")
            else:
                self.mensaje_resultado.update("Datos incompletos para realizar la venta.")