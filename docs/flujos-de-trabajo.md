# Flujos de Trabajo del Sistema

## Visión General

Este documento describe los flujos de trabajo principales del sistema Mi Tiendita Soft, detallando paso a paso cómo se ejecutan las operaciones críticas del negocio.

## 1. Inicialización del Sistema

### Flujo de Arranque

```mermaid
flowchart TD
    A["Usuario ejecuta main.py"] --> B["Aplicación llama initialiaze_operations()"]
    B --> C{"Existen archivos Excel?"}
    C -->|NO| D["Crear archivos con datos ejemplo"]
    C -->|SÍ| E["Cargar configuración existente"]
    D --> F["Registrar todas las pantallas (screens)"]
    E --> F
    F --> G["Mostrar HomeView (pantalla principal)"]
```

### Inicialización de Base de Datos

**Ubicación:** `src/business/create_stock_controller.py:initialiaze_operations()`

1. **Verificación de archivos**

   ```python
   if os.path.exists(STOCK_FILE_PATH):
       return "La base de datos ya ha sido creada"
   ```

2. **Creación de datos iniciales** (si no existen)

   - **Productos ejemplo:** 4 productos en categoría "Alimentos y bebidas"
   - **Categorías:** 7 categorías predefinidas del sistema
   - **Ventas:** Archivo vacío listo para registros

3. **Archivos creados:**
   - `product_stock_data.xlsx`: Inventario con productos ejemplo
   - `category_data.xlsx`: Categorías del sistema
   - `sell_data.xlsx`: Base de datos de ventas (vacía)

## 2. Gestión de Inventario

```mermaid
flowchart TD
    A["Usuario accede al Sistema de Inventario"] --> B{"Seleccionar operación"}

    B -->|Registrar Producto| C["Navegar a StockCreateView"]
    C --> D["Formulario de Registro"]
    D --> E["Seleccionar categoría del dropdown"]
    E --> F["Ingresar datos del producto<br/>(nombre, cantidad, precios)"]
    F --> G["Generar código automático<br/>create_item_code(category)"]
    G --> H["Validar datos del formulario"]
    H --> I{"Datos válidos?"}
    I -->|NO| J["Mostrar errores de validación"]
    I -->|SÍ| K["Crear DataFrame con nuevo producto"]
    K --> L["Guardar en Excel<br/>product_stock_data.xlsx"]
    L --> M["Enviar StockDataRefreshMessage"]
    M --> N["Mostrar confirmación de registro"]

    B -->|Consultar/Gestionar| O["Navegar a StockManageView"]
    O --> P["Cargar inventario completo<br/>refresh_data()"]
    P --> Q["Mostrar tabla interactiva"]
    Q --> R{"Acción del usuario"}

    R -->|Buscar| S["Ingresar criterio de búsqueda"]
    S --> T{"Tipo de búsqueda"}
    T -->|Por código| U["Búsqueda exacta"]
    T -->|Por nombre| V["Búsqueda parcial"]
    U --> W["Filtrar tabla en tiempo real"]
    V --> W
    W --> Q

    R -->|Editar| X["Seleccionar producto de la tabla"]
    X --> Y["Enviar StockUpdateMessage"]
    Y --> Z["Navegar a StockCreateView<br/>(modo edición)"]
    Z --> AA["Pre-cargar formulario con datos"]
    AA --> AB["Modificar datos necesarios"]
    AB --> AC["Confirmar actualización"]
    AC --> AD["Actualizar base de datos"]
    AD --> AE["Refrescar vista de gestión"]

    R -->|Eliminar| AF["Seleccionar producto"]
    AF --> AG["Mostrar modal de confirmación"]
    AG --> AH{"Confirmar eliminación?"}
    AH -->|NO| AI["Cancelar operación"]
    AH -->|SÍ| AJ["delete_stock_product()"]
    AJ --> AK["Actualizar Excel"]
    AK --> AL["Refrescar vista automáticamente"]

    J --> F
    N --> AM["Continuar operaciones"]
    AI --> Q
    AL --> Q
    AE --> Q
    AM --> B
```

### 2.1 Registro de Nuevo Producto

**Vista:** `StockCreateView`
**Controlador:** `create_stock_controller.py`

