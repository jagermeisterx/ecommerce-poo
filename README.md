# 🛒 Ecommerce CLI – Módulo 4 (POO y roles)

Aplicación de consola en **Python 3** que simula una tienda online, ahora
reestructurada con **Programación Orientada a Objetos**, **roles** (ADMIN y
CLIENTE), **herencia**, **composición**, **manejo de excepciones** y
**persistencia en archivos de texto**.

Evolución del proyecto del **Módulo 3** (Bootcamp AD Academy – Sustantiva).

---

## 👥 Roles

### ADMIN — gestiona el catálogo
1. Listar productos
2. Crear producto (id, nombre, categoría, precio)
3. Actualizar producto
4. Eliminar producto
5. Guardar catálogo en archivo

### CLIENTE — compra
1. Ver catálogo
2. Buscar por nombre o categoría
3. Agregar al carrito (con cantidad)
4. Ver carrito y total
5. Confirmar compra (queda registrada en `data/ordenes.txt`)

Al iniciar, el programa pregunta si ingresas como **ADMIN** o **CLIENTE** y
muestra el menú correspondiente.

---

## 🚀 Cómo ejecutarlo

Requiere **Python 3** (sin librerías externas).

```bash
cd ecommerce
python main.py
```
> En algunos sistemas usa `python3` en lugar de `python`.

---

## 🗂 Estructura del proyecto

```
ecommerce/
├── main.py          # Punto de entrada
├── config.py        # Rutas de los archivos de datos
├── excepciones.py   # Excepciones personalizadas
├── producto.py      # Clase Producto
├── catalogo.py      # Clase Catalogo (composición + persistencia)
├── carrito.py       # Clases ItemCarrito y Carrito (composición)
├── usuarios.py      # Usuario (base) → Admin / Cliente (herencia)
├── tienda.py        # Clase Tienda (coordina la ejecución y los menús)
├── utils.py         # Utilidades de consola
├── PRD.md           # Documento de requisitos / plan
├── README.md        # Este archivo
└── data/
    ├── catalogo.csv # Catálogo persistente (se carga al iniciar)
    └── ordenes.txt  # Se genera al confirmar compras
```

---

## 🧱 Conceptos aplicados

- **Clases y composición:** `Catalogo` contiene `Producto`; `Carrito` contiene
  `ItemCarrito`; `Cliente` tiene un `Carrito`.
- **Herencia:** `Admin` y `Cliente` extienden `Usuario` con menús y
  comportamientos distintos (polimorfismo en `mostrar_menu` / `procesar_opcion`).
- **Excepciones personalizadas:** `ProductoNoEncontradoError`,
  `CantidadInvalidaError`, `CarritoVacioError`, `IdDuplicadoError`, usadas con
  bloques `try/except/finally`.
- **Archivos de texto:** lectura/escritura del catálogo y registro obligatorio
  de las compras con fecha/hora, productos y total.

---

## 🛍 Catálogo inicial

10 productos en tres categorías: **tecnología**, **hogar** y **ropa**. Si el
archivo `data/catalogo.csv` no existe, el programa lo crea a partir del catálogo
definido en el código.
