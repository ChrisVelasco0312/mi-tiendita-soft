# MI TIENDITA SOFT

Software de inventario y caja para tiendas de barrio.

- Python.
- Interfaz en Textual.

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

Para configurar el entorno de desarrollo en NixOS, se utiliza el archivo `flake.nix`. Este archivo define un entorno de desarrollo que incluye Python y Poetry. Para activar este entorno, se puede usar el comando:

```bash
nix develop
```

## Uso de Poetry

Poetry se utiliza para gestionar las dependencias del proyecto. Para instalar las dependencias, se puede ejecutar:

```bash
poetry install --no-root
```

Para ejecutar el proyecto, se utiliza el siguiente comando:

```bash
poetry run python main.py
```

## Scripts del Makefile

El `Makefile` contiene los siguientes scripts:

- `dev`: Activa el entorno de desarrollo de Nix.
- `install`: Instala las dependencias del proyecto usando Poetry.
- `run`: Ejecuta el proyecto usando Poetry.

## Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal del proyecto.
- **Textual**: Biblioteca utilizada para la interfaz del proyecto.
- **Poetry**: Herramienta para la gestión de dependencias y empaquetado de Python.
- **Nix**: Sistema de gestión de paquetes utilizado para configurar el entorno de desarrollo. 