#### Flujo Paso a Paso

1. **Navegación**

   ```
   HomeView → Botón "Registro de Inventario" → StockCreateView
   ```

2. **Formulario de Registro**

   - Usuario selecciona categoría del dropdown
   - Ingresa nombre del producto
   - Especifica cantidad inicial
   - Define precio de compra y venta

3. **Generación Automática de Código**

   ```python
   def create_item_code(category_name: str):
       # Extrae iniciales: "Alimentos y Bebidas" → "AYB"
       item_letters = "".join([word[0] for word in category_name.split()]).upper()

       # Busca último consecutivo de la categoría
       filtered_data = search_data_by_field(STOCK_FILE_PATH, SHEET_NAME, "category", category_name)

       if not filtered_data.empty:
           last_code = filtered_data["item_code"].iloc[-1]
           consecutive_num = re.findall(r"\d+", last_code)[0]
           new_consecutive = int(consecutive_num) + 1
           return f"{new_consecutive}{item_letters}"
       else:
           return f"1{item_letters}"
   ```

4. **Validación de Datos**

   - Precios deben ser positivos
   - Cantidad debe ser válida
   - Nombre no puede estar vacío
   - Categoría debe existir

5. **Persistencia**

   ```python
   def create_stock_product(data):
       # Crear DataFrame con nuevo producto
       df_new_product = pd.DataFrame(data)

       # Leer datos actuales
       df_current_stock_data = read_excel_data(STOCK_FILE_PATH, SHEET_NAME, "")

       # Combinar datos
       df_combined_data = pd.concat([df_current_stock_data, df_new_product])

       # Guardar en Excel
       df_combined_data.to_excel(STOCK_FILE_PATH, sheet_name=SHEET_NAME, index=False)
   ```

6. **Notificación**
   - Envía `StockDataRefreshMessage`
   - Actualiza automáticamente `StockManageView` si está abierta
   - Muestra confirmación al usuario

#### Ejemplo de Generación de Códigos

| Categoría           | Primera vez | Segunda vez | Tercera vez |
| ------------------- | ----------- | ----------- | ----------- |
| Alimentos y bebidas | 1AYB        | 2AYB        | 3AYB        |
| Aseo personal       | 1AP         | 2AP         | 3AP         |
| Dulcería            | 1D          | 2D          | 3D          |

### 2.2 Consulta y Gestión de Inventario

**Vista:** `StockManageView`

```mermaid
flowchart TD
    A["Usuario navega a StockManageView"] --> B["on_mount(): Cargar todos los productos<br/>refresh_data()"]
    B --> C["Mostrar tabla con inventario completo"]
    C --> D["Usuario decide acción"]
    D --> E{"Tipo de acción"}

    E -->|Búsqueda| F["Usuario ingresa criterio de búsqueda"]
    F --> G{"Tipo de búsqueda"}
    G -->|Por código| H["Búsqueda exacta por item_code<br/>(ej: '1AYB')"]
    G -->|Por nombre| I["Búsqueda parcial en product_name"]
    H --> J["Actualizar tabla en tiempo real"]
    I --> J
    J --> K["Mostrar resultados filtrados"]
    K --> D

    E -->|Editar| L["Usuario selecciona fila en tabla"]
    L --> M["Presiona Enter o botón Editar"]
    M --> N["get_selected_row_data()<br/>Obtener datos del producto"]
    N --> O["Enviar StockUpdateMessage<br/>con payload de datos"]
    O --> P["Navegar a StockCreateView<br/>(modo edición)"]
    P --> Q["Pre-cargar formulario con datos"]
    Q --> R["Cambiar botón a 'Actualizar'"]
    R --> S["Usuario modifica datos"]
    S --> T["Confirmar actualización"]
    T --> U["Actualizar base de datos Excel"]
    U --> V["Enviar StockDataRefreshMessage"]
    V --> W["Actualizar StockManageView"]
    W --> X["Mostrar confirmación"]

    E -->|Eliminar| Y["Usuario selecciona producto"]
    Y --> Z["Presiona botón 'Eliminar'"]
    Z --> AA["Mostrar modal de confirmación"]
    AA --> BB{"Usuario confirma eliminación?"}
    BB -->|NO| CC["Cancelar eliminación"]
    BB -->|SÍ| DD["delete_stock_product(item_code)"]
    DD --> EE["Buscar índice del producto<br/>en DataFrame"]
    EE --> FF["Eliminar fila con drop()"]
    FF --> GG["Guardar DataFrame actualizado<br/>en Excel"]
    GG --> HH["Actualizar vista automáticamente"]
    HH --> II["Mostrar confirmación de eliminación"]

    X --> JJ["Volver a vista de gestión"]
    CC --> D
    II --> D
    JJ --> D
```

