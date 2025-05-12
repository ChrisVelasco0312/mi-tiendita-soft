## Historias de Usuario para "Mi Tiendita Soft"

### Épica: Navegación Principal

1.  **HU001: Acceso a Módulo de Inventario**

    - **Como** usuario administrador,
    - **Quiero** poder hacer clic en un botón "Inventario" en la pantalla principal,
    - **Para** acceder a las funcionalidades de gestión de inventario.

2.  **HU002: Acceso a Módulo de Ventas**
    - **Como** usuario cajero/administrador,
    - **Quiero** poder hacer clic en un botón "Venta" en la pantalla principal,
    - **Para** acceder a las funcionalidades de gestión de ventas.

### Épica: Gestión de Inventario

3.  **HU101: Acceso a Registro de Producto**

    - **Como** usuario administrador,
    - **Quiero** poder seleccionar la opción "Registrar producto" dentro del módulo de Inventario,
    - **Para** poder añadir nuevos artículos al sistema.

4.  **HU102: Acceso a Consulta de Inventario**

    - **Como** usuario administrador,
    - **Quiero** poder seleccionar la opción "Consultar inventario" dentro del módulo de Inventario,
    - **Para** poder ver los productos existentes y sus detalles.
    - _(Nota: La interfaz de consulta no está detallada, pero la opción existe)._

5.  **HU103: Visualización de Categorías de Producto**

    - **Como** usuario administrador,
    - **Al** acceder a "Registrar producto", **quiero** ver una lista de categorías de producto existentes (ej: "001 <Nombre de categoría>", "002 Alimentos y bebidas", etc.),
    - **Para** poder clasificar el nuevo producto.

6.  **HU104: Creación de Nueva Categoría de Producto**

    - **Como** usuario administrador,
    - **Al** registrar un producto, **quiero** tener una opción "Crear nueva categoría",
    - **Para** poder añadir una nueva clasificación si no existe una adecuada.

7.  **HU105: Edición en Línea de Nueva Categoría**

    - **Como** usuario administrador,
    - **Al** hacer clic en "Crear nueva categoría", **quiero** que aparezca un campo de texto editable,
    - **Para** ingresar el nombre de la nueva categoría y confirmarla (ej: presionando Enter).

8.  **HU106: Actualización de Lista de Categorías**

    - **Como** usuario administrador,
    - **Después** de crear una nueva categoría, **quiero** que esta aparezca inmediatamente en la lista de categorías disponibles para seleccionar,
    - **Para** poder usarla en el registro del producto actual.

9.  **HU107: Selección de Categoría para Registro de Producto**

    - **Como** usuario administrador,
    - **Quiero** poder seleccionar una categoría de la lista (existente o recién creada),
    - **Para** que se despliegue el formulario de detalles del producto asociado a esa categoría.

10. **HU108: Visualización de Formulario de Registro de Producto**

    - **Como** usuario administrador,
    - **Después** de seleccionar una categoría, **quiero** ver un formulario con los campos: Código de ítem, Nombre del producto, Precio compra, Precio venta, Cantidad, Descripción y Proveedor,
    - **Para** ingresar la información del nuevo producto.

11. **HU109: Definición de Tipos de Dato y Obligatoriedad en Formulario**

    - **Como** usuario administrador,
    - **Quiero** que los campos del formulario de registro de producto tengan tipos de dato específicos (número, texto) y que los campos "Código de ítem", "Nombre del producto", "Precio compra", "Precio venta" y "Cantidad" sean requeridos,
    - **Para** asegurar la integridad de los datos del producto.

12. **HU110: Finalización de Registro de Producto (Botón)**

    - **Como** usuario administrador,
    - **Después** de llenar el formulario de registro de producto, **quiero** poder hacer clic en un botón "Terminar registro",
    - **Para** iniciar el proceso de guardado del producto.

13. **HU111: Confirmación de Registro de Producto**

    - **Como** usuario administrador,
    - **Al** hacer clic en "Terminar registro", **quiero** ver un mensaje de confirmación (ej: "¿Está seguro de que desea terminar el registro?") con opciones "SI" y "NO",
    - **Para** evitar registros accidentales y poder revisar la información.

14. **HU112: Acción de Confirmación "SI" para Registro**

    - **Como** usuario administrador,
    - **En** el diálogo de confirmación, **quiero** poder hacer clic en "SI",
    - **Para** guardar el producto en el sistema.
    - _(Nota: Se asumiría una redirección o mensaje de éxito posterior)._

15. **HU113: Acción de Cancelación "NO" para Registro**
    - **Como** usuario administrador,
    - **En** el diálogo de confirmación, **quiero** poder hacer clic en "NO",
    - **Para** volver al formulario de registro y poder corregir o cancelar la operación.

### Épica: Gestión de Ventas

16. **HU201: Acceso a Generación de Venta**

    - **Como** usuario cajero/administrador,
    - **Quiero** poder seleccionar la opción "Generar venta" dentro del módulo de Ventas,
    - **Para** poder registrar una nueva transacción comercial.
    - _(Nota: La interfaz de generación de venta no está detallada, pero la opción existe)._

17. **HU202: Acceso a Consulta de Ventas**
    - **Como** usuario cajero/administrador,
    - **Quiero** poder seleccionar la opción "Consultar ventas" dentro del módulo de Ventas,
    - **Para** poder ver el historial de ventas realizadas.
    - _(Nota: La interfaz de consulta de ventas no está detallada, pero la opción existe)._
