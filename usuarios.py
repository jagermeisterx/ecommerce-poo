"""Roles de la tienda: Usuario (base), Admin y Cliente (herencia)."""

from datetime import datetime

from carrito import Carrito
from config import RUTA_ORDENES, DATA_DIR
from excepciones import (
    EcommerceError,
    ProductoNoEncontradoError,
    CantidadInvalidaError,
    CarritoVacioError,
    IdDuplicadoError,
)
from producto import Producto
from utils import separador, leer_texto, leer_entero

import os


class Usuario:
    """Clase base de los roles. Define el contrato común de los menús."""

    def __init__(self, nombre, catalogo):
        self.nombre = nombre
        self.catalogo = catalogo  # el catálogo es compartido por la tienda

    @property
    def rol(self):
        return self.__class__.__name__.upper()

    def mostrar_menu(self):
        """Cada rol define su propio menú (se sobreescribe)."""
        raise NotImplementedError

    def procesar_opcion(self, opcion):
        """Procesa la opción elegida. Devuelve True para seguir, False para salir."""
        raise NotImplementedError


class Admin(Usuario):
    """Administrador: gestiona el catálogo de productos."""

    def mostrar_menu(self):
        separador(40)
        print(f"*  MENÚ ADMIN ({self.nombre})")
        separador(40)
        print("* (1) Listar productos")
        print("* (2) Crear producto")
        print("* (3) Actualizar producto")
        print("* (4) Eliminar producto")
        print("* (5) Guardar catálogo en archivo")
        print("* (0) Salir")
        separador(40)

    def procesar_opcion(self, opcion):
        if opcion == 1:
            self.listar_productos()
        elif opcion == 2:
            self.crear_producto()
        elif opcion == 3:
            self.actualizar_producto()
        elif opcion == 4:
            self.eliminar_producto()
        elif opcion == 5:
            self.catalogo.guardar_en_archivo()
        elif opcion == 0:
            print("Cerrando sesión de ADMIN...")
            return False
        else:
            print("Opción no válida...")
        return True

    # --- acciones del admin ---

    def listar_productos(self):
        separador()
        if len(self.catalogo) == 0:
            print("El catálogo está vacío.")
            separador()
            return
        for producto in self.catalogo.listar():
            print(f"  {producto}")
        separador()

    def crear_producto(self):
        separador()
        print("Crear nuevo producto")
        sugerido = self.catalogo.siguiente_id()
        id_producto = leer_entero(f"ID del producto (sugerido {sugerido}): ",
                                   minimo=1)
        if id_producto is None:
            return

        nombre = leer_texto("Nombre: ")
        categoria = leer_texto("Categoría: ")
        precio = leer_entero("Precio: ", minimo=1)
        if precio is None:
            return

        try:
            nuevo = Producto(id_producto, nombre, categoria, precio)
            self.catalogo.agregar_producto(nuevo)
            print(f"Producto creado: {nuevo}")
        except IdDuplicadoError as error:
            print(f"Error: {error}")

    def actualizar_producto(self):
        separador()
        id_producto = leer_entero("ID del producto a actualizar: ", minimo=1)
        if id_producto is None:
            return

        try:
            producto = self.catalogo.buscar_por_id(id_producto)
        except ProductoNoEncontradoError as error:
            print(f"Error: {error}")
            return

        print(f"Editando: {producto}")
        print("(Deje en blanco para mantener el valor actual)")

        nuevo_nombre = leer_texto("Nuevo nombre: ", permitir_vacio=True)
        nueva_categoria = leer_texto("Nueva categoría: ", permitir_vacio=True)
        nuevo_precio_txt = leer_texto("Nuevo precio: ", permitir_vacio=True)

        nuevo_precio = None
        if nuevo_precio_txt:
            try:
                nuevo_precio = int(nuevo_precio_txt)
                if nuevo_precio <= 0:
                    print("Precio inválido. No se cambia el precio.")
                    nuevo_precio = None
            except ValueError:
                print("Precio no numérico. No se cambia el precio.")

        self.catalogo.actualizar_producto(
            id_producto,
            nombre=nuevo_nombre or None,
            categoria=nueva_categoria or None,
            precio=nuevo_precio,
        )
        print(f"Producto actualizado: {self.catalogo.buscar_por_id(id_producto)}")

    def eliminar_producto(self):
        separador()
        id_producto = leer_entero("ID del producto a eliminar: ", minimo=1)
        if id_producto is None:
            return
        try:
            eliminado = self.catalogo.eliminar_producto(id_producto)
            print(f"Producto eliminado: {eliminado}")
        except ProductoNoEncontradoError as error:
            print(f"Error: {error}")


