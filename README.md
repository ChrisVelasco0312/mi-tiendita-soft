# MI TIENDITA SOFT

Software de inventario y caja para tiendas de barrio.

# Introducción y objetivos

Se presenta la necesidad de un sistema sencillo para tiendas de barrio que
permita la gestión de inventario y ventas.

Las tiendas de barrio son negocios pequeños que muchas veces no cuentan con una
organización adecuada de los procesos básicos de venta y registro de
inventario, algunas veces los procesos de caja, venta e inventario se organizan
de forma manual en papel.

La implementación de este software tiene como objetivo mejorar los procesos de
gestón de inventario y venta para tiendas pequeñas de barrio, permitiendo al
usuario registrar productos en una base de datos local en formato excel de forma
automática a través de un formulario sencillo, además de habilitar la consulta
de los productos registrados de inventario junto con la cantidad en existencia.

Adicional a ello permitir al usuario generar ventas y facturas, agregando
productos existentes a la venta, calculando precio total y registrar la venta en
una base de datos excel para la consulta de ventas por fecha (mensual, semanal
y díaria)

# Alcance

Hemos planeado 2 versiones que definen el alcance del proyecto, la primera
versión se plantea cómo MVP (Mínimo Producto Viable) y es la versión que se
presentará para la clase de fundamentos de programación. La primera versión
no usa bases de datos relacionales y debe funcionar en local al almacenar los
datos en archivos de excel. Tampoco incluye un módulo de autorización de
usuarios, pero si contiene un ejecutable portable para windows.

## Version 1 MVP Clase Fundamentos de Programación

- Módulo de registro de inventario.
  - Registro de producto con categoría.
  - Base de datos en excel para productos.
  - Consulta y actualización de producto.
- Módulo de ventas
  - Buscar y agregar productos
  - Calcular total
  - Generar factura pdf
  - Registrar venta en base de datos excel
  - Consultar venta por fecha díaria
- Interfaz de usuario en Textual, es una interfaz de usuario
  sensilla que se ejecuta fácilmente en una terminal, los requisitos
  son mínimos ya que ni siquiera requiere de un navegador ya que se puede
  considerar como una app de escritorio.
- Se entrega un ejecutable demo para windows.

## Versión 2 Sistema mejorado para comercializarlo

- Módulo de administración de usuarios
- Uso de bases de datos relacionales.
- Implementación de aplicación web que funcione en la nube.
- Interfaz web con react.

## Versión 3

- Versión de escritorio con Electron para Windows.
- Versión móvil android y ios.

# Avances del código

- Se implementa la interfaz para el registro de producto.
- Se divide el proyecto de forma módular de la siguiente forma.
  - `ui` es la carpeta que contiene todas las pantallas y componentes de
    interfaz (front-end con `Textual`)
  - `business` es la carpeta que contiene la lógica de negocio, todas las
    operaciones CRUD con el excel de Inventario y las funciones controlador que se
    exponen a la interfaz. (backend)
- Se implementa la lógica básica CRUD para el registro de productos en el
  inventario.

# Próximos pasos:

- [ ] Interfaz de consulta de inventario y actualización de producto.
- [ ] Interfaz de generación de venta.
- [ ] Lógica de generación de venta, registro en nueva base de datos de ventas.
- [ ] Interfaz de consulta de ventas por fecha diaria.
- [ ] Generación de factura en pdf

# Detalles del proyecto e instrucciones de ejecución

## Estructura de Carpetas

```
.
├── main.py
├── src
│   ├── ui
│   └── business
├── Makefile
├── pyproject.toml
├── poetry.lock
├── .git
├── flake.nix
├── flake.lock
├── example_code.py
├── docs
├── .gitignore
└── README.md
```

## Configuración para NixOS

Para configurar el entorno de desarrollo en NixOS, se utiliza el archivo
`flake.nix`. Este archivo define un entorno de desarrollo que incluye Python y
Poetry. Para activar este entorno, se puede usar el comando:

```bash
nix develop
```

## Uso de Poetry

Poetry se utiliza para gestionar las dependencias del proyecto. Para instalar
las dependencias, se puede ejecutar:

```bash
poetry install --no-root
```

Para ejecutar el proyecto, se utiliza el siguiente comando:

```bash
poetry run python main.py
```

## Scripts del Makefile

El `Makefile` contiene los siguientes scripts:

- `ed`: Activa automaticamente el entorno nix y abre neovim.
- `dev`: Ejecuta modo dev de textual
- `serve`: Ejecuta el modo web de textual
- `pinstall`: Instala las dependencias del proyecto usando Poetry.
- `start`: Ejecuta el programa automáticamente con el entorno nix
- `run`: Ejecuta el proyecto usando Poetry.

## Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal del proyecto.
- **Textual**: Biblioteca utilizada para la interfaz del proyecto.
- **Pandas**: Biblioteca utilizada para hacer operaciones sobre excel.
- **Poetry**: Herramienta para la gestión de dependencias y empaquetado de Python.
- **Nix**: Sistema de gestión de paquetes utilizado para configurar el entorno
  de desarrollo, solo relevante para usuarios de Nix o NixOS
