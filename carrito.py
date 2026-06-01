from excepciones import CantidadInvalidaError

class ItemCarrito:
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad

    def subtotal(self):
        return self.producto.precio * self.cantidad


class Carrito:  #Contiene muchos ItemCarrito y calcula el total a pagar.
    def __init__(self):
        self.items = []  # composición: lista de ItemCarrito

    def esta_vacio(self):
        return len(self.items) == 0

    def agregar(self, producto, cantidad):
        """Agrega un producto al carrito validando la cantidad.

        Lanza CantidadInvalidaError si la cantidad no es un entero > 0.
        Si el producto ya estaba, suma la cantidad.
        """
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise CantidadInvalidaError(
                "La cantidad debe ser un número entero mayor que 0.")

        # Si ya existe el producto en el carrito, sumamos la cantidad
        for item in self.items:
            if item.producto.id == producto.id:
                item.cantidad += cantidad
                return item

        nuevo_item = ItemCarrito(producto, cantidad)
        self.items.append(nuevo_item)
        return nuevo_item

    def calcular_total(self):       # Suma los subtotales de todos los ítems.
        return sum(item.subtotal() for item in self.items)

    def vaciar(self):
        self.items.clear()