**Detalles de implementación:**

#### Flujo de Consulta

1. **Carga Inicial**

   ```python
   def on_mount(self):
       self.refresh_data()  # Carga todos los productos
   ```

2. **Búsqueda**

   - **Por código:** Ingresa código exacto (ej: "1AYB")
   - **Por nombre:** Búsqueda parcial en nombre del producto
   - **Resultado inmediato:** Se actualiza tabla en tiempo real

3. **Visualización**
   - Tabla interactiva con DataTable de Textual
   - Columnas: Código, Categoría, Nombre, Cantidad, Precios
   - Navegación con teclado (flechas, Tab, Enter)

#### Comunicación Entre Vistas

```python
def on_data_table_row_selected(self, event):
    # Obtiene datos del producto seleccionado
    row_data = self.get_selected_row_data()

    # Envía mensaje con datos para edición
    self.post_message(StockUpdateMessage(payload=row_data))
```

#### Eliminación de Productos

```python
def delete_stock_product(item_code: str):
    df_current_stock_data = read_excel_data(STOCK_FILE_PATH, SHEET_NAME, "")
    item_index = df_current_stock_data[df_current_stock_data["item_code"] == item_code].index
    deleted_db = df_current_stock_data.drop(item_index)
    deleted_db.to_excel(STOCK_FILE_PATH, sheet_name=SHEET_NAME, index=False)
```

## 3. Gestión de Ventas

### 3.1 Proceso de Venta

**Vista:** `CreateSellView`
**Controlador:** `sell_controller.py`

#### Flujo Completo de Venta

```mermaid
flowchart TD
    A["Usuario navega a 'Generar Venta'"] --> B["CreateSellView se inicializa"]
    B --> C["Inicializar carrito vacío"]
    C --> D["Usuario ingresa código de producto"]
    D --> E["Sistema busca producto por código"]
    E --> F{"Producto encontrado?"}
    F -->|NO| G["Mostrar error:<br/>'Producto no encontrado'"]
    F -->|SÍ| H["Verificar stock disponible"]
    H --> I{"Stock suficiente?"}
    I -->|NO| J["Mostrar error:<br/>'Stock insuficiente'"]
    I -->|SÍ| K["Validar cantidad solicitada"]
    K --> L{"Cantidad válida?"}
    L -->|NO| M["Mostrar error:<br/>'Cantidad inválida'"]
    L -->|SÍ| N["Crear item del carrito<br/>{code, name, quantity, price, subtotal}"]
    N --> O["Agregar item al carrito"]
    O --> P["Actualizar visualización del carrito"]
    P --> Q["Calcular total automático<br/>sum(item.subtotal)"]
    Q --> R["¿Agregar más productos?"]
    R -->|SÍ| D
    R -->|NO| S{"Carrito vacío?"}
    S -->|SÍ| T["Mostrar error:<br/>'Carrito vacío'"]
    S -->|NO| U["Usuario presiona 'Confirmar Venta'"]
    U --> V["Mostrar modal de confirmación"]
    V --> W{"Usuario confirma?"}
    W -->|NO| X["Cancelar proceso"]
    W -->|SÍ| Y["Preparar datos de venta"]
    Y --> Z["Registrar venta en base de datos"]
    Z --> AA["Actualizar inventario<br/>reducir stock de productos"]
    AA --> BB["Mostrar confirmación de venta"]
    BB --> CC["Limpiar carrito"]
    G --> D
    J --> D
    M --> D
    T --> D
    X --> R
```

**Detalles de implementación:**