class Cliente(Usuario):
    """Cliente: navega el catálogo, usa un carrito y confirma compras."""

    def __init__(self, nombre, catalogo):
        super().__init__(nombre, catalogo)
        self.carrito = Carrito()  # composición: el cliente tiene un carrito

    def mostrar_menu(self):
        separador(40)
        print(f"*  MENÚ CLIENTE ({self.nombre})")
        separador(40)
        print("* (1) Ver catálogo")
        print("* (2) Buscar producto")
        print("* (3) Agregar producto al carrito")
        print("* (4) Ver carrito y total")
        print("* (5) Confirmar compra")
        print("* (0) Salir")
        separador(40)

    def procesar_opcion(self, opcion):
        if opcion == 1:
            self.ver_catalogo()
        elif opcion == 2:
            self.buscar_producto()
        elif opcion == 3:
            self.agregar_al_carrito()
        elif opcion == 4:
            self.ver_carrito_y_total()
        elif opcion == 5:
            self.confirmar_compra()
        elif opcion == 0:
            print("¡Vuelva pronto!")
            return False
        else:
            print("Opción no válida...")
        return True

    # --- acciones del cliente ---

    def ver_catalogo(self):
        separador()
        if len(self.catalogo) == 0:
            print("El catálogo está vacío.")
            separador()
            return
        for producto in self.catalogo.listar():
            print(f"  {producto}")
        separador()

    def buscar_producto(self):
        termino = leer_texto("Buscar por nombre o categoría: ")
        resultados = self.catalogo.buscar(termino)
        separador()
        if not resultados:
            print("Producto no encontrado...")
        else:
            print(f"Se encontraron {len(resultados)} resultado(s):")
            for producto in resultados:
                print(f"  {producto}")
        separador()

    def agregar_al_carrito(self):
        separador()
        id_producto = leer_entero("ID del producto: ", minimo=1)
        if id_producto is None:
            return

        try:
            producto = self.catalogo.buscar_por_id(id_producto)
            cantidad = leer_entero(
                f"¿Cuántas unidades de '{producto.nombre}'? ")
            if cantidad is None:
                return
            item = self.carrito.agregar(producto, cantidad)
            print(f"'{producto.nombre}' en el carrito "
                  f"(cantidad total: {item.cantidad}).")
        except ProductoNoEncontradoError as error:
            print(f"Error: {error}")
        except CantidadInvalidaError as error:
            print(f"Error: {error}")

    def ver_carrito_y_total(self):
        separador()
        if self.carrito.esta_vacio():
            print("El carrito está vacío.")
            separador()
            return

        print(f"{'ID':<5}{'Nombre':<24}{'Cant.':>6}{'P.Unit':>12}{'Subtotal':>14}")
        separador()
        for item in self.carrito.items:
            p = item.producto
            print(f"{p.id:<5}{p.nombre:<24}{item.cantidad:>6}"
                  f"{('$' + format(p.precio, ',.0f')):>12}"
                  f"{('$' + format(item.subtotal(), ',.0f')):>14}")
        separador()
        total = self.carrito.calcular_total()
        print(f"TOTAL A PAGAR: ${total:,.0f}")
        separador()

    def confirmar_compra(self):
        separador()
        try:
            if self.carrito.esta_vacio():
                raise CarritoVacioError(
                    "El carrito está vacío, no se puede confirmar la compra.")
            self._registrar_orden()
            print("¡Compra confirmada! La orden quedó registrada.")
            self.carrito.vaciar()
        except CarritoVacioError as error:
            print(f"Error: {error}")
        except OSError as error:
            print(f"No se pudo registrar la orden: {error}")

    def _registrar_orden(self):
        """Escribe la compra en ordenes.txt con fecha/hora, productos y total."""
        archivo = None
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            archivo = open(RUTA_ORDENES, "a", encoding="utf-8")
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            total = self.carrito.calcular_total()

            archivo.write(f"===== ORDEN ({fecha}) =====\n")
            archivo.write(f"Cliente: {self.nombre}\n")
            for item in self.carrito.items:
                p = item.producto
                archivo.write(
                    f"  - {p.nombre} x{item.cantidad} "
                    f"(${p.precio:,.0f} c/u) = ${item.subtotal():,.0f}\n")
            archivo.write(f"TOTAL: ${total:,.0f}\n\n")
        finally:
            # Pase lo que pase, si el archivo se abrió, lo cerramos
            if archivo is not None:
                archivo.close()
