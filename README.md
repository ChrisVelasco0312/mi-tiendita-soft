# MI TIENDITA SOFT

Software de inventario y caja para tiendas de barrio con interfaz en terminal.

## 🚀 Inicio Rápido

### Prerrequisitos
- Python 3.11 o superior
- Poetry (recomendado) o pip

### Instalación y Ejecución

#### Opción 1: Con Poetry (Recomendado)
```bash
# Instalar dependencias
poetry install --no-root

# Ejecutar aplicación
poetry run python main.py
```

#### Opción 2: Con Nix (Para usuarios NixOS)
```bash
# Activar entorno de desarrollo
nix develop

# Ejecutar aplicación
python main.py
```

#### Opción 3: Con pip
```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install textual pandas openpyxl xlsxwriter

# Ejecutar aplicación
python main.py
```

### Scripts de Automatización (Makefile)

```bash
make pinstall    # Instalar dependencias con Poetry
make run         # Ejecutar con Poetry
make start       # Ejecutar con Nix
make dev         # Modo desarrollo Textual
make serve       # Modo web Textual
```

## 📖 Documentación

### Documentación Principal
- **[Introducción y Objetivos](docs/introduccion-y-objetivos.md)** - Problemática, objetivos y beneficios del proyecto
- **[Alcance y Versiones](docs/alcance-y-versiones.md)** - Roadmap de desarrollo y características por versión
- **[Arquitectura del Sistema](docs/arquitectura.md)** - Estructura técnica y componentes principales
- **[Flujos de Trabajo](docs/flujos-de-trabajo.md)** - Procesos detallados de inventario y ventas

### Documentación Técnica
- **[Historias de Usuario](docs/historias-usuario.md)** - Requisitos funcionales desde perspectiva del usuario
- **[Convenciones de Categorías](docs/convencion_categoria.md)** - Estándares para categorías de productos
- **[Convenciones de Items](docs/convencion_item.md)** - Reglas para códigos de productos

## 🎯 Funcionalidades Principales

### ✅ Módulo de Inventario
- Registro de productos con categorías predefinidas
- Generación automática de códigos únicos
- Consulta y edición de inventario
- Eliminación de productos con confirmación

### ✅ Módulo de Ventas
- Carrito de compras interactivo
- Validación de stock en tiempo real
- Cálculo automático de totales
- Historial de ventas con filtros temporales

### ✅ Interfaz de Usuario
- Terminal UI moderna con Textual
- Navegación intuitiva con teclado
- Temas claro y oscuro
- Validaciones en tiempo real

## 🏪 Uso del Sistema

### Navegación Principal
Al ejecutar la aplicación, encontrarás dos secciones principales:

**Inventario:**
- **Registro de Inventario**: Agregar nuevos productos
- **Consulta de Inventario**: Buscar y gestionar productos existentes

**Ventas:**
- **Generar Venta**: Crear nuevas transacciones de venta
- **Consultar Venta**: Revisar historial de ventas con filtros

### Atajos de Teclado
- `d`: Alternar entre tema claro y oscuro
- `Tab`: Navegar entre elementos
- `Enter`: Confirmar selección
- `Escape`: Regresar/cancelar
- `ctrl + q`: Cerrar la aplicación

## 🛠️ Tecnologías Utilizadas

- **Python 3.11+**: Lenguaje principal
- **Textual**: Framework para interfaz de terminal moderna
- **Pandas**: Manipulación de datos y operaciones Excel
- **Poetry**: Gestión de dependencias
- **Nix**: Entorno reproducible de desarrollo (opcional)

## 📊 Estado del Proyecto

**Versión Actual: 1.0 (MVP Completado)**

- ✅ Sistema completo de inventario
- ✅ Proceso de ventas funcional
- ✅ Persistencia en archivos Excel
- ✅ Interfaz intuitiva en terminal
- ✅ Validaciones de negocio implementadas

## 📄 Licencia

Proyecto académico desarrollado para IU Digital. 