1. **Validación de Producto**

   ```python
   # Buscar producto por código
   product_data = search_stock("item_code", product_code)

   if product_data.empty:
       show_error("Producto no encontrado")
       return

   # Verificar stock disponible
   available_stock = product_data.iloc[0]["quantity"]
   if requested_quantity > available_stock:
       show_error(f"Stock insuficiente. Disponible: {available_stock}")
       return
   ```

2. **Agregado al Carrito**

   ```python
   cart_item = {
       "code": product_code,
       "name": product_name,
       "quantity": requested_quantity,
       "unit_price": sale_price,
       "subtotal": sale_price * requested_quantity
   }

   self.cart_items.append(cart_item)
   self.update_cart_display()
   self.calculate_total()
   ```

3. **Cálculo Automático**

   ```python
   def calculate_total(self):
       total = sum(item["subtotal"] for item in self.cart_items)
       self.total_label.update(f"Total: ${total:,}")
   ```

4. **Procesamiento Final**

   ```python
   def process_sale(self):
       # Preparar datos de venta
       sale_data = {
           "items": ",".join([item["code"] for item in self.cart_items]),
           "quantities": ",".join([str(item["quantity"]) for item in self.cart_items]),
           "total": self.total_amount
       }

       # Registrar venta
       sell_controller.create_sell([sale_data])

       # Actualizar inventario
       for item in self.cart_items:
           update_stock_after_sale(item["code"], item["quantity"])
   ```

#### Validaciones Durante la Venta

- **Producto existe:** Verificación en base de datos
- **Stock suficiente:** Cantidad solicitada ≤ stock disponible
- **Cantidades válidas:** Números positivos y enteros
- **Carrito no vacío:** Mínimo un producto para procesar

### 3.2 Consulta de Ventas

**Vista:** `ManageSellView`

#### Flujo de Consulta

```mermaid
flowchart TD
    A["Usuario navega a ManageSellView"] --> B["on_mount(): Cargar datos de ventas"]
    B --> C["Aplicar filtro por defecto: 'hoy'"]
    C --> D["Usuario selecciona filtro temporal"]
    D --> E{"Tipo de filtro"}
    E -->|hoy| F["Filtrar ventas de hoy<br/>sales_data.date == today"]
    E -->|ayer| G["Filtrar ventas de ayer<br/>sales_data.date == yesterday"]
    E -->|7_dias| H["Filtrar últimos 7 días<br/>sales_data.date >= week_ago"]
    E -->|30_dias| I["Filtrar últimos 30 días<br/>sales_data.date >= month_ago"]
    F --> J["Formatear detalles de venta"]
    G --> J
    H --> J
    I --> J
    J --> K["Parsear productos y cantidades<br/>items.split(','), quantities.split(',')"]
    K --> L["Crear descripción legible<br/>product_name x quantity"]
    L --> M["Calcular totales del período"]
    M --> N["Mostrar estadísticas<br/>Total ventas y monto"]
    N --> O["Actualizar tabla con datos filtrados"]
```

**Detalles de implementación:**

1. **Carga Inicial**

   ```python
   def on_mount(self):
       self.load_sales_data()
       self.apply_filter("hoy")  # Filtro por defecto
   ```

2. **Filtros Temporales**

   ```python
   def apply_date_filter(self, filter_type: str):
       today = datetime.now().date()

       if filter_type == "hoy":
           filtered_sales = sales_data[sales_data["date"].dt.date == today]
       elif filter_type == "ayer":
           yesterday = today - timedelta(days=1)
           filtered_sales = sales_data[sales_data["date"].dt.date == yesterday]
       elif filter_type == "7_dias":
           week_ago = today - timedelta(days=7)
           filtered_sales = sales_data[sales_data["date"].dt.date >= week_ago]
       elif filter_type == "30_dias":
           month_ago = today - timedelta(days=30)
           filtered_sales = sales_data[sales_data["date"].dt.date >= month_ago]
   ```

3. **Visualización Detallada**

   ```python
   def format_sale_details(self, sale_row):
       # Parsear productos vendidos
       items = sale_row["items"].split(",")
       quantities = sale_row["quantities"].split(",")

       # Crear descripción legible
       details = []
       for item_code, qty in zip(items, quantities):
           product_name = self.get_product_name(item_code)
           details.append(f"{product_name} x{qty}")

       return " | ".join(details)
   ```

