# Alcance y Versiones del Proyecto

## Estrategia de Desarrollo

Hemos planeado 3 versiones que definen el alcance del proyecto, permitiendo un desarrollo incremental y escalable que se adapte a las necesidades y recursos disponibles.

## Versión 1: MVP - Clase Fundamentos de Programación

**Estado: COMPLETADO**

Esta primera versión se plantea como MVP (Mínimo Producto Viable) y es la versión que se presenta para la clase de fundamentos de programación.

### Características Principales

- **Sin bases de datos relacionales**: Utiliza archivos Excel para máxima compatibilidad
- **Funcionamiento local**: No requiere conexión a internet
- **Sin módulo de usuarios**: Acceso directo sin autenticación
- **Interfaz en terminal**: Usando Textual para una experiencia moderna
- **Ejecutable portable**: Distribución sencilla para Windows

### Módulos Implementados

#### Módulo de Inventario

- Registro de producto con categoría
- Base de datos en Excel para productos
- Consulta y actualización de producto
- Eliminación de productos con confirmación
- Generación automática de códigos únicos
- 7 categorías predefinidas

#### Módulo de Ventas

- Búsqueda y agregado de productos al carrito
- Cálculo automático de totales
- Validación de stock disponible
- Registro de venta en base de datos Excel
- Consulta de ventas por fecha (diaria, semanal, mensual)
- Actualización automática de inventario post-venta

#### Interfaz de Usuario

- Interfaz en Textual (TUI moderna)
- Navegación intuitiva con teclado
- Temas claro y oscuro
- Validación en tiempo real
- Mensajes informativos y confirmaciones

### Logros del Entregable 2

- Implementación de interfaz para registro de productos
- División modular del proyecto (UI + Business)
- Lógica básica CRUD para inventario

### Logros del Entregable 3

- Vista de consulta de inventario con búsqueda
- Sistema completo de ventas con carrito
- Consulta de ventas con filtros temporales
- Validaciones completas de negocio

## Versión 2: Sistema Comercial Mejorado

**Estado: PLANIFICADO**

Esta versión está diseñada para comercializar el producto como una solución profesional para pequeñas tiendas.

### Nuevas Características

#### Gestión de Usuarios

- **Módulo de autenticación**: Login y roles de usuario
- **Perfiles diferenciados**: Administrador, vendedor, consulta
- **Auditoría de acciones**: Log de operaciones por usuario
- **Configuración de permisos**: Control granular de acceso

#### Base de Datos Relacional

- **Migración a PostgreSQL/MySQL**: Mayor robustez y escalabilidad
- **Integridad referencial**: Relaciones consistentes entre tablas
- **Respaldos automáticos**: Protección de datos críticos
- **Optimización de consultas**: Mejor rendimiento con grandes volúmenes

#### Interfaz Web

- **Frontend en React**: Interfaz moderna y responsiva
- **API REST**: Backend desacoplado para flexibilidad
- **Funcionalidad en la nube**: Acceso desde cualquier dispositivo
- **Sincronización offline**: Trabajo sin conexión con sync posterior

#### Funcionalidades Avanzadas

- **Generación de facturas PDF**: Documentos profesionales
- **Reportes avanzados**: Análisis de ventas, inventario y rentabilidad
- **Gestión de proveedores**: Control de compras y costos
- **Alertas de stock**: Notificaciones automáticas de stock bajo

### Arquitectura Planificada

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (PostgreSQL)  │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Versión 3: Aplicaciones Nativas

**Estado: FUTURO**

Expansión a plataformas móviles y de escritorio para máxima accesibilidad.

### Plataformas Objetivo

#### Aplicación de Escritorio

- **Electron para Windows/Mac/Linux**: Experiencia nativa multiplataforma
- **Sincronización con versión web**: Datos unificados
- **Funcionalidad offline completa**: Operación sin internet
- **Integración con hardware**: Lectores de código de barras, impresoras

#### Aplicaciones Móviles

- **Android nativo**: Kotlin/Java para máximo rendimiento
- **iOS nativo**: Swift para integración completa
- **Funcionalidades móviles**: Cámara para códigos de barras, GPS para entregas
- **Notificaciones push**: Alertas en tiempo real

### Funcionalidades Móviles Específicas

#### Para Vendedores

- **Ventas móviles**: Procesamiento desde tablet/smartphone
- **Consulta rápida de inventario**: Verificación instant
- **Modo offline**: Ventas sin conexión con sincronización posterior

#### Para Administradores

- **Dashboard en tiempo real**: KPIs y métricas importantes
- **Gestión remota**: Control del negocio desde cualquier lugar
- **Alertas inteligentes**: Notificaciones basadas en reglas de negocio
