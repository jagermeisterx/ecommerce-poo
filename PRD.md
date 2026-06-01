# PRD – Ecommerce CLI con POO y roles (Módulo 4)

## 1. Propósito
Reestructurar el ecommerce de consola del **Módulo 3** (actualmente procedural) hacia
**Programación Orientada a Objetos** en Python, agregando **roles** (ADMIN y CLIENTE),
**herencia**, **composición**, **manejo de excepciones** y **persistencia en archivos de texto**.

El comportamiento de cara al usuario se mantiene (catálogo, búsqueda, carrito, total),
pero ahora se organiza en clases con responsabilidades claras y se incorporan las funciones
de administración y de confirmación de compra que el módulo exige.

---

## 2. Estado actual (Módulo 3) vs. Estado objetivo (Módulo 4)

| Aspecto | Módulo 3 (actual) | Módulo 4 (objetivo) |
|---|---|---|
| Paradigma | Procedural (funciones + variables globales) | POO (clases con responsabilidades) |
| Datos | `dict` sueltos en listas globales | Objetos `Producto`, `Catalogo`, `Carrito` |
| Roles | No existen | `Usuario` → `Admin` / `Cliente` (herencia) |
| Administración | No existe | Crear / actualizar / eliminar productos |
| Compra | No existe (solo ver total) | Confirmar compra + registro en archivo |
| Excepciones | Solo `ValueError` puntual | `try/except/finally` + excepciones propias |
| Archivos | No usa | Lee/escribe `catalogo.csv` y `ordenes.txt` |
| Organización | Un solo `.py` | Módulos separados por responsabilidad |

---

## 3. Arquitectura objetivo

### 3.1. Clases del dominio (datos y lógica)
- **`Producto`** — unidad básica: `id`, `nombre`, `categoria`, `precio`. Sabe serializarse a/desde CSV.
- **`Catalogo`** — *composición*: contiene muchos `Producto`. Agrega, actualiza, elimina, busca, y persiste en archivo.
- **`ItemCarrito`** — *composición*: une un `Producto` con una `cantidad` y calcula su subtotal.
- **`Carrito`** — *composición*: contiene muchos `ItemCarrito`. Agrega ítems, calcula total, se vacía.

### 3.2. Clases de roles (herencia)
- **`Usuario`** — clase base: nombre y contrato común (`mostrar_menu`, `procesar_opcion`).
- **`Admin(Usuario)`** — gestiona el catálogo.
- **`Cliente(Usuario)`** — navega, usa su propio `Carrito` (*composición*) y confirma compras.

### 3.3. Coordinación
- **`Tienda`** — orquesta la app: carga el catálogo, pide el rol al inicio y ejecuta el menú correspondiente de forma polimórfica.

### 3.4. Excepciones personalizadas
- `EcommerceError` (base)
- `ProductoNoEncontradoError`
- `CantidadInvalidaError`
- `CarritoVacioError`
- `IdDuplicadoError`

### 3.5. Archivos de texto
- **`data/catalogo.csv`** — catálogo persistente (se lee al iniciar, se guarda desde el menú ADMIN).
- **`data/ordenes.txt`** — registro **obligatorio** de cada compra confirmada (fecha/hora, productos, total).

---

## 4. Estructura de archivos del proyecto
```
ecommerce/
├── main.py            # Punto de entrada
├── config.py          # Rutas de los archivos de datos
├── excepciones.py     # Excepciones personalizadas
├── producto.py        # Clase Producto
├── catalogo.py        # Clase Catalogo (+ carga/seed inicial)
├── carrito.py         # Clases ItemCarrito y Carrito
├── usuarios.py        # Usuario, Admin, Cliente
├── tienda.py          # Clase Tienda (coordinación y menús)
├── README.md
├── PRD.md
└── data/
    ├── catalogo.csv   # Catálogo inicial (10 productos del M3)
    └── ordenes.txt    # Se genera al confirmar compras
```

---

## 5. Requisitos funcionales

### ADMIN
1. Listar productos del catálogo.
2. Crear producto (id, nombre, categoría, precio) — validando ID único y precio > 0.
3. Actualizar producto (nombre, precio o categoría).
4. Eliminar producto.
5. Guardar catálogo en archivo (`catalogo.csv`).

### CLIENTE
1. Ver catálogo.
2. Buscar por nombre o categoría.
3. Agregar al carrito (id + cantidad entera > 0).
4. Ver carrito y total (nombre, cantidad, precio unitario, subtotal y total).
5. Confirmar compra: bloquear si está vacío, registrar en `ordenes.txt` y vaciar el carrito.

### Manejo de errores
- ID inexistente → `ProductoNoEncontradoError`.
- Cantidad ≤ 0 o no entera → `CantidadInvalidaError`.
- Carrito vacío al comprar → `CarritoVacioError`.
- ID duplicado al crear → `IdDuplicadoError`.
- Errores de archivo → captura de `OSError` con `try/except/finally`.

---

## 6. Checklist de tareas (mapeado a la rúbrica)

- [ ] **Diseño OO**: `Producto`, `Catalogo`, `ItemCarrito`, `Carrito`, `Usuario`, `Admin`, `Cliente`, `Tienda`.
- [ ] **Herencia**: `Admin` y `Cliente` extienden `Usuario` con menús/comportamientos distintos.
- [ ] **Composición**: `Catalogo` contiene `Producto`; `Carrito` contiene `ItemCarrito`; `Cliente` tiene un `Carrito`.
- [ ] **Roles**: selección ADMIN/CLIENTE al inicio + menús claros.
- [ ] **Funcionalidades ADMIN**: listar, crear, actualizar, eliminar, guardar.
- [ ] **Funcionalidades CLIENTE**: ver, buscar, carrito, total, confirmar compra.
- [ ] **Excepciones**: `try/except/finally` + al menos una excepción personalizada.
- [ ] **Archivos**: lectura/escritura de `catalogo.csv` y registro en `ordenes.txt`.
- [ ] **Legibilidad**: `snake_case`, indentación, comentarios breves, módulos separados.
- [ ] **Restricciones**: sin BD, sin librerías externas, sin frameworks web.