4. **Cálculo de Totales**

   ```python
   def calculate_period_totals(self, filtered_sales):
       total_sales = len(filtered_sales)
       total_amount = filtered_sales["total"].sum()

       self.stats_label.update(
           f"Ventas: {total_sales} | Total: ${total_amount:,}"
       )
   ```

## 4. Comunicación Entre Componentes

### Sistema de Mensajes

**Arquitectura:** Observer Pattern usando mensajes de Textual

#### Mensajes Disponibles

```python
class StockUpdateMessage(Message):
    """Notifica que se debe editar un producto específico"""
    def __init__(self, payload: dict) -> None:
        self.payload = payload  # Datos del producto a editar
        super().__init__()

class StockDataRefreshMessage(Message):
    """Solicita actualización de datos de inventario"""
    pass
```

#### Flujo de Comunicación

1. **Envío de Mensaje**

   ```python
   # Desde StockManageView
   self.post_message(StockUpdateMessage(payload=product_data))
   ```

2. **Recepción en Aplicación Principal**

   ```python
   # En MiTienditaApp
   def on_stock_update_message(self, message: StockUpdateMessage) -> None:
       stock_screen = self.get_screen("stock_register_view")
       if hasattr(stock_screen, "set_edit_data"):
           stock_screen.set_edit_data(message.payload)
       self.push_screen("stock_register_view")
   ```

3. **Procesamiento en Vista Destino**
   ```python
   # En StockCreateView
   def set_edit_data(self, data: dict):
       self.edit_mode = True
       self.category_select.value = data["category"]
       self.name_input.value = data["product_name"]
       # ... llenar otros campos
   ```

## 5. Manejo de Errores y Validaciones

### Validaciones en Tiempo Real

#### Formulario de Productos

```python
def validate_price_input(self, value: str) -> bool:
    try:
        price = float(value)
        return price > 0
    except ValueError:
        return False

def on_input_changed(self, event):
    if not self.validate_price_input(event.value):
        self.show_validation_error("El precio debe ser un número positivo")
```

#### Proceso de Venta

```python
def validate_sale_item(self, product_code: str, quantity: int) -> tuple[bool, str]:
    # Verificar que el producto existe
    product = search_stock("item_code", product_code)
    if product.empty:
        return False, "Producto no encontrado"

    # Verificar stock disponible
    available = product.iloc[0]["quantity"]
    if quantity > available:
        return False, f"Stock insuficiente. Disponible: {available}"

    return True, "OK"
```

### Manejo de Excepciones

```python
def safe_excel_operation(operation_func, *args, **kwargs):
    try:
        return operation_func(*args, **kwargs)
    except FileNotFoundError:
        logger.error("Archivo de base de datos no encontrado")
        return None
    except PermissionError:
        logger.error("Sin permisos para acceder al archivo")
        return None
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        return None
```

## 6. Diagrama de flujo de toda la aplicación

