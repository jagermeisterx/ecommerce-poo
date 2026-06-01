import os

from config import RUTA_CATALOGO, DATA_DIR
from producto import Producto
from excepciones import ProductoNoEncontradoError, IdDuplicadoError


#  Se usa como semilla si no existe el archivo catalogo.csv todavía.
CATALOGO_INICIAL = [
    (1, "Ampolleta LED", "hogar", 2500),
    (2, 'Smart TV 55"', "tecnologia", 259990),
    (3, "Polera básica", "ropa", 9990),
    (4, "Jeans slim fit", "ropa", 24990),
    (5, "Audífonos bluetooth", "tecnologia", 49990),
    (6, "Teclado mecánico", "tecnologia", 39990),
    (7, "Lámpara de escritorio", "hogar", 14990),
    (8, "Cojín decorativo", "hogar", 7990),
    (9, "Zapatillas running", "ropa", 34990),
    (10, "Mouse inalámbrico", "tecnologia", 19990),
]


class Catalogo:
    """Contiene muchos Producto y gestiona su ciclo de vida y persistencia."""

    def __init__(self, ruta=RUTA_CATALOGO):
        self.ruta = ruta
        self.productos = []  # composición: lista de objetos Producto

    def __len__(self):
        return len(self.productos)

    def listar(self):       #Devuelve la lista de productos (sin imprimir).
        return self.productos

        def buscar_por_id(self, id_producto):   #Devuelve el Producto con ese id o lanza ProductoNoEncontradoError.
        for producto in self.productos:
            if producto.id == id_producto:
                return producto
        raise ProductoNoEncontradoError(
            f"No existe ningún producto con ID {id_producto}.")

    def buscar(self, termino):      # Devuelve los productos cuyo nombre o categoría contienen el término.
        termino = termino.strip().lower()
        resultados = []
        for producto in self.productos:
            if (termino in producto.nombre.lower()
                    or termino in producto.categoria.lower()):
                resultados.append(producto)
        return resultados

    def _existe_id(self, id_producto):
        return any(p.id == id_producto for p in self.productos)

    def siguiente_id(self):     # Sugiere el próximo id disponible (máximo actual + 1).
        if not self.productos:
            return 1
        return max(p.id for p in self.productos) + 1

    def agregar_producto(self, producto):   # Agrega un producto nuevo. Lanza IdDuplicadoError si el id ya existe.
        if self._existe_id(producto.id):
            raise IdDuplicadoError(
                f"Ya existe un producto con ID {producto.id}.")
        self.productos.append(producto)

    def actualizar_producto(self, id_producto, nombre=None, categoria=None, precio=None):   # Actualiza los campos indicados de un producto existente.
        producto = self.buscar_por_id(id_producto)  # puede lanzar excepción
        if nombre is not None:
            producto.nombre = nombre
        if categoria is not None:
            producto.categoria = categoria
        if precio is not None:
            producto.precio = precio
        return producto

    def eliminar_producto(self, id_producto):   # Elimina un producto por id. Lanza ProductoNoEncontradoError si no está.
        producto = self.buscar_por_id(id_producto)  # puede lanzar excepción
        self.productos.remove(producto)
        return producto

    # --- persistencia en archivo ---

    def cargar_desde_archivo(self):
        """Carga el catálogo desde el archivo de texto.
        Si el archivo no existe, usa el catálogo inicial del código y lo guarda.
        """
        try:
            with open(self.ruta, "r", encoding="utf-8") as f:
                self.productos = []
                for linea in f:
                    if linea.strip():  # ignora líneas vacías
                        self.productos.append(Producto.from_csv(linea))
            print(f"Catálogo cargado desde '{self.ruta}' "
                  f"({len(self.productos)} productos).")
        except FileNotFoundError:
            print("No se encontró catálogo previo. Se carga el catálogo inicial.")
            self.cargar_inicial()
            self.guardar_en_archivo()
        except (ValueError, OSError) as error:      # Archivo corrupto o ilegible: avisamos y seguimos con el inicial
            print(f"No se pudo leer el catálogo ({error}). Se usa el inicial.")
            self.cargar_inicial()

    def cargar_inicial(self):     # Carga en memoria el catálogo de ejemplo definido en el código.
        self.productos = [
            Producto(id_, nombre, categoria, precio)
            for (id_, nombre, categoria, precio) in CATALOGO_INICIAL
        ]

    def guardar_en_archivo(self):       # Guarda el catálogo completo en el archivo de texto.
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(self.ruta, "w", encoding="utf-8") as f:
                for producto in self.productos:
                    f.write(producto.to_csv() + "\n")
            print(f"Catálogo guardado en '{self.ruta}'.")
        except OSError as error:
            print(f"Error al guardar el catálogo: {error}")