```mermaid
flowchart TD
    %% System Initialization
    A["Usuario ejecuta main.py"] --> B["Aplicación llama initialize_operations()"]
    B --> C{"Existen archivos Excel?"}
    C -->|NO| D["Crear archivos con datos ejemplo"]
    C -->|SÍ| E["Cargar configuración existente"]
    D --> F["Registrar todas las pantallas"]
    E --> F
    F --> G["Mostrar HomeView"]

    %% Main Menu
    G --> H{"Seleccionar módulo"}

    %% Inventory Management Branch
    H -->|Gestión de Inventario| I{"Operación de Inventario"}

    %% Product Registration Flow
    I -->|Registrar Producto| J["StockCreateView"]
    J --> K["Llenar formulario de producto"]
    K --> L["Generar código automático"]
    L --> M["Validar datos"]
    M --> N{"Datos válidos?"}
    N -->|NO| O["Mostrar errores"]
    N -->|SÍ| P["Guardar en Excel"]
    P --> Q["Enviar StockDataRefreshMessage"]
    Q --> R["Confirmación de registro"]

    %% Inventory Management Flow
    I -->|Consultar/Gestionar| S["StockManageView"]
    S --> T["Cargar inventario completo"]
    T --> U["Mostrar tabla interactiva"]
    U --> V{"Acción en inventario"}

    V -->|Buscar| W["Ingresar criterio búsqueda"]
    W --> X{"Tipo de búsqueda"}
    X -->|Por código| Y["Búsqueda exacta"]
    X -->|Por nombre| Z["Búsqueda parcial"]
    Y --> AA["Filtrar tabla"]
    Z --> AA
    AA --> U

    V -->|Editar| BB["Seleccionar producto"]
    BB --> CC["Enviar StockUpdateMessage"]
    CC --> DD["Navegar a StockCreateView modo edición"]
    DD --> EE["Pre-cargar datos"]
    EE --> FF["Modificar datos"]
    FF --> GG["Actualizar base de datos"]
    GG --> HH["Refrescar vista"]

    V -->|Eliminar| II["Confirmar eliminación"]
    II --> JJ{"Confirmar?"}
    JJ -->|NO| KK["Cancelar"]
    JJ -->|SÍ| LL["delete_stock_product()"]
    LL --> MM["Actualizar Excel"]
    MM --> NN["Refrescar vista"]

    %% Sales Management Branch
    H -->|Gestión de Ventas| OO{"Operación de Ventas"}

    %% Sales Creation Flow
    OO -->|Generar Venta| PP["CreateSellView"]
    PP --> QQ["Inicializar carrito vacío"]
    QQ --> RR["Ingresar código producto"]
    RR --> SS["Buscar producto"]
    SS --> TT{"Producto encontrado?"}
    TT -->|NO| UU["Error: Producto no encontrado"]
    TT -->|SÍ| VV["Verificar stock"]
    VV --> WW{"Stock suficiente?"}
    WW -->|NO| XX["Error: Stock insuficiente"]
    WW -->|SÍ| YY["Validar cantidad"]
    YY --> ZZ{"Cantidad válida?"}
    ZZ -->|NO| AAA["Error: Cantidad inválida"]
    ZZ -->|SÍ| BBB["Agregar al carrito"]
    BBB --> CCC["Calcular total"]
    CCC --> DDD{"Agregar más productos?"}
    DDD -->|SÍ| RR
    DDD -->|NO| EEE{"Carrito vacío?"}
    EEE -->|SÍ| FFF["Error: Carrito vacío"]
    EEE -->|NO| GGG["Confirmar venta"]
    GGG --> HHH{"Usuario confirma?"}
    HHH -->|NO| III["Cancelar venta"]
    HHH -->|SÍ| JJJ["Procesar venta"]
    JJJ --> KKK["Registrar en base de datos"]
    KKK --> LLL["Actualizar inventario"]
    LLL --> MMM["Mostrar confirmación"]
    MMM --> NNN["Limpiar carrito"]

    %% Sales Consultation Flow
    OO -->|Consultar Ventas| OOO["ManageSellView"]
    OOO --> PPP["Cargar datos de ventas"]
    PPP --> QQQ["Aplicar filtro 'hoy'"]
    QQQ --> RRR["Usuario selecciona filtro"]
    RRR --> SSS{"Tipo de filtro"}
    SSS -->|hoy| TTT["Filtrar ventas de hoy"]
    SSS -->|ayer| UUU["Filtrar ventas de ayer"]
    SSS -->|7_dias| VVV["Filtrar últimos 7 días"]
    SSS -->|30_dias| WWW["Filtrar últimos 30 días"]
    TTT --> XXX["Formatear detalles"]
    UUU --> XXX
    VVV --> XXX
    WWW --> XXX
    XXX --> YYY["Parsear productos y cantidades"]
    YYY --> ZZZ["Crear descripción legible"]
    ZZZ --> AAAA["Calcular totales período"]
    AAAA --> BBBB["Mostrar estadísticas"]
    BBBB --> CCCC["Actualizar tabla filtrada"]

    %% Return paths to main menu
    O --> K
    R --> DDDD["Continuar operaciones"]
    KK --> U
    NN --> U
    HH --> U
    UU --> RR
    XX --> RR
    AAA --> RR
    FFF --> RR
    III --> DDD
    NNN --> EEEE["Nueva venta"]
    CCCC --> FFFF["Continuar consultas"]

    DDDD --> I
    U --> I
    EEEE --> OO
    FFFF --> OO
    I --> H
    OO --> H
```